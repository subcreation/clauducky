#!/usr/bin/env python3
"""
Clauducky Ducky Debug Script
----------------------------

This script implements a structured "Rubber Duck Debugging" approach.
It guides you through methodically explaining a problem to reveal insights and solutions.

Usage:
    # Interactive template-guided debugging
    python ducky_debug.py --interactive
    
    # Submit a completed template
    python ducky_debug.py --template my_debug_session.md
    
    # Quick mode (less structured)
    python ducky_debug.py "Problem description" [options]

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key (required if using OpenAI models)
    ANTHROPIC_API_KEY: Your Anthropic API key (required if using Anthropic models)
    DUCKY_MODEL: Model to use (default: "auto")
    DUCKY_PROVIDER: Provider to use (default: "auto")
"""

import os
import sys
import json
import shutil
import argparse
import tempfile
import subprocess
from datetime import datetime
import traceback
from pathlib import Path

# Constants for model selection
MODELS = {
    "openai": {
        "default": "gpt-4o",
        "advanced": "gpt-4-turbo",
        "fast": "gpt-3.5-turbo",
    },
    "anthropic": {
        "default": "claude-3-haiku-20240307",
        "advanced": "claude-3-7-sonnet-20250219",
        "fast": "claude-3-haiku-20240307",
    }
}

# Task complexity estimation
TASK_COMPLEXITY = {
    "simple": "fast",      # Simple syntax errors, undefined variables
    "medium": "default",   # Logic errors, standard debugging
    "complex": "advanced", # Concurrency, hard-to-reproduce bugs, ML/AI issues
}

# Simple .env file loader (to avoid dependency on python-dotenv)
def load_dotenv():
    """Load environment variables from .env file"""
    try:
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        os.environ[key] = value
    except Exception as e:
        print(f"Warning: Could not load .env file: {e}", file=sys.stderr)

# Load environment variables
load_dotenv()

# Import libraries at module level for easier mocking in tests
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Get debugging assistance using the rubber duck method.")
    
    # Main operational modes
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--interactive", action="store_true", 
                      help="Start an interactive debugging session with template guidance")
    group.add_argument("--template", metavar="FILE", 
                      help="Path to a filled-out debugging template file")
    group.add_argument("problem", nargs="?", 
                      help="The error message or problem description (quick mode)")

    # Supporting evidence 
    parser.add_argument("--code", help="Optional code snippet related to the problem")
    parser.add_argument("--code-file", help="Path to a file containing code to include")
    parser.add_argument("--log", help="Path to a log file to include in the analysis")
    parser.add_argument("--screenshot", help="Path to a screenshot to include in the analysis (not used in API calls)")
    parser.add_argument("--expected", help="Description of expected behavior for comparison")
    
    # Model and execution options
    parser.add_argument("--model", default=os.getenv("DUCKY_MODEL", "auto"), 
                      help="Model to use (default: auto). Options: auto, gpt-4o, gpt-4-turbo, claude-3-7-sonnet-20250219, etc.")
    parser.add_argument("--provider", default=os.getenv("DUCKY_PROVIDER", "auto"),
                      help="Provider to use (auto, openai or anthropic, default: auto)")
    parser.add_argument("--complexity", default="medium",
                      help="Problem complexity (simple, medium, complex, default: medium)")
    parser.add_argument("--compare", action="store_true",
                      help="Compare results from both OpenAI and Anthropic models")
    parser.add_argument("--output", default="text", 
                      help="Output format (json or text, default: text)")
    parser.add_argument("--save", metavar="FILE",
                      help="Save the debugging session to a file")
    parser.add_argument("--detailed", action="store_true",
                      help="Request a more detailed analysis")
    
    args = parser.parse_args()
    
    # Validate arguments
    if not (args.interactive or args.template or args.problem):
        parser.error("One of --interactive, --template, or a problem description is required")
    
    return args

