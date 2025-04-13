# Clauducky

**Clauducky** is a **portable toolkit** for AI-assisted development workflows, especially when used with [**Claude Code**](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) — Anthropic's agentic coding assistant that runs in your terminal.

---

## Overview

Clauducky is a **process-oriented toolkit** that enhances Claude Code's capabilities while guiding it through methodical software development workflows. It provides specialized scripts and processes that benefit both participants:

**For Human Developers**, Clauducky:
- Reduces cognitive load by automating routine tasks
- Enforces good development practices automatically
- Maintains project stability with verified commits
- Eliminates manual work of managing logs and context
- Preserves context across sessions and `/compact` commands

**For Claude Code**, Clauducky:
- Provides clear workflow guidelines and process checkpoints
- Gives access to external resources via specialized scripts
- Structures debugging and research methodologies
- Helps maintain context across sessions
- Prevents common workflow errors

Current capabilities include:
- **Research** via external LLMs with specialized domain knowledge
- **Methodical debugging** using structured "rubber duck" techniques
- **Context preservation** across sessions and `/compact` commands
- **Safe git workflows** with verification and backup mechanisms
- **Console logging** for browser-based applications

Clauducky slows down the process in strategic ways ("you have to slow down to go faster") to achieve better results, fewer regressions, and more predictable outcomes—all while freeing human developers to focus on vision and creativity rather than process management.

---

## Current Status (Phase 2 In Progress)

Clauducky has completed Phase 1 and is actively developing Phase 2 features. Currently available:

1. **Methodical Development Workflow** defined in `CLAUDE.md` that guides Claude Code through a process of making changes, testing, verification, and commits.

2. **Core Python Scripts**:
   - `research.py`: Connect to external LLMs for specialized knowledge and research
   - `ducky_debug.py`: Structured "rubber duck" debugging with methodical problem analysis
   - `init.py`: Context preservation across sessions and `/compact` commands
   - `git_safe.py`: Safe git workflows with verification, backups, and tagging

3. **Browser Logging Tools**:
   - JavaScript tools for capturing and analyzing browser console output
   - Streamlined reporting of front-end issues to Claude Code

4. **Process Enforcement**:
   - Development workflow process with clear checkpoints
   - Git safety mechanisms to prevent unverified commits
   - Session state tracking to maintain context

Features still on our roadmap include screenshot analysis, advanced debugging tools, and more (see `ROADMAP.md` for details).

---

## Quick Start

There are two ways to use Clauducky: either install individual scripts into your project, or clone the entire repository for a self-contained experience.

### Method 1: Clone the Complete Repository (Recommended)

1. **Clone the repo in your project**:
   ```bash
   git clone https://github.com/subcreation/clauducky
   ```

2. **Run the setup script**:
   ```bash
   ./clauducky/scripts/setup_clauducky.sh
   ```
   
   This will:
   - Create a virtual environment in the clauducky directory
   - Install all required dependencies
   - Create a .env file from the template
   - Set up the logs directory

3. **Edit your API keys**:
   ```bash
   # Edit the .env file with your API keys
   nano clauducky/.env
   ```

4. **Initialize with Claude Code**:
   In Claude Code, run:
   ```bash
   source clauducky/venv/bin/activate && python3 clauducky/scripts/python/init.py
   ```

Claude Code will now be aware of all Clauducky capabilities and the recommended workflow.

### Method 2: Use as a Git Submodule

1. **Add Clauducky as a submodule**:
   ```bash
   git submodule add https://github.com/subcreation/clauducky.git
   ```

2. **Run the setup script**:
   ```bash
   ./clauducky/scripts/setup_clauducky.sh
   ```

3. **Edit your API keys**:
   ```bash
   # Edit the .env file with your API keys
   nano clauducky/.env
   ```

4. **Initialize with Claude Code**:
   ```bash
   source clauducky/venv/bin/activate && python3 clauducky/scripts/python/init.py
   ```

> **Note**: When using as a submodule, all log files are stored in the `clauducky/logs/` directory, making Clauducky self-contained.

### Method 3: Individual Script Installation

