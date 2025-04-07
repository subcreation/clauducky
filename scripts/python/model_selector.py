#!/usr/bin/env python3
"""
Clauducky Model Selector
------------------------

This script helps select the most appropriate model for a given task based on
task requirements. It uses the model_reference.json file to make recommendations.

Usage:
    python model_selector.py [--task TASK] [--provider PROVIDER] [--criteria CRITERIA]
"""

import os
import sys
import json
import argparse

def load_model_reference():
    """Load the model reference JSON file."""
    try:
        file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                               'models', 'model_reference.json')
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading model reference: {e}", file=sys.stderr)
        return None

def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Select an appropriate model for a task.")
    parser.add_argument("--task", default="standard_research", 
                      help="Task type (basic_research, standard_research, complex_research, visual_analysis)")
    parser.add_argument("--provider", default="openai",
                      help="Provider to use (openai or anthropic)")
    parser.add_argument("--criteria", default="balanced",
                      help="Selection criteria (speed, cost, quality, balanced)")
    return parser.parse_args()

def select_model(task="standard_research", provider="openai", criteria="balanced"):
    """Select an appropriate model based on task and criteria."""
    model_ref = load_model_reference()
    if not model_ref:
        return None
    
    # First check if we have a direct mapping for this task
    if task in model_ref["recommended_mappings"]:
        if provider in model_ref["recommended_mappings"][task]:
            return model_ref["recommended_mappings"][task][provider]
    
    # If no direct mapping or provider not found, select based on criteria
    if provider not in model_ref:
        print(f"Provider {provider} not found in model reference", file=sys.stderr)
        return None
    
    available_models = model_ref[provider]
    
    # Apply criteria-based selection
    if criteria == "speed":
        # Sort by response time, fastest first
        sorted_models = sorted(available_models.items(), 
                             key=lambda x: {"very fast": 1, "fast": 2, "medium": 3, "slow": 4, "very slow": 5}
                             .get(x[1].get("response_time", "medium"), 3))
    elif criteria == "cost":
        # Sort by cost, lowest first
        sorted_models = sorted(available_models.items(), 
                             key=lambda x: {"very low": 1, "low": 2, "medium": 3, "high": 4, "very high": 5}
                             .get(x[1].get("cost_profile", "medium"), 3))
    elif criteria == "quality":
        # Sort by presumed quality (inverse of cost)
        sorted_models = sorted(available_models.items(), 
                             key=lambda x: {"very low": 5, "low": 4, "medium": 3, "high": 2, "very high": 1}
                             .get(x[1].get("cost_profile", "medium"), 3))
    else:  # balanced or anything else
        # Return the standard research model
        if "standard_research" in model_ref["recommended_mappings"]:
            if provider in model_ref["recommended_mappings"]["standard_research"]:
                return model_ref["recommended_mappings"]["standard_research"][provider]
        # Default to first model if no standard mapping
        return list(available_models.keys())[0] if available_models else None
    
    # Return the first model after sorting
    return sorted_models[0][0] if sorted_models else None

def main():
    """Main function to run the script."""
    args = get_args()
    model = select_model(args.task, args.provider, args.criteria)
    
    if model:
        print(json.dumps({"model": model, "provider": args.provider}))
    else:
        print(json.dumps({"error": "Could not select an appropriate model"}))
        sys.exit(1)

if __name__ == "__main__":
    main()