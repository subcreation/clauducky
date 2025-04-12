#!/usr/bin/env python3
"""
Clauducky Initialization Script
-------------------------------

This script helps maintain Claude Code's awareness of Clauducky capabilities.
It should be run at the beginning of sessions or after context-clearing operations.

Usage:
    # Basic initialization
    source venv/bin/activate
    python3 scripts/python/init.py
    
    # Check if the session has been initialized already
    python3 scripts/python/init.py --check-only
"""

import os
import sys
import argparse
from datetime import datetime

def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Initialize Clauducky capabilities in Claude Code"
    )
    
    parser.add_argument(
        "--check-only", 
        action="store_true",
        help="Only check if session is initialized, don't run initialization"
    )
    
    parser.add_argument(
        "--force", 
        action="store_true",
        help="Force reinitialization even if already initialized"
    )
    
    parser.add_argument(
        "--quiet", 
        action="store_true",
        help="Suppress detailed output"
    )
    
    return parser.parse_args()

def get_clauducky_root():
    """Get the root directory of the Clauducky project."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels to get to the Clauducky root
    clauducky_root = os.path.dirname(os.path.dirname(script_dir))
    return clauducky_root

def get_session_file_path():
    """Get the path to the session state file."""
    clauducky_root = get_clauducky_root()
    return os.path.join(clauducky_root, '.clauducky_session')

def get_claude_md_path():
    """Get the path to the CLAUDE.md file."""
    clauducky_root = get_clauducky_root()
    return os.path.join(clauducky_root, 'CLAUDE.md')

def check_session_initialized():
    """Check if a session has been initialized."""
    session_file = get_session_file_path()
    
    if not os.path.exists(session_file):
        return False
    
    # Check if file was created recently (within last 6 hours)
    file_time = os.path.getmtime(session_file)
    current_time = datetime.now().timestamp()
    six_hours = 6 * 60 * 60  # 6 hours in seconds
    
    if current_time - file_time > six_hours:
        return False
    
    try:
        with open(session_file, 'r') as f:
            for line in f:
                if line.startswith('initialized=') and 'true' in line.lower():
                    return True
    except Exception:
        return False
    
    return False

def save_session_state(initialized=True):
    """Save the session state to a file."""
    session_file = get_session_file_path()
    
    try:
        with open(session_file, 'w') as f:
            f.write(f"initialized={str(initialized).lower()}\n")
            f.write(f"timestamp={datetime.now().isoformat()}\n")
            f.write(f"script_version=1.0\n")
        return True
    except Exception as e:
        print(f"Error saving session state: {e}", file=sys.stderr)
        return False

def load_claude_md():
    """Load the contents of CLAUDE.md."""
    claude_md_path = get_claude_md_path()
    
    if not os.path.exists(claude_md_path):
        print(f"Error: CLAUDE.md not found at {claude_md_path}", file=sys.stderr)
        return None
    
    try:
        with open(claude_md_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading CLAUDE.md: {e}", file=sys.stderr)
        return None

def display_core_guidelines(quiet=False):
    """Display the core guidelines from CLAUDE.md."""
    content = load_claude_md()
    
    if not content:
        return False
    
    if not quiet:
        print("\n" + "=" * 80)
        print("CLAUDE CODE ORIENTATION SESSION - PLEASE READ CAREFULLY")
        print("Loading Clauducky methodology and guidelines...")
        print("=" * 80 + "\n")
        
        print(content)
        
        print("\n" + "=" * 80)
        print("IMPORTANT: Please confirm you've read and understood these guidelines.")
        print("Type 'confirm' when ready to proceed.")
        print("=" * 80 + "\n")
    else:
        # In quiet mode, just print a brief message
        print("Claude Code orientation: Clauducky methodology loaded.")
    
    return True

def initialize_session(args):
    """Initialize the Clauducky session with Claude Code."""
    if check_session_initialized() and not args.force:
        print("Session already initialized. Use --force to reinitialize.")
        return True
    
    # Display guidelines and require confirmation
    if not display_core_guidelines(args.quiet):
        return False
    
    # In a real interactive environment, we'd wait for confirmation
    # Since this will be run by Claude, we'll skip that and just save the state
    
    # Save the session state
    if save_session_state():
        if not args.quiet:
            print("\nSession initialized successfully.")
        return True
    else:
        print("Failed to initialize session.")
        return False

def main():
    """Main function to run the script."""
    args = get_args()
    
    if args.check_only:
        if check_session_initialized():
            print("Session is initialized.")
            sys.exit(0)
        else:
            print("Session is not initialized.")
            sys.exit(1)
    else:
        if initialize_session(args):
            sys.exit(0)
        else:
            sys.exit(1)

if __name__ == "__main__":
    main()