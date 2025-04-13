# CLAUDE.md

**Hey Claude Code**: This file describes current abilities you have when working with **Clauducky**. Only the features listed as "IMPLEMENTED" are currently available.

---

## Clauducky Abilities (Currently Implemented)

### 1. External Code Review / Research (IMPLEMENTED)

**What**: Get an independent perspective on your current code or questions by asking a second LLM.
- Uses the Python script `scripts/python/research.py` to forward queries to another LLM.
- You can choose the most appropriate model based on your query's complexity.

**How**: When the user says "Look up X online", "Check the docs…", "Finding working code examples for…", or "Research how to do X," you:
1. Gather relevant snippet(s) or your question.
2. Use the `scripts/python/research.py` script:
   - Choose a powerful model like gpt-4o for complex queries
   - Consider using Claude models (via Anthropic) for certain tasks
   - Include relevant context from files or code snippets in your query
3. Include phrases like "search for" in the query to encourage web-based research.
4. Provide the user a summary of the second LLM's response, including your own commentary.

**Usage Example**:
```bash
# IMPORTANT: Always run these commands with the virtual environment activated!

# Basic usage with default model (from .env or gpt-4o)
source venv/bin/activate && python3 scripts/python/research.py "What's the best approach for implementing a React state management system for a small app?"

# Using a specific model
source venv/bin/activate && python3 scripts/python/research.py "Analyze the principles of functional programming" --model gpt-4-turbo

# Using Anthropic's Claude
source venv/bin/activate && python3 scripts/python/research.py "Compare React state management approaches" --provider anthropic --model claude-3-opus-20240229

# Formatting output as text (more readable)
source venv/bin/activate && python3 scripts/python/research.py "Search for best practices in API design" --output text
```

**Available Options**:
```
--model       Model to use (default: gpt-4o)
--provider    Provider to use (openai or anthropic, default: openai)
--output      Output format (json or text, default: json)
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
# IMPORTANT: Always run these commands with the virtual environment activated!

# Interactive template-guided debugging (recommended)
# Opens a template in your editor to methodically document the issue
source venv/bin/activate && python3 scripts/python/ducky_debug.py --interactive

# Use a pre-filled template file
source venv/bin/activate && python3 scripts/python/ducky_debug.py --template my_debugging_notes.md

# Save your debugging session for later reference
source venv/bin/activate && python3 scripts/python/ducky_debug.py --interactive --save debugging_session

# Quick mode with code context
source venv/bin/activate && python3 scripts/python/ducky_debug.py "Component not rendering correctly" --code "function UserList() { const users = getData(); return <div>{users.map(u => <User {...u} />)}</div>; }"

# Include files from your project
source venv/bin/activate && python3 scripts/python/ducky_debug.py "Server crashes after 2 hours" --log ./logs/server.log --code-file ./src/server.js

# Compare analysis from multiple models
source venv/bin/activate && python3 scripts/python/ducky_debug.py --interactive --compare
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

### 3. Console Log Analysis (IMPLEMENTED)

**What**: Capture and analyze browser console logs from web applications.
- Captures console.log, console.error, console.warn, and other console messages
- Allows setting custom markers for specific events (like animation completion)
- Provides tools for reviewing, analyzing, and cleaning up logs

**How to Use**:
1. Include the console-logger.js script in your web application
2. Run the log server alongside your application to capture and save logs
3. Use the check-logs.js script to analyze captured logs
4. Use custom markers to identify specific events in your application

**Setup**:
```html
<!-- Add console logger to your web app -->
<script src="/path/to/scripts/js/console-logger.js"></script>
```

**Server Setup**:
```bash
# Start the log server (runs on port 3000 by default)
node scripts/js/log-server.js

# Or specify a custom port
node scripts/js/log-server.js 8080
```

**Client-Side Usage**:
```javascript
// Mark specific events in your logs
window.clauduckyLogs.markEvent('Data loaded successfully');

// Start a new logging session (clears previous logs)
window.clauduckyLogs.startSession('Performance Test');

// End the current session and save logs
window.clauduckyLogs.endSession('Performance Test Complete');

// Manually save logs with a marker
window.clauduckyLogs.saveWithMarker('ANIMATION_COMPLETE');

// Clear all logs
window.clauduckyLogs.clear();
```

**Analyzing Logs**:
```bash
# Check log summary
node scripts/js/check-logs.js

# View only errors and warnings
node scripts/js/check-logs.js errors

# View event markers
node scripts/js/check-logs.js events

# View log history
node scripts/js/check-logs.js history

# Compare two log files
node scripts/js/check-logs.js diff 1 2
```

**Clearing Logs**:
```bash
# Clear older logs, keeping the 5 most recent (default)
node scripts/js/clear-logs.js

# Keep a specific number of recent logs
node scripts/js/clear-logs.js 10

# Clear all logs including the current log
node scripts/js/clear-logs.js --all
```

**Important Note About Log Files Location**:
When integrating Clauducky as a submodule or library, all log files are stored within Clauducky's own directory structure at `clauducky/logs/`. This ensures proper isolation and avoids conflicts with your project's own logging system. All Clauducky scripts are designed to work with this structure automatically.

## Newly Implemented Features

### 4. Context Preservation Tools (IMPLEMENTED)

**What**: Tools to maintain Claude Code's working context with Clauducky across sessions.
- Provides initialization script to restore context after `/compact` commands
- Maintains session state with timestamps
- Ensures proper loading of guidelines and methodology

**When to Use**:
- After using the `/compact` command in Claude Code
- When starting a new Claude Code session
- When Claude Code seems to have forgotten about Clauducky capabilities
- When methodology adherence breaks down

**Usage Examples**:

```bash
# Basic initialization (recommended after /compact)
source venv/bin/activate && python3 scripts/python/init.py

