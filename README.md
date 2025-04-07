# Clauducky

**Clauducky** is a **portable toolkit** for AI-assisted development workflows, especially when used with [**Claude Code**](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) — Anthropic's agentic coding assistant that runs in your terminal.

---

## Overview

Clauducky aims to bridge key gaps in Claude Code's abilities by providing **scripts** and **workflows** to help an AI assistant:

- **Research** new coding tasks before implementation  
- **Brainstorm** or review code changes  
- **Capture console output** from front-end apps so Claude Code can "see" what's happening in the browser  
- **Take and interpret screenshots** of UI changes, optionally comparing them to design mockups  
- **Suggest or verify tests**, plan debugging steps, and more

The end goal is to let you have **richer, more automated conversations** with Claude Code throughout your dev cycle—without manually shuttling logs, images, or references between windows.

---

## Current Status (Phase 1)

We're in **early development**. Right now, you'll find:

1. **A `CLAUDE.md`** file (in this repo) defining how Claude Code should interpret phrases like "look at the logs" or "research this approach," so it can call the appropriate scripts.
2. **Initial Python Scripts** (e.g., a "research" script, or "ducky" debugging) that you can copy into your project to let Claude Code consult an external LLM or generate debugging hypotheses.
3. **(Optional) Browser Logging**: Some proof-of-concept JavaScript for capturing front-end console logs—if you're doing web dev.

Many of the bigger features—like screenshot analysis or advanced code reviews—are still **on our roadmap** (see `ROADMAP.md`). If you see references to those features, please note they may not be fully implemented yet!

---

## Quick Start (Alpha Version)

1. **Clone this repo**:
   ```bash
   git clone https://github.com/subcreation/clauducky
   cd clauducky
   ```

2. **Copy (or symlink) the scripts you need into your project**:
   - Python-based "research" or "ducky" scripts:
     ```bash
     cp scripts/python/research.py /path/to/your-project/scripts/research.py
     cp scripts/python/ducky_debug.py /path/to/your-project/scripts/ducky_debug.py
     ```
   - JavaScript-based browser logging (if you need it):
     ```bash
     cp scripts/js/console-logger.js /path/to/your-project/scripts/console-logger.js
     ```

3. **Add CLAUDE.md to your project root**
   - This file explains how to use Clauducky's abilities in natural language.
   - Claude Code will automatically read CLAUDE.md for context each session.
   ```bash
   cp CLAUDE.md /path/to/your-project/
   ```

4. **Install Dependencies**
   - For Python scripts:
     ```bash
     pip install -r requirements.txt
     ```
   - For Node-based logging scripts:
     ```bash
     npm install
     ```

5. **Set up API keys**
   - Copy the `.env.example` file to a new file named `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file to add your API keys:
     - Get an OpenAI API key from https://platform.openai.com/api-keys
     - Get an Anthropic API key from https://console.anthropic.com/
   - The `.env` file is gitignored to keep your keys private

6. **Use with Claude Code**
   - In your Claude Code terminal, simply ask in natural language to "research this approach," or "let's do a ducky debug," etc.
   - Claude Code will reference your CLAUDE.md definitions to decide which script(s) to run.

Note: Because we're in an early phase, setup might require some manual steps. For detailed usage instructions, see the [USAGE.md](docs/USAGE.md) file. Eventually, we plan a single "installer" command (like `npx clauducky init`) for quick setup.

---

## Roadmap

For more details on what's done and what's coming, see `ROADMAP.md`. Here's a brief outline:

1. **Phase 1**: Core Python scripts (e.g., research, "ducky debug") + minimal docs.
2. **Phase 2**: Additional scripts for screenshot analysis, design comparisons, and advanced code review.
3. **Phase 3**: Automated "installer" CLI for easily integrating Clauducky into new or existing projects.
4. **Phase 4**: UI test automation, custom workflows, unit test coverage suggestions, etc.

---

## Philosophy & Best Practices

We view AI (like Claude Code) as an accelerator—not a replacement—for human developers. Key reminders:
- **Stay in control**: Always read and understand AI-generated code or logs.
- **Keep learning**: The more you know, the better your prompts and decisions will be.
- **Give real context**: Provide designs, logs, or specs so the AI sees the bigger picture.

Learn more about our approach in AI as Thought Accelerant on VerseZine.com. If Clauducky helps you, please sign up on VerseZine to support us!

---

## Support & Contributing
- **Free & Open Source**: We welcome issues and pull requests!
- **Community**: Create or comment on issues if you have ideas or need help.
- **Extend**: Clauducky can pair with other code-review AIs (e.g., MentatBot) or custom scripts.

---

## License

Licensed under MIT. Clauducky is not affiliated with Anthropic; we reference "Claude Code" purely for compatibility.

Happy coding—and quacking!