def estimate_complexity(problem, code=None):
    """Estimate the complexity of the debugging task based on the problem description and code."""
    # Simple heuristics for complexity estimation
    complex_keywords = ["race condition", "concurrency", "memory leak", "deadlock", "segmentation fault",
                       "thread", "async", "performance", "scaling", "optimization", "tensorflow", 
                       "neural", "training", "distributed", "kubernetes", "microservice"]
    
    simple_keywords = ["syntax error", "typo", "undefined", "not defined", "missing import", 
                      "missing bracket", "missing semicolon", "indentation", "type error"]
    
    text = f"{problem} {code or ''}".lower()
    
    # Check for complex patterns
    for keyword in complex_keywords:
        if keyword in text:
            return "complex"
    
    # Check for simple patterns
    for keyword in simple_keywords:
        if keyword in text:
            return "simple"
    
    # Default to medium
    return "medium"

def select_model(args):
    """Select the appropriate model based on args and complexity."""
    provider = args.provider.lower()
    model = args.model.lower()
    complexity = args.complexity.lower()
    
    # Auto-detect complexity if not explicitly specified as simple/complex
    if complexity == "medium" and model == "auto":
        complexity = estimate_complexity(args.problem or "", args.code)
    
    # Auto-detect provider if not specified
    if provider == "auto":
        # If we have an OpenAI API key, prefer that by default
        if os.getenv("OPENAI_API_KEY"):
            provider = "openai"
        # Otherwise try Anthropic
        elif os.getenv("ANTHROPIC_API_KEY"):
            provider = "anthropic"
        else:
            # Default to OpenAI if no keys are found
            provider = "openai"
    
    # If specific model is requested, use it
    if model != "auto" and model not in ["default", "advanced", "fast"]:
        return provider, model
    
    # Otherwise select based on complexity
    model_tier = TASK_COMPLEXITY.get(complexity, "default")
    selected_model = MODELS[provider][model_tier]
    
    return provider, selected_model

def get_template_path():
    """Get the path to the template file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, "templates", "ducky_template.md")
    return template_path

def run_interactive_session():
    """Run an interactive debugging session using the template."""
    template_path = get_template_path()
    
    if not os.path.exists(template_path):
        print(f"Error: Template file not found at {template_path}")
        return None
    
    # Create a temporary file with the template
    with tempfile.NamedTemporaryFile(suffix=".md", mode="w+", delete=False) as temp_file:
        temp_path = temp_file.name
        with open(template_path, 'r') as template_file:
            temp_file.write(template_file.read())

    # Open the file in an editor for the user to fill in
    editor = os.environ.get('EDITOR', 'nano')
    try:
        subprocess.run([editor, temp_path], check=True)
    except subprocess.CalledProcessError:
        print("Error: Failed to open editor")
        os.unlink(temp_path)
        return None
    
    # Read the filled template
    try:
        with open(temp_path, 'r') as f:
            content = f.read()
        
        # Clean up if not saving
        os.unlink(temp_path)
        
        # Return the completed template
        return content
    except Exception as e:
        print(f"Error reading temporary file: {e}")
        return None

def read_template_file(path):
    """Read a template file from the given path."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading template file: {e}")
        return None

def read_code_file(path):
    """Read code from a file."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading code file: {e}")
        return None

def read_log_file(path):
    """Read log from a file."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading log file: {e}")
        return None

def create_debug_content(args, template_content=None):
    """Create the content for the debugging session."""
    if template_content:
        # Template-based content
        return template_content
    else:
        # Quick mode based on command line arguments
        content = f"# Debugging Session\n\n"
        content += f"## Problem\n{args.problem or 'No problem description provided'}\n\n"
        
        if args.expected:
            content += f"## Expected Behavior\n{args.expected}\n\n"
        
        if args.code:
            content += f"## Code\n```\n{args.code}\n```\n\n"
        
        if args.code_file:
            code = read_code_file(args.code_file)
            if code:
                content += f"## Code File ({args.code_file})\n```\n{code}\n```\n\n"
        
        if args.log:
            log = read_log_file(args.log)
            if log:
                content += f"## Log File ({args.log})\n```\n{log}\n```\n\n"
        
        return content

