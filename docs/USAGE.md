# Clauducky Usage Guide

This document provides detailed instructions on how to set up and use the Clauducky scripts.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- API keys for OpenAI and/or Anthropic (depending on which services you want to use)

### Installation

1. **Set up a virtual environment**

   It's recommended to use a virtual environment to avoid package conflicts:

   ```bash
   # Create a virtual environment
   python3 -m venv venv
   
   # Activate the virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**

   Copy the `.env.example` file to create your own `.env` file:

   ```bash
   cp .env.example .env
   ```

   Then edit the `.env` file to add your API keys:
   
   ```
   # OpenAI API key for GPT models
   OPENAI_API_KEY=your_openai_key_here
   
   # Anthropic API key for Claude models
   ANTHROPIC_API_KEY=your_anthropic_key_here
   
   # Default model settings
   RESEARCH_MODEL=gpt-4o
   RESEARCH_PROVIDER=openai
   DUCKY_MODEL=gpt-4o
   DUCKY_PROVIDER=openai
   ```

## Using the Scripts

### Research Script

The research script forwards your query to an external LLM (like OpenAI's GPT-4 or Anthropic's Claude) and returns the results:

**Basic usage:**

```bash
python scripts/python/research.py "Your research question here"
```

**Advanced options:**

```bash
python scripts/python/research.py "Your research question here" --provider openai --model gpt-4o --output text
```

**Available options:**
- `--provider`: Choose between `openai` or `anthropic` (default: value from `.env` or `openai`)
- `--model`: Specify the model to use
  - For OpenAI: `gpt-4o`, `gpt-4-turbo`, etc.
  - For Anthropic: `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, etc.
- `--output`: Format of the output, either `json` or `text` (default: `json`)

### Ducky Debug Script

The ducky debug script uses the rubber duck debugging approach to analyze a problem and suggest debugging steps.

**Basic usage:**

```bash
python scripts/python/ducky_debug.py "Your error message or problem description"
```

**With code snippet:**

```bash
python scripts/python/ducky_debug.py "Your error message" --code "function example() { console.log('test'); }"
```

**Advanced options:**

```bash
python scripts/python/ducky_debug.py "Your error message" --provider anthropic --model claude-3-haiku-20240307 --output text
```

**Available options:**
- `--code`: Optional code snippet related to the problem
- `--provider`: Choose between `openai` or `anthropic` (default: value from `.env` or `openai`)
- `--model`: Specify the model to use (default: value from `.env` or `gpt-4o`)
- `--output`: Format of the output, either `json` or `text` (default: `json`)

## Model Selection Guidelines

- **For research tasks:** 
  - OpenAI's `gpt-4o` is recommended for its strong reasoning and built-in search capabilities
  - For deeper analysis on complex topics, consider `gpt-4-turbo` or Anthropic's `claude-3-opus`
  
- **For debugging tasks:**
  - OpenAI's `gpt-4o` works well for most debugging scenarios
  - For simpler bugs, `gpt-3.5-turbo` or `claude-3-haiku` may be faster and more cost-effective
  
- **For code review:**
  - Anthropic's `claude-3-opus` or `claude-3-sonnet` often excel at detailed code analysis
  - OpenAI's `gpt-4o` is also strong for code review tasks

## Troubleshooting

If you encounter any issues:

1. **API key errors:**
   - Ensure your API keys are correctly set in the `.env` file
   - Check that you have sufficient credits/quota on your API accounts

2. **Package installation problems:**
   - Make sure your virtual environment is activated
   - Try updating pip: `pip install --upgrade pip`
   - If a specific package fails, try installing it separately

3. **Model availability:**
   - Not all models are available to all API users
   - Check your account access level if a model is unavailable