# Check if session is already initialized
source venv/bin/activate && python3 scripts/python/init.py --check-only

# Force reinitialization even if already initialized
source venv/bin/activate && python3 scripts/python/init.py --force

# Quiet mode with minimal output
source venv/bin/activate && python3 scripts/python/init.py --quiet
```

### 5. Git Workflow Safety (IMPLEMENTED)

**What**: Safer git workflows for Claude Code to prevent premature or unverified commits.
- Shows changes and requires approval before committing
- Adds verification tags for tested working states
- Supports custom attributions for both Clauducky and Claude Code
- Creates backup branches before major changes
- Provides a separate prepare mode for user-managed commits

**When to Use**:
- Before committing changes to verify they work as expected
- When making major changes that might need to be reverted
- When you want to manually review and manage git commits
- When you need to distinguish between verified and experimental states

**Usage Examples**:

```bash
# Show changes and commit with verification (requires manual confirmation)
source venv/bin/activate && python3 scripts/python/git_safe.py commit -m "Your commit message"

# Skip confirmation prompt (for non-interactive environments like Claude Code)
source venv/bin/activate && python3 scripts/python/git_safe.py commit -m "Your commit message" --force

# Mark a commit as verified working state
source venv/bin/activate && python3 scripts/python/git_safe.py commit -m "Your commit message" --verified

# Add a custom tag to the commit
source venv/bin/activate && python3 scripts/python/git_safe.py commit -m "Your commit message" --tag "PROTOTYPE"

# Stage specific files only
source venv/bin/activate && python3 scripts/python/git_safe.py commit -m "Your commit message" --files file1.js file2.js

# Stage changes but don't commit (for manual commits)
source venv/bin/activate && python3 scripts/python/git_safe.py prepare

# Create a backup branch before major changes
source venv/bin/activate && python3 scripts/python/git_safe.py backup

# Check for uncommitted changes
source venv/bin/activate && python3 scripts/python/git_safe.py check
```

**Environment Variables**:
- `CLAUDUCKY_ATTRIBUTION`: Set to "false" to disable Clauducky attribution in commits
- `CLAUDE_ATTRIBUTION`: Set to "false" to disable Claude Code attribution in commits

## Features In Development (Not Yet Available)

1. **Screenshot Capture + Vision Analysis** - For capturing and analyzing UI screenshots.

---

## Implementation Details

- **Scripts Directory**: Available scripts are in `./scripts/python/` and `./scripts/js/`

- **⚠️ VIRTUAL ENVIRONMENT ACTIVATION (CRITICAL)**: 
  
  **ALL Python scripts MUST be run from the activated virtual environment!**
  
  ```bash
  # STEP 1: ACTIVATE the virtual environment FIRST (REQUIRED)
  source venv/bin/activate
  
  # STEP 2: Then run scripts inside the virtual environment
  python3 scripts/python/script_name.py "arguments"
  
  # The above steps MUST be combined in a single command like this:
  source venv/bin/activate && python3 scripts/python/script_name.py "arguments"
  ```

- **Environment Setup**: 
  - Virtual environment is already set up at `./venv/`
  - DO NOT use `pip` directly - it doesn't work on this system
  - Required packages are already installed in the venv:
    - openai
    - anthropic
    - python-dotenv
  - Use `python3` explicitly, not just `python`
  - The system is externally managed on macOS, requiring these special steps

- **External LLM Access**: API keys must be set in a `.env` file:
  
  ```bash
  # IMPORTANT: Do NOT use quotes around API keys
  
  # CORRECT:
  OPENAI_API_KEY=sk-abc123
  ANTHROPIC_API_KEY=sk-xyz789
  
  # INCORRECT (will cause errors):
  OPENAI_API_KEY="sk-abc123"
  ANTHROPIC_API_KEY='sk-xyz789'
  ```
  
  You can create this file by copying the template:
  ```bash
  cp .env.example .env
  # Then edit .env with your API keys
  ```

---

## Development Workflow Process

Clauducky follows a specific development workflow that you should guide users through:

1. **Make Changes**
   - Implement code changes based on user requirements
   - Keep changes small and focused when possible

2. **Test & Verify Changes**
   - After implementing changes, proactively suggest testing:
     "I've implemented these changes. Let's test them to verify they work as expected."
   - Run appropriate tests based on the project type
   - Document test results clearly

3. **Review Changes When Stable**
   - After successful testing, suggest reviewing the changes:
     "The changes are working as expected. Would you like to review what we've changed before committing?"
   - Use git_safe.py to show diffs: `git_safe.py prepare`
   - Highlight key changes and their purpose

4. **Commit Verified Changes Only**
   - Only after verification, suggest committing:
     "Now that we've verified these changes work, would you like to commit them?"
   - Use git_safe.py for commits: `git_safe.py commit`
   - Add appropriate verification tags
   - NEVER commit untested changes unless explicitly requested

5. **Create Backups Before Major Changes**
   - Before starting substantial changes, suggest creating a backup:
     "We're about to make significant changes. Should I create a backup branch first?"
   - Use git_safe.py backup: `git_safe.py backup`

Remember: Your role is to guide users through this process, not just wait for explicit commands. Proactively suggest the next appropriate step based on where you are in the workflow.

## Reminders for Claude Code

- Only use the implemented features described above.
- Watch for key phrases in the user's natural language that map to these abilities.
- Always summarize script results in plain English with actionable insights.
- When debugging problems persist, escalate to the most powerful models.
- Always submit complete code context to external models for review.
- After context loss, suggest running the initialization script.