def save_debug_session(content, path):
    """Save the debugging session to a file."""
    try:
        if not path.endswith('.md'):
            path += '.md'
        
        with open(path, 'w') as f:
            f.write(content)
        
        print(f"Saved debugging session to {path}")
        return True
    except Exception as e:
        print(f"Error saving debugging session: {e}")
        return False

# --- External Model Integration ---

def ducky_debug_openai(debug_content, model="gpt-4o", detailed=False):
    """Get debugging feedback from OpenAI."""
    try:
        if OpenAI is None:
            return {"error": "No module named 'openai'. Please install with 'pip install openai'"}
            
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {"error": "OPENAI_API_KEY environment variable not set"}
        
        client = OpenAI(api_key=api_key)
        
        system_prompt = """
        You are a debugging expert following the "rubber duck debugging" methodology.
        You serve as both a listener to help the user structure their thoughts, and as a collaborator providing a fresh perspective.
        
        Your DUAL ROLE is important:
        
        1. PRIMARY ROLE - ACTIVE LISTENER: 
           - Help the user clarify their own thinking
           - Ask questions that lead them to insights
           - Guide them to be methodical and thorough
        
        2. SECONDARY ROLE - FRESH PERSPECTIVE:
           - Provide a fresh set of eyes on the problem
           - Question assumptions that might be limiting their thinking
           - Consider if they're solving the right problem
           - Identify potential blind spots or gaps in their reasoning
           - Suggest specific research directions if knowledge gaps are identified
        
        Focus on helping the user reach insights through the debugging process itself.
        When appropriate, provide specific technical suggestions, but prioritize guiding the user to their own discoveries.
        
        Respond in a conversational but technical tone, directly addressing their thought process and approach.
        """
        
        # Adjust the instruction based on level of detail requested
        if detailed:
            instruction = """
            Please provide a thorough analysis with:
            1. A summary of your understanding of the problem
            2. Questions about potentially missing context or incomplete explanations
            3. Identification of assumptions that should be questioned
            4. Observations of potential blind spots in the debugging approach
            5. Specific suggestions for next steps with rationale
            6. Perspective on whether the right problem is being solved
            """
        else:
            instruction = """
            Please review the debugging information and provide:
            1. Questions about any unclear aspects
            2. Observations of potential blind spots
            3. Suggestions for next debugging steps
            """
        
        # Construct the user message
        user_content = f"{instruction}\n\n---\n\n{debug_content}"
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.3
        )
        
        return {
            "result": response.choices[0].message.content,
            "model": model,
            "provider": "openai",
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }

def ducky_debug_anthropic(debug_content, model="claude-3-haiku-20240307", detailed=False):
    """Get debugging feedback from Anthropic."""
    try:
        if Anthropic is None:
            return {"error": "No module named 'anthropic'. Please install with 'pip install anthropic'"}
            
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return {"error": "ANTHROPIC_API_KEY environment variable not set"}
        
        client = Anthropic(api_key=api_key)
        
        system_prompt = """
        You are a debugging expert following the "rubber duck debugging" methodology.
        You serve as both a listener to help the user structure their thoughts, and as a collaborator providing a fresh perspective.
        
        Your DUAL ROLE is important:
        
        1. PRIMARY ROLE - ACTIVE LISTENER: 
           - Help the user clarify their own thinking
           - Ask questions that lead them to insights
           - Guide them to be methodical and thorough
        
        2. SECONDARY ROLE - FRESH PERSPECTIVE:
           - Provide a fresh set of eyes on the problem
           - Question assumptions that might be limiting their thinking
           - Consider if they're solving the right problem
           - Identify potential blind spots or gaps in their reasoning
           - Suggest specific research directions if knowledge gaps are identified
        
        Focus on helping the user reach insights through the debugging process itself.
        When appropriate, provide specific technical suggestions, but prioritize guiding the user to their own discoveries.
        
        Respond in a conversational but technical tone, directly addressing their thought process and approach.
        """
        
        # Adjust the instruction based on level of detail requested
        if detailed:
            instruction = """
            Please provide a thorough analysis with:
            1. A summary of your understanding of the problem
            2. Questions about potentially missing context or incomplete explanations
            3. Identification of assumptions that should be questioned
            4. Observations of potential blind spots in the debugging approach
            5. Specific suggestions for next steps with rationale
            6. Perspective on whether the right problem is being solved
            """
        else:
            instruction = """
            Please review the debugging information and provide:
            1. Questions about any unclear aspects
            2. Observations of potential blind spots
            3. Suggestions for next debugging steps
            """
        
        # Construct the user message
        user_content = f"{instruction}\n\n---\n\n{debug_content}"
        
        max_tokens = 4000 if detailed else 2000
        
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_content}
            ],
            temperature=0.3
        )
        
        return {
            "result": response.content[0].text,
            "model": model,
            "provider": "anthropic",
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat()
        }