1. **Copy the scripts you need**:
   ```bash
   mkdir -p scripts/python scripts/js
   cp clauducky/scripts/python/research.py scripts/python/
   cp clauducky/scripts/python/ducky_debug.py scripts/python/
   cp clauducky/scripts/python/init.py scripts/python/
   cp clauducky/scripts/python/git_safe.py scripts/python/
   cp clauducky/scripts/python/env_loader.py scripts/python/
   
   # Optional: Copy JavaScript logging tools
   cp clauducky/scripts/js/console-logger.js scripts/js/
   cp clauducky/scripts/js/log-server.js scripts/js/
   ```

2. **Copy CLAUDE.md to your project root**:
   ```bash
   cp clauducky/CLAUDE.md ./
   ```

3. **Set up environment**:
   ```bash
   cp clauducky/.env.example .env
   # Edit .env with your API keys
   
   python -m venv venv
   source venv/bin/activate
   pip install -r clauducky/requirements.txt
   ```

4. **Initialize with Claude Code**:
   ```bash
   source venv/bin/activate && python3 scripts/python/init.py
   ```

### Using Clauducky with Claude Code

Once initialized, Claude Code will guide you through the development workflow:

1. Implementing changes
2. Testing and verifying
3. Reviewing changes
4. Making validated commits

Key commands for Claude Code:
```bash
# Research a topic
source venv/bin/activate && python3 scripts/python/research.py "Your research query"

# Methodical debugging
source venv/bin/activate && python3 scripts/python/ducky_debug.py --interactive

# Reinitialize after /compact
source venv/bin/activate && python3 scripts/python/init.py

# Safe git commits
source venv/bin/activate && python3 scripts/python/git_safe.py commit -m "Your commit message" --verified --force
```

For detailed usage instructions, see the [USAGE.md](docs/USAGE.md) file.

---

## Roadmap

For detailed development plans, see `ROADMAP.md`. Here's a brief outline of our phases:

1. ✅ **Phase 1: Core Python Scripts** (Completed)
   - Research and external LLM integration
   - Initial ducky debug implementation
   - Basic documentation

2. 🔄 **Phase 2: Context Preservation and Process Enforcement** (In Progress)
   - Context preservation across sessions
   - Improved git workflow safety
   - Methodical development process
   - Automated workflow enforcement

3. 📅 **Phase 3: Logging and Screenshot Analysis** (Planned)
   - Enhanced browser console logging
   - Screenshot capture and analysis
   - Visual UI comparison tools

4. 📅 **Phase 4: Installation and Project Integration** (Planned)
   - Automated installer
   - Framework-specific templates
   - Project type detection

5. 📅 **Phase 5: Advanced Features** (Future)
   - UI test automation
   - Advanced code review
   - Custom workflow builders

---

## Philosophy & Best Practices

Clauducky embodies several key principles for productive AI-assisted development:

- **Process Over Speed**: Following methodical processes leads to fewer regressions and better outcomes. As with learning any skill, "you have to slow down to go faster."

- **Dual-Participant Design**: Clauducky is designed with both human developers and AI assistants in mind, optimizing the experience for both participants.

- **Guided Workflow**: Rather than leaving process management to chance, Clauducky provides clear checkpoints and verification steps.

- **Context Preservation**: Maintaining shared understanding between sessions is critical for continuity and building on previous work.

- **Verification First**: Changes should be tested and verified before being committed, preserving project stability.

- **Continuous Documentation**: Keeping documentation updated alongside code changes ensures everyone understands the evolving system.

We view AI assistants as accelerators for human creativity—not replacements for human judgment. Clauducky helps both humans and AI assistants work together more effectively by providing structure, tools, and processes that complement their respective strengths.

---

## Support & Contributing
- **Free & Open Source**: We welcome issues and pull requests!
- **Community**: Create or comment on issues if you have ideas or need help.
- **Extend**: Clauducky can pair with other code-review AIs (e.g., MentatBot) or custom scripts.

---

## License

Licensed under MIT. Clauducky is not affiliated with Anthropic; we reference "Claude Code" purely for compatibility.

Happy coding—and quacking!