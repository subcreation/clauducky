#!/bin/bash
# Test script for research.py

# Change to the script directory
cd "$(dirname "$0")"

# Test the research script with a simple query
echo "Testing research.py with OpenAI..."
python python/research.py "What are the best practices for implementing a React component that manages form state?" --output text

# Test with Anthropic if you want to try both
# echo -e "\n\nTesting with Anthropic..."
# python python/research.py "What are the best practices for implementing a React component that manages form state?" --provider anthropic --model claude-3-opus-20240229 --output text