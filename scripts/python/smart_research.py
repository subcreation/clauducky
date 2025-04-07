#!/usr/bin/env python3
"""
Clauducky Smart Research Script
------------------------------

This script combines model selection and research in one step.
It automatically selects the most appropriate model based on the query complexity.

Usage:
    python smart_research.py "Your query here" [--task TASK] [--provider PROVIDER] [--criteria CRITERIA] [--output FORMAT]
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime

# Add the parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

# Import the model selector
try:
    from model_selector import select_model
except ImportError:
    print("Error: Could not import model_selector module", file=sys.stderr)
    sys.exit(1)

def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Smart research with automatic model selection.")
    parser.add_argument("query", help="The query or code snippet to research")
    parser.add_argument("--task", default="standard_research", 
                      help="Task type (basic_research, standard_research, complex_research, visual_analysis)")
    parser.add_argument("--provider", default="openai",
                      help="Provider to use (openai or anthropic)")
    parser.add_argument("--criteria", default="balanced",
                      help="Selection criteria (speed, cost, quality, balanced)")
    parser.add_argument("--output", default="text", 
                      help="Output format (json or text, default: text)")
    return parser.parse_args()

def estimate_complexity(query):
    """Estimate the complexity of the query to suggest a task type."""
    # Simple heuristics for complexity estimation
    query_lower = query.lower()
    words = query_lower.split()
    
    # Check for complex phrases
    complex_indicators = ["analyze", "compare", "evaluate", "synthesize", "implications", 
                         "theory", "complex", "detailed", "thorough", "comprehensive",
                         "nuanced", "sophisticated", "advanced"]
    
    # Check for simple queries
    simple_indicators = ["what is", "how to", "when did", "where is", "list", "basic",
                        "simple", "quick", "brief", "summary"]
    
    # Check for visual tasks
    visual_indicators = ["image", "picture", "diagram", "screenshot", "visual", "look at"]
    
    # Count indicators
    complex_count = sum(1 for word in words if any(ind in word for ind in complex_indicators))
    simple_count = sum(1 for word in words if any(ind in word for ind in simple_indicators))
    visual_count = sum(1 for word in words if any(ind in word for ind in visual_indicators))
    
    # Determine task type based on counts
    if visual_count > 0:
        return "visual_analysis"
    elif complex_count > simple_count:
        return "complex_research"
    elif simple_count > complex_count or len(words) < 10:
        return "basic_research"
    else:
        return "standard_research"

def run_research(query, model, provider, output_format):
    """Run the research script with the selected model."""
    research_script = os.path.join(script_dir, "research.py")
    
    try:
        cmd = [
            sys.executable,
            research_script,
            query,
            "--model", model,
            "--provider", provider,
            "--output", output_format
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return json.dumps({
            "error": f"Research script execution failed: {e}",
            "stderr": e.stderr,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return json.dumps({
            "error": f"Failed to run research: {e}",
            "timestamp": datetime.now().isoformat()
        })

def main():
    """Main function to run the script."""
    args = get_args()
    
    # If task is auto, estimate complexity
    if args.task == "auto":
        args.task = estimate_complexity(args.query)
    
    # Select the appropriate model
    model = select_model(args.task, args.provider, args.criteria)
    
    if not model:
        print(json.dumps({
            "error": "Could not select an appropriate model",
            "timestamp": datetime.now().isoformat()
        }))
        sys.exit(1)
    
    # Print model selection info if output is text
    if args.output == "text":
        print(f"Selected model: {model} ({args.provider}) for task type: {args.task}\n")
    
    # Run the research with the selected model
    result = run_research(args.query, model, args.provider, args.output)
    print(result)

if __name__ == "__main__":
    main()