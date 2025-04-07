# CLAUDE.md

**Hey Claude Code**: This file describes current abilities you have when working with **Clauducky**. Only the features listed as "IMPLEMENTED" are currently available.

---

## Clauducky Abilities (Currently Implemented)

### 1. External Code Review / Research (IMPLEMENTED)

**What**: Get an independent perspective on your current code or questions by asking a second LLM.
- Uses the Python script `scripts/python/smart_research.py` to forward queries to another LLM.
- Automatically selects the appropriate model based on query complexity.

**How**: When the user says "Get an outside opinion" or "Research how to do X," you:
1. Gather relevant snippet(s) or your question.
2. Use the `scripts/python/smart_research.py` script which handles model selection automatically:
   - For general research, it will use gpt-4o (default)
   - For complex reasoning tasks, it will select gpt-4-turbo
   - For simple questions, it may select gpt-3.5-turbo for efficiency
3. Include phrases like "search for" in the query to encourage web-based research.
4. Provide the user a summary of the second LLM's response, including your own commentary.

**Usage Example**:
```bash
# Basic usage (automatically selects appropriate model)
python scripts/python/smart_research.py "What's the best approach for implementing a React state management system for a small app?"

# With explicit search request
python scripts/python/smart_research.py "Search for the latest React state management libraries and compare their features"

# Override automatic selection for specific needs
python scripts/python/smart_research.py "Analyze the principles of functional programming" --task complex_research

# Optimize for cost
python scripts/python/smart_research.py "What is React?" --criteria cost
```

**Advanced Options**:
You can still use the original research script with manual model selection if needed:
```bash
python scripts/python/research.py "Your query" --model gpt-4-turbo --provider openai
```

### 2. Ducky Debug (INITIAL VERSION IMPLEMENTED)

**What**: A systematic approach to "rubber duck debugging" - the practice of methodically explaining a problem to reveal insights and solutions.
- Uses a structured framework to guide thorough problem explanation and analysis
- The current script (`scripts/python/ducky_debug.py`) is an initial implementation that needs enhancement

**Dual Purpose**:
- **Primary Purpose**: Structure our own thinking through methodical explanation
  - Forces complete documentation of expected vs. actual behavior
  - The process of explanation often reveals the solution itself
  - Uses the external model primarily as a listener/collaborator
  - Leverages the independence of the external model as a feature, not a bug

- **Secondary Purpose**: Gain fresh perspectives that may provide breakthroughs
  - The external model can question our assumptions
  - May identify when we're solving the wrong problem
  - Can spot patterns or issues we've become blind to
  - May suggest research directions when knowledge gaps exist

**How to Use Effectively**:
1. When encountering a bug, start by creating a complete explanation:
   - What you expect to happen and why
   - What's actually happening (with specific evidence)
   - Your current understanding of the discrepancy
   - Steps you've already taken
   - Pending hypotheses to test
2. As you prepare this explanation, run additional tests if gaps in understanding emerge
3. Use the external model as a collaborator in the debugging process
4. Focus on high-reasoning models (GPT-4o, Claude 3.7 Sonnet) for breakthrough insights

**When to Use**:
- When debugging requires methodical thinking
- When you've been stuck on an issue for too long
- When you need to break out of circular thinking
- When explaining to a "duck" might reveal your own blind spots

**Usage Examples**:

```bash
# Interactive template-guided debugging (recommended)
# Opens a template in your editor to methodically document the issue
source venv/bin/activate
python3 scripts/python/ducky_debug.py --interactive

# Use a pre-filled template file
python3 scripts/python/ducky_debug.py --template my_debugging_notes.md

# Save your debugging session for later reference
python3 scripts/python/ducky_debug.py --interactive --save debugging_session

# Quick mode with code context
python3 scripts/python/ducky_debug.py "Component not rendering correctly" --code "function UserList() { const users = getData(); return <div>{users.map(u => <User {...u} />)}</div>; }"

# Include files from your project
python3 scripts/python/ducky_debug.py "Server crashes after 2 hours" --log ./logs/server.log --code-file ./src/server.js

# Compare analysis from multiple models
python3 scripts/python/ducky_debug.py --interactive --compare
```

**Operational Modes**:
- `--interactive`: Guides you through a structured debugging process (recommended)
- `--template FILE`: Uses a pre-filled debugging template
- Direct problem description: Quick mode for simple issues

**Evidence Options**:
- `--code`: Include code snippet directly in command
- `--code-file`: Include code from a file
- `--log`: Include log file content
- `--expected`: Describe expected behavior
- `--screenshot`: Reference a screenshot (for context only)

**Model Options**:
- `--model`: Specify model or "auto" for automatic selection
- `--provider`: Choose "openai", "anthropic", or "auto"
- `--complexity`: Indicate problem complexity as "simple", "medium", or "complex"
- `--compare`: Get analysis from both OpenAI and Anthropic
- `--detailed`: Request more thorough analysis

**Output Options**:
- `--output`: Format as "json" or "text" (default: text)
- `--save FILE`: Save debugging session to a file

---

## Features In Development (Not Yet Available)

1. **Console Log Analysis (Browser)** - For viewing and analyzing console output from web applications.
2. **Screenshot Capture + Vision Analysis** - For capturing and analyzing UI screenshots.

---

## Implementation Details

- **Scripts Directory**: Available scripts are in `./scripts/python/`
- **Required Environment**: Python 3.13 running in a virtual environment:
  ```bash
  # IMPORTANT: All script execution must use the virtual environment
  source venv/bin/activate
  python3 scripts/python/script_name.py "arguments"
  ```
- **Environment Setup**: 
  - Virtual environment is already set up at `./venv/`
  - DO NOT use `pip` directly - it doesn't work on this system
  - Required packages are already installed in the venv:
    - openai
    - anthropic
  - Use `python3` explicitly, not just `python`
  - The system is externally managed on macOS, requiring these special steps
- **External LLM Access**: API keys should be set in `.env` file:
  ```
  OPENAI_API_KEY=your_key_here
  ANTHROPIC_API_KEY=your_key_here
  ```

---

## Reminders for Claude Code

- Only use the implemented features described above.
- Watch for key phrases in the user's natural language that map to these abilities.
- Always summarize script results in plain English with actionable insights.