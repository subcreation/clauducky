#!/usr/bin/env python3
"""
Clauducky Git Safety Script
---------------------------

This script provides a safer git workflow for Claude Code, addressing issues with
premature commits and unverified changes.

Usage:
    # Show staged and unstaged changes, requiring approval before commit
    source venv/bin/activate
    python3 scripts/python/git_safe.py commit

    # Prepare a commit (stage changes) but don't actually commit
    python3 scripts/python/git_safe.py prepare

    # Create a backup branch before major changes
    python3 scripts/python/git_safe.py backup

Environment Variables:
    CLAUDUCKY_ATTRIBUTION: Set to "false" to disable Clauducky attribution in commits
    CLAUDE_ATTRIBUTION: Set to "false" to disable Claude Code attribution in commits
"""

import os
import sys
import argparse
import subprocess
from datetime import datetime

# Default attribution messages
CLAUDUCKY_ATTR = "🦆 Powered by [Clauducky](https://github.com/subcreation/clauducky)"
CLAUDE_ATTR = "🤖 Generated with [Claude Code](https://claude.ai/code)"
CO_AUTHOR = "Co-Authored-By: Claude <noreply@anthropic.com>"

def get_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Safer git workflow for Claude Code."
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Commit command
    commit_parser = subparsers.add_parser("commit", help="Show changes and commit with verification")
    commit_parser.add_argument("--message", "-m", help="Commit message")
    commit_parser.add_argument("--files", nargs="+", help="Specific files to stage (default: all changed files)")
    commit_parser.add_argument("--verified", action="store_true", help="Mark commit as verified working state")
    commit_parser.add_argument("--tag", help="Add a custom tag to the commit message")
    
    # Prepare command
    prepare_parser = subparsers.add_parser("prepare", help="Stage changes but don't commit")
    prepare_parser.add_argument("--files", nargs="+", help="Specific files to stage (default: all changed files)")
    
    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create a backup branch")
    backup_parser.add_argument("--name", help="Custom backup branch name")
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Check for uncommitted changes")
    
    args = parser.parse_args()
    
    # Default to showing help if no command is provided
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    return args

def run_command(command, description=None, check=True):
    """Run a shell command and return the output."""
    if description:
        print(f"\n=== {description} ===")
    
    try:
        # Use text=True to get string output
        result = subprocess.run(
            command, 
            shell=True, 
            check=check, 
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(f"ERROR: {result.stderr}", file=sys.stderr)
            
        return result.stdout
    
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr}")
        if check:
            sys.exit(e.returncode)
        return None

def show_changes():
    """Show current git status and changes."""
    print("\n=== Current Status ===")
    run_command("git status", check=False)
    
    print("\n=== Staged Changes ===")
    run_command("git diff --staged", check=False)
    
    print("\n=== Unstaged Changes ===")
    run_command("git diff", check=False)
    
    return True

def get_recent_commits(count=3):
    """Show recent commits to help with commit message style."""
    print("\n=== Recent Commits ===")
    run_command(f"git log --oneline -n {count}", "Recent commits for reference", check=False)
    
    return True

def build_commit_message(message, verified=False, tag=None):
    """Build a properly formatted commit message with attributions."""
    # Get environment variables for attribution settings
    include_clauducky = os.getenv("CLAUDUCKY_ATTRIBUTION", "true").lower() != "false"
    include_claude = os.getenv("CLAUDE_ATTRIBUTION", "true").lower() != "false"
    
    # Start with the user's message
    full_message = message.strip()
    
    # Add verification tag if requested
    if verified:
        full_message = f"[VERIFIED] {full_message}"
    
    # Add custom tag if provided
    if tag:
        full_message = f"[{tag}] {full_message}"
    
    # Add attributions
    attributions = []
    if include_clauducky:
        attributions.append(CLAUDUCKY_ATTR)
    if include_claude:
        attributions.append(CLAUDE_ATTR)
    
    # Add co-author if Claude attribution is included
    if include_claude:
        co_author_line = f"\n\n{CO_AUTHOR}"
    else:
        co_author_line = ""
    
    # Combine everything
    if attributions:
        attribution_text = " ".join(attributions)
        full_message = f"{full_message}\n\n{attribution_text}{co_author_line}"
    
    return full_message

def safe_commit(args):
    """Show changes and ask for confirmation before committing."""
    # Show current changes
    show_changes()
    
    # Show recent commits for reference
    get_recent_commits()
    
    # If no message was provided, prompt for one
    if not args.message:
        print("\nERROR: Commit message is required.")
        print("Use --message or -m to provide a commit message.")
        return False
    
    # Build complete commit message
    commit_message = build_commit_message(
        args.message, 
        verified=args.verified,
        tag=args.tag
    )
    
    # Display the commit message that will be used
    print("\n=== Commit Message ===")
    print(commit_message)
    
    # Ask for confirmation
    print("\nReady to commit these changes?")
    confirmation = input("Type 'yes' to commit: ")
    
    if confirmation.lower() != "yes":
        print("Commit cancelled.")
        return False
    
    # Stage files if specific ones were requested
    if args.files:
        file_list = " ".join([f'"{f}"' for f in args.files])
        run_command(f"git add {file_list}", "Staging specific files")
    else:
        # Otherwise stage all changes
        run_command("git add -A", "Staging all changes")
    
    # Create the commit with the formatted message
    # Use a heredoc to preserve formatting in the commit message
    commit_cmd = f"""git commit -m "$(cat <<'EOF'
{commit_message}
EOF
)"
"""
    run_command(commit_cmd, "Creating commit")
    
    # Show the result
    run_command("git status", "Updated status")
    
    print("\nCommit created successfully.")
    return True

def prepare_commit(args):
    """Stage changes but don't commit."""
    # Show current changes first
    show_changes()
    
    # Stage files if specific ones were requested
    if args.files:
        file_list = " ".join([f'"{f}"' for f in args.files])
        run_command(f"git add {file_list}", "Staging specific files")
    else:
        # Otherwise stage all changes
        run_command("git add -A", "Staging all changes")
    
    # Show the updated status
    run_command("git status", "Updated status")
    
    print("\nChanges staged successfully. Use 'git commit' to create the commit.")
    return True

def create_backup(args):
    """Create a backup branch before making major changes."""
    # Get current branch name
    current_branch = run_command("git rev-parse --abbrev-ref HEAD", check=False).strip()
    
    # Create a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Generate backup branch name
    if args.name:
        backup_name = f"backup/{args.name}_{timestamp}"
    else:
        backup_name = f"backup/{current_branch}_{timestamp}"
    
    # Create the backup branch
    run_command(f"git checkout -b {backup_name}", f"Creating backup branch: {backup_name}")
    
    # Show result
    print(f"\nBackup created as branch: {backup_name}")
    
    # Go back to the original branch
    run_command(f"git checkout {current_branch}", f"Returning to {current_branch}")
    
    return True

def check_changes():
    """Check for uncommitted changes."""
    # Check if there are any uncommitted changes
    status = run_command("git status --porcelain", check=False)
    
    if status.strip():
        print("\nWARNING: There are uncommitted changes:")
        show_changes()
        return False
    else:
        print("\nWorking directory is clean.")
        return True

def main():
    """Main function to run the script."""
    args = get_args()
    
    # Handle the appropriate command
    if args.command == "commit":
        safe_commit(args)
    elif args.command == "prepare":
        prepare_commit(args)
    elif args.command == "backup":
        create_backup(args)
    elif args.command == "check":
        check_changes()
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)

if __name__ == "__main__":
    main()