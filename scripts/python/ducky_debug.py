#!/usr/bin/env python3
"""
Clauducky Ducky Debug Script
----------------------------

This script implements the "Rubber Duck Debugging" approach with AI assistance.
It analyzes a problem description and generates hypotheses, tests, and next steps.
This can be used by Claude Code to get a second perspective on debugging challenges.

Usage:
    python ducky_debug.py "Your error or problem description here"
    python ducky_debug.py "Your problem description" --code "const x = getData(); console.log(x.items);"
    python ducky_debug.py "Component not rendering" --model "gpt-4o" --provider "openai"

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key (required if using OpenAI models)
    ANTHROPIC_API_KEY: Your Anthropic API key (required if using Claude models)
    DUCKY_MODEL: Model to use (default: "gpt-4o")
    DUCKY_PROVIDER: Provider to use (default: "openai")
"""

import os
import sys
import json
import argparse
from datetime import datetime
import traceback

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

def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Get debugging assistance using the rubber duck method.")
    parser.add_argument("problem", help="The error message or problem description")
    parser.add_argument("--code", help="Optional code snippet related to the problem")
    parser.add_argument("--log", help="Path to a log file to include in the analysis")
    parser.add_argument("--screenshot", help="Path to a screenshot to include in the analysis (not used in API calls, but for context)")
    parser.add_argument("--expected", help="Description of expected behavior for comparison")
    parser.add_argument("--model", default=os.getenv("DUCKY_MODEL", "gpt-4o"), 
                      help="Model to use (default: gpt-4o)")
    parser.add_argument("--provider", default=os.getenv("DUCKY_PROVIDER", "openai"),
                      help="Provider to use (openai or anthropic, default: openai)")
    parser.add_argument("--output", default="json", 
                      help="Output format (json or text, default: json)")
    parser.add_argument("--detailed", action="store_true",
                      help="Request more detailed analysis")
    return parser.parse_args()

def ducky_debug_openai(problem, code=None, log_file=None, expected=None, detailed=False, model="gpt-4o"):
    """Get debugging hypotheses from OpenAI."""
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {"error": "OPENAI_API_KEY environment variable not set"}
        
        client = OpenAI(api_key=api_key)
        
        system_prompt = """
        You are an expert debugging assistant following the "rubber duck debugging" methodology.
        Given a problem description and optional code snippet, you will:
        
        1. Analyze the problem carefully, looking for obvious issues and common pitfalls
        2. Generate 3-5 specific hypotheses about what might be causing the issue
        3. For each hypothesis, suggest a concrete test or verification step that would confirm or refute it
        4. Recommend next debugging steps in order of priority, with clear actionable instructions
        5. Include code examples or log patterns to watch for when applicable
        
        Format your response in Markdown with these sections:
        
        ## Analysis
        Brief analysis of the problem and its potential root causes.
        
        ## Hypotheses
        1. **Hypothesis 1**: Clear description
           - **Test**: Specific verification step
           - **Expected outcome if true**: What you would observe if this hypothesis is correct
        
        2. **Hypothesis 2**: ...
        
        ## Recommended Steps
        1. First priority action
        2. Second priority action
        3. ...
        
        ## Additional Diagnostics
        Any additional logging, tools, or approaches that might help isolate the issue.
        """
        
        user_content = f"Problem: {problem}\n\n"
        
        if expected:
            user_content += f"Expected behavior: {expected}\n\n"
            
        if code:
            user_content += f"Related code:\n```\n{code}\n```\n\n"
            
        if log_file:
            try:
                with open(log_file, 'r') as f:
                    log_content = f.read()
                user_content += f"Log file content:\n```\n{log_content}\n```\n\n"
            except Exception as log_error:
                user_content += f"Error reading log file: {str(log_error)}\n\n"
        
        if detailed:
            user_content += "Please provide a detailed analysis with comprehensive hypotheses and thorough testing steps.\n\n"
        
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

def ducky_debug_anthropic(problem, code=None, log_file=None, expected=None, detailed=False, model="claude-3-haiku-20240307"):
    """Get debugging hypotheses from Anthropic."""
    try:
        from anthropic import Anthropic
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return {"error": "ANTHROPIC_API_KEY environment variable not set"}
        
        client = Anthropic(api_key=api_key)
        
        system_prompt = """
        You are an expert debugging assistant following the "rubber duck debugging" methodology.
        Given a problem description and optional code snippet, you will:
        
        1. Analyze the problem carefully, looking for obvious issues and common pitfalls
        2. Generate 3-5 specific hypotheses about what might be causing the issue
        3. For each hypothesis, suggest a concrete test or verification step that would confirm or refute it
        4. Recommend next debugging steps in order of priority, with clear actionable instructions
        5. Include code examples or log patterns to watch for when applicable
        
        Format your response in Markdown with these sections:
        
        ## Analysis
        Brief analysis of the problem and its potential root causes.
        
        ## Hypotheses
        1. **Hypothesis 1**: Clear description
           - **Test**: Specific verification step
           - **Expected outcome if true**: What you would observe if this hypothesis is correct
        
        2. **Hypothesis 2**: ...
        
        ## Recommended Steps
        1. First priority action
        2. Second priority action
        3. ...
        
        ## Additional Diagnostics
        Any additional logging, tools, or approaches that might help isolate the issue.
        """
        
        user_content = f"Problem: {problem}\n\n"
        
        if expected:
            user_content += f"Expected behavior: {expected}\n\n"
            
        if code:
            user_content += f"Related code:\n```\n{code}\n```\n\n"
            
        if log_file:
            try:
                with open(log_file, 'r') as f:
                    log_content = f.read()
                user_content += f"Log file content:\n```\n{log_content}\n```\n\n"
            except Exception as log_error:
                user_content += f"Error reading log file: {str(log_error)}\n\n"
        
        if detailed:
            user_content += "Please provide a detailed analysis with comprehensive hypotheses and thorough testing steps.\n\n"
        
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

def main():
    """Main function to run the script."""
    args = get_args()
    
    if args.provider.lower() == "openai":
        result = ducky_debug_openai(
            problem=args.problem,
            code=args.code,
            log_file=args.log,
            expected=args.expected,
            detailed=args.detailed,
            model=args.model
        )
    elif args.provider.lower() == "anthropic":
        result = ducky_debug_anthropic(
            problem=args.problem,
            code=args.code,
            log_file=args.log,
            expected=args.expected,
            detailed=args.detailed,
            model=args.model
        )
    else:
        result = {"error": f"Unknown provider: {args.provider}. Use 'openai' or 'anthropic'."}
    
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
    
    # Return non-zero exit code on error
    if "error" in result:
        sys.exit(1)

if __name__ == "__main__":
    main()