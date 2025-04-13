#!/bin/bash
# Clauducky Setup Script
# This script sets up the virtual environment and installs dependencies for Clauducky

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# Navigate up one level to get to the Clauducky root
CLAUDUCKY_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "🦆 Setting up Clauducky environment in $CLAUDUCKY_ROOT"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$CLAUDUCKY_ROOT/venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$CLAUDUCKY_ROOT/venv"
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to create virtual environment."
        exit 1
    fi
else
    echo "✅ Virtual environment already exists."
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source "$CLAUDUCKY_ROOT/venv/bin/activate"

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r "$CLAUDUCKY_ROOT/requirements.txt"
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f "$CLAUDUCKY_ROOT/.env" ]; then
    echo "🔑 Creating .env file from template..."
    cp "$CLAUDUCKY_ROOT/.env.example" "$CLAUDUCKY_ROOT/.env"
    echo "⚠️ Please edit the .env file and add your API keys."
else
    echo "✅ .env file already exists."
fi

# Create logs directory if it doesn't exist
if [ ! -d "$CLAUDUCKY_ROOT/logs" ]; then
    echo "📝 Creating logs directory..."
    mkdir -p "$CLAUDUCKY_ROOT/logs"
else
    echo "✅ Logs directory already exists."
fi

echo ""
echo "🎉 Clauducky setup complete! 🎉"
echo ""
echo "To use Clauducky, always activate the virtual environment first:"
echo "    source \"$CLAUDUCKY_ROOT/venv/bin/activate\""
echo ""
echo "Documentation is available in CLAUDE.md"
echo ""
echo "If you're using Clauducky as a submodule, you can run commands like:"
echo "    source \"$CLAUDUCKY_ROOT/venv/bin/activate\" && python3 \"$CLAUDUCKY_ROOT/scripts/python/research.py\" \"Your query here\""
echo ""