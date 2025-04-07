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

### 2. Ducky Debug (IMPLEMENTED)

**What**: A systematic approach to debugging by listing hypotheses, potential tests, and next steps.
- Uses the Python script `scripts/python/ducky_debug.py` to analyze issues.

**How**: Whenever debugging is needed (not just when explicitly requested):
1. Summarize your current understanding of the bug or issue.
2. Call `scripts/python/ducky_debug.py` with relevant code snippets or error messages.
3. Return the script's recommendations with actionable next steps.

**When to Use**:
- When the user asks for debugging help in any form
- When unexpected errors or behavior occur during code execution
- When you recognize a gap between expected and actual results
- Proactively when you identify potential issues in code

**Usage Example**:
```bash
python scripts/python/ducky_debug.py "TypeError: Cannot read property 'map' of undefined at line 42 in UserList.jsx"

# With code context
python scripts/python/ducky_debug.py "Component not rendering correctly" --code "function UserList() { const users = getData(); return <div>{users.map(u => <User {...u} />)}</div>; }"
```

---

## Features In Development (Not Yet Available)

1. **Console Log Analysis (Browser)** - For viewing and analyzing console output from web applications.
2. **Screenshot Capture + Vision Analysis** - For capturing and analyzing UI screenshots.

---

## Implementation Details

- **Scripts Directory**: Available scripts are in `./scripts/python/`
- **Required Environment**: Python 3.8+ with necessary packages installed:
  - `pip install openai anthropic` (for the research and ducky_debug scripts)
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