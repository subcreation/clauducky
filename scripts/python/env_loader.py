#!/usr/bin/env python3
"""
Clauducky Environment Loader
----------------------------

This module provides functions for loading environment variables from .env files.
It supports both simple file parsing and python-dotenv if available.

Usage:
    from env_loader import load_env
    load_env()
"""

import os
import sys
import importlib.util

def load_env():
    """
    Load environment variables from .env file.
    
    Uses python-dotenv if available, falls back to simple parsing if not.
    Handles both quoted and unquoted values correctly.
    """
    # Try to use python-dotenv if available
    dotenv_spec = importlib.util.find_spec("dotenv")
    
    if dotenv_spec is not None:
        try:
            import dotenv
            # Get the project root directory
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            env_path = os.path.join(root_dir, '.env')
            
            # Load environment variables
            dotenv.load_dotenv(env_path)
            print("Environment loaded with python-dotenv")
            return True
        except Exception as e:
            print(f"Warning: Error using python-dotenv: {e}", file=sys.stderr)
            # Fall back to simple parsing
            return _simple_env_load()
    else:
        print("Warning: python-dotenv not found, using simple environment parsing", file=sys.stderr)
        return _simple_env_load()

def _simple_env_load():
    """
    Simple .env file parser that handles quotes correctly.
    """
    try:
        # Get the project root directory
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        env_path = os.path.join(root_dir, '.env')
        
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remove quotes if present
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                            
                        os.environ[key] = value
            return True
        else:
            print(f"Warning: .env file not found at {env_path}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"Warning: Could not load .env file: {e}", file=sys.stderr)
        return False

# Provide a way to test this module
if __name__ == "__main__":
    success = load_env()
    if success:
        print("Environment variables loaded successfully")
        # Print count of loaded variables (without exposing values)
        env_keys = [k for k in os.environ.keys() if k in ('OPENAI_API_KEY', 'ANTHROPIC_API_KEY')]
        print(f"Loaded keys: {', '.join(env_keys)}")
    else:
        print("Failed to load environment variables")
        sys.exit(1)