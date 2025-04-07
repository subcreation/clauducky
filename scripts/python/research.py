#!/usr/bin/env python3
"""
Clauducky Research Script
-------------------------

This script forwards a query to an external LLM (like OpenAI's GPT models)
to get a second opinion or gather research on a topic. It can be used by
Claude Code to expand its knowledge or get alternative perspectives.

Usage:
    python research.py "Your query here"

Environment Variables:
    OPENAI_API_KEY: Your OpenAI API key (required if using OpenAI models)
    ANTHROPIC_API_KEY: Your Anthropic API key (required if using Claude models)
    RESEARCH_MODEL: Model to use (default: "gpt-4o")
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
    parser = argparse.ArgumentParser(description="Get research or a second opinion from an LLM.")
    parser.add_argument("query", help="The query or code snippet to research")
    parser.add_argument("--model", default=os.getenv("RESEARCH_MODEL", "gpt-4o"), 
                      help="Model to use (default: gpt-4o)")
    parser.add_argument("--provider", default=os.getenv("RESEARCH_PROVIDER", "openai"),
                      help="Provider to use (openai or anthropic, default: openai)")
    parser.add_argument("--output", default="json", 
                      help="Output format (json or text, default: json)")
    return parser.parse_args()

def research_with_openai(query, model="gpt-4o"):
    """Get research results from OpenAI."""
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return {"error": "OPENAI_API_KEY environment variable not set"}
        
        client = OpenAI(api_key=api_key)
        
        system_prompt = """
        You are a helpful research assistant providing clear, accurate information. 
        Focus on providing factual, practical advice and explanations.
        Be concise but thorough. Include code examples when relevant.
        Format your response in Markdown.
        """
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
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

def research_with_anthropic(query, model="claude-3-haiku-20240307"):
    """Get research results from Anthropic."""
    try:
        from anthropic import Anthropic
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return {"error": "ANTHROPIC_API_KEY environment variable not set"}
        
        client = Anthropic(api_key=api_key)
        
        system_prompt = """
        You are a helpful research assistant providing clear, accurate information. 
        Focus on providing factual, practical advice and explanations.
        Be concise but thorough. Include code examples when relevant.
        Format your response in Markdown.
        """
        
        response = client.messages.create(
            model=model,
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": query}
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
        result = research_with_openai(args.query, args.model)
    elif args.provider.lower() == "anthropic":
        result = research_with_anthropic(args.query, args.model)
    else:
        result = {"error": f"Unknown provider: {args.provider}. Use 'openai' or 'anthropic'."}
    
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"\n--- Research Results ({result['provider']}/{result['model']}) ---\n")
            print(result["result"])
            print("\n--- End of Results ---\n")
    
    # Return non-zero exit code on error
    if "error" in result:
        sys.exit(1)

if __name__ == "__main__":
    main()