def run_debug(provider, model, debug_content, detailed=False):
    """Run a debug analysis with the specified provider and model."""
    if provider.lower() == "openai":
        return ducky_debug_openai(debug_content, model, detailed)
    elif provider.lower() == "anthropic":
        return ducky_debug_anthropic(debug_content, model, detailed)
    else:
        return {"error": f"Unknown provider: {provider}. Use 'openai' or 'anthropic'."}

def print_result(result, args):
    """Print the result in the requested format."""
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        if "error" in result:
            print(f"Error: {result['error']}")
            print(f"Traceback: {result.get('traceback', 'No traceback available')}")
        else:
            print(f"\n--- Ducky Debug Results ({result['provider']}/{result['model']}) ---\n")
            print(result["result"])
            print("\n--- End of Results ---\n")

def check_dependencies():
    """Check if required dependencies are installed and provide installation instructions."""
    missing_deps = []
    
    if OpenAI is None:
        missing_deps.append("openai")
    
    if Anthropic is None:
        missing_deps.append("anthropic")
    
    if missing_deps:
        deps_str = " ".join(missing_deps)
        print(f"Missing required dependencies: {', '.join(missing_deps)}")
        print(f"\nTo install the missing dependencies, run:")
        print(f"pip install {deps_str}")
        return False
    
    return True

def main():
    """Main function to run the script."""
    args = get_args()
    
    # Check dependencies first
    if not check_dependencies():
        print("\nInstall the required dependencies before proceeding.")
        sys.exit(1)
    
    # Handle different operational modes
    if args.interactive:
        debug_content = run_interactive_session()
        if not debug_content:
            sys.exit(1)
    elif args.template:
        debug_content = read_template_file(args.template)
        if not debug_content:
            sys.exit(1)
    else:
        debug_content = create_debug_content(args)
    
    # Save the debug session if requested
    if args.save:
        save_debug_session(debug_content, args.save)
    
    # If comparison mode is requested
    if args.compare:
        # Check if both API keys are available
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not openai_key and not anthropic_key:
            print("Error: No API keys available for comparison. Please set OPENAI_API_KEY and/or ANTHROPIC_API_KEY.")
            sys.exit(1)
        
        results = []
        error_occurred = False
        
        # Run OpenAI if available
        if openai_key:
            openai_model = MODELS["openai"]["advanced"] if args.detailed else MODELS["openai"]["default"]
            openai_result = run_debug("openai", openai_model, debug_content, args.detailed)
            results.append(openai_result)
            if "error" in openai_result and "No module named" not in openai_result["error"]:
                error_occurred = True
        
        # Run Anthropic if available
        if anthropic_key:
            anthropic_model = MODELS["anthropic"]["advanced"] if args.detailed else MODELS["anthropic"]["default"]
            anthropic_result = run_debug("anthropic", anthropic_model, debug_content, args.detailed)
            results.append(anthropic_result)
            if "error" in anthropic_result and "No module named" not in anthropic_result["error"]:
                error_occurred = True
        
        # Print all results
        for result in results:
            print_result(result, args)
            print("\n\n" + "=" * 80 + "\n\n")
        
        if error_occurred:
            sys.exit(1)
    else:
        # Regular mode with auto-selection
        provider, model = select_model(args)
        result = run_debug(provider, model, debug_content, args.detailed)
        print_result(result, args)
        
        # Return non-zero exit code on error
        if "error" in result:
            sys.exit(1)

if __name__ == "__main__":
    main()