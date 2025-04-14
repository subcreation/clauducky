# Clauducky Roadmap

This document outlines our development plan and milestones for Clauducky.

## Phase 1: Core Python Scripts
**Status: Completed ✅ (April 2025)**

### Goals
- Create foundational Python scripts for research and debugging
- Establish basic project structure and documentation

### Deliverables
- [x] Project structure setup
- [x] README.md with project overview
- [x] CLAUDE.md with current abilities definition
- [x] External Research Script
  - [x] Robust research script (`research.py`)
  - [x] Connect to external LLM (OpenAI/Anthropic)
  - [x] Pass queries and receive responses
  - [x] Format responses for Claude Code consumption
- [✓] Initial Ducky Debug Script (`ducky_debug.py`)
  - [✓] Accept problem descriptions and code snippets
  - [✓] Support for log files and expected behavior
  - [✓] Auto-select models based on problem complexity
  - [✓] Support multiple providers (OpenAI, Anthropic)
- [x] Basic tests to verify script functionality
  - [x] Unit tests for research script
  - [x] Unit tests for ducky_debug script

## Phase 2: Context Preservation and Process Enforcement
**Status: In Progress**

### Goals
- Address issues with context preservation after `/compact` commands
- Improve process enforcement and methodology adherence
- Implement safer git workflows for Claude Code
- Create initialization scripts for session management

### Deliverables
- [x] Context Preservation
  - [x] Create initialization script (`init.py`) to restore context after `/compact`
  - [x] Session state tracking with timestamps
  - [ ] Automatic detection of context loss
  - [ ] Interactive reorientation process

- [x] Git Workflow Safety (Priority)
  - [x] Create commit verification system
    - [x] Show diffs and require approval before committing
    - [x] Distinguish between verified/tested commits and experimental code
    - [x] Add commit tags for verified working states
  - [x] Implement safer commit message templates
    - [x] Add Clauducky attribution alongside Claude Code
    - [x] Option to suppress AI attribution for privacy
  - [x] Create "prepare commit" mode for user-managed git operations
  - [x] Implement automatic git backups before major changes
  - [ ] Add clean working directory enforcement
  
- [ ] Automated Workflow Enforcement (Future Enhancement)
  - [ ] Develop a state-tracking system that maintains workflow context
  - [ ] Create workflow phase detection (implementation, testing, review, commit)
  - [ ] Add automated checkpoints that verify requirements before proceeding
  - [ ] Implement process validation hooks that prevent workflow violations
  - [ ] Develop a prompt generator for context-aware user guidance
  - [ ] Create automatic recovery mechanisms for workflow deviations

- [ ] Enhanced Ducky Debug Workflow
  - [ ] Revise ducky_debug.py with structured debugging framework:
    - [ ] Create template/form for methodically documenting the problem
    - [ ] Add sections for expected behavior, actual behavior, evidence
    - [ ] Include prompts for listing already-tried solutions
    - [ ] Build checklist to ensure methodical debugging steps
  - [ ] Enhance interaction model for dual purpose:
    - [ ] Primary role: Serve as listener/collaborator during problem explanation process
    - [ ] Secondary role: Fresh outside perspective with potential breakthrough insights
    - [ ] Design prompts that specifically encourage questioning assumptions
    - [ ] Instruct model to evaluate if we're solving the right problem
    - [ ] Ensure complete relevant code context is provided for external review
    - [ ] Default to highest-capability models when progress stalls
    - [ ] Add automatic escalation to more powerful models after failed attempts
    - [ ] Create clear mechanism for suggesting research paths when knowledge gaps identified
    - [ ] Add option to iterate on explanations when clarification needed
  - [ ] Integration with existing tools:
    - [ ] Import and adapt console logging from thought-tree-prototype
    - [ ] Create mechanism to include snippets of logs in explanation
    - [ ] Support attaching screenshots/visuals to debugging context

- [ ] Research Script Improvements
  - [ ] Rename `research.py` to `search.py` for clarity and simplicity
  - [ ] Support both in-depth research and quick searches in a unified approach
  - [ ] Streamline usage with clearer command-line arguments

### Timeline
- Target completion: End of Q2 2025

## Potential Future Enhancement: "Enhanced Ducky Research"

**Rationale**: We've considered a more advanced approach to `research.py` that would go beyond a single query/response cycle. This could include:

1. **Iterative Querying**  
   - The script automatically performs multiple searches, refining each new query based on the previous result.

2. **Structured Thinking / Checklists**  
   - Before calling any external LLM, Claude Code follows a methodical checklist (e.g., identifying the core knowledge gap, clarifying search goals). 
   - This ensures we "rubber-duck" the research question thoroughly, potentially solving the issue without external calls.

3. **User Intervention Points**  
   - As the script refines its questions, it could prompt the developer for confirmation or additional details before continuing. 
   - This helps prevent runaway searches or wasted API calls.

4. **Smarter Model Selection**  
   - If needed, we may create a robust (and genuinely "smart") logic to pick a model—possibly involving a search-enabled LLM or an up-to-date local reference. 
   - This would require ongoing maintenance and might not be necessary if Claude Code itself can already make good decisions.

**When**: We'll evaluate the effectiveness of our current `research.py` approach during real projects. If we discover repeated shortcomings—like shallow queries, unnecessary costs, or incomplete info—we'll revisit these ideas.

---

## Phase 2: Logging and Screenshot Analysis
**Status: In Progress**

### Goals
- Implement browser console logging integration
- Create screenshot capture and analysis capabilities

### Deliverables
- [ ] Console Logging System
  - JavaScript collector for browser logs
  - Log storage and formatting
  - Log analysis in Python
- [ ] Screenshot Tools
  - Screenshot capture script
  - Image analysis using vision-capable LLMs
  - Design comparison utilities
- [ ] Updated documentation and examples

### Timeline
- Target start: Q3 2025
- Target completion: End of Q3 2025

---

## Phase 3: Logging and Screenshot Analysis
**Status: Planned**

### Goals
- Implement browser console logging integration
- Create screenshot capture and analysis capabilities

### Deliverables
- [ ] Console Logging System
  - JavaScript collector for browser logs
  - Log storage and formatting
  - Log analysis in Python
- [ ] Screenshot Tools
  - Screenshot capture script
  - Image analysis using vision-capable LLMs
  - Design comparison utilities
- [ ] Updated documentation and examples

### Timeline
- Target start: Q3 2025
- Target completion: End of Q3 2025

---

## Phase 4: Intelligent Installation and Project Integration
**Status: In Progress**

### Goals
- Create an intelligent installation process that adapts to existing projects
- Add framework-specific templates and adaptations
- Provide seamless integration options for different project types

### Deliverables
- [x] Basic Setup Script
  - [x] Simple setup script to configure Clauducky environment
  - [x] Create virtual environment in Clauducky directory
  - [x] Install required dependencies 
  - [x] Generate .env file from template
  - [x] Set up logs directory structure properly for submodule usage

- [ ] LLM-Powered Intelligent Installer
  - [ ] Intelligent code analysis and integration without breaking existing functionality
  - [ ] Smart detection of HTML insertion points for console logging
  - [ ] Automatic migration path for projects with existing Clauducky components
  - [ ] Optional API key collection during installation for enhanced intelligence
  - [ ] Tiered installation options:
    - Basic: Manual integration with guidance
    - Standard: Semi-automated with human verification
    - Advanced: Fully automated with LLM-powered code modifications
  - [ ] Rollback capability for failed installations

- [ ] Framework-specific Templates and Adaptations
  - [ ] React/Next.js integration patterns
  - [ ] Vue/Nuxt integration patterns
  - [ ] Python/Django/Flask patterns
  - [ ] Other common frameworks

- [ ] Project Type Detection
  - [ ] Automatic detection of project structure and framework
  - [ ] Custom installation paths based on detected technologies
  - [ ] Dependency management appropriate to project type

- [ ] Configuration Management
  - [ ] Secure API key handling
  - [ ] Environment configuration helpers
  - [ ] Project-specific customization options

### Implementation Notes
- Use LLMs during installation to intelligently modify code when necessary
- Provide transparency about API key usage during installation
- Make advanced features optional for users concerned about sharing API keys
- Document real-world manual installation experiences to inform automated approaches

### Timeline
- Target start: Q4 2025
- Target completion: End of Q1 2026

---

## Critical Bugs and Fixes
**Status: URGENT - BLOCKING WORK**

### Goals
- Fix critical issues with API key detection and model selection
- Improve script naming and user experience
- Enhance research capabilities

### Deliverables
- [ ] Fix API Key Detection
  - Modify all scripts to check for API keys in multiple locations:
    - The clauducky directory itself
    - One level up (parent project directory)
    - Current working directory
  - Create clear error messages when keys aren't found
  - Document the API key location requirements
- [ ] Fix Model Selection
  - Update ducky_debug.py to ALWAYS use the most capable model by default
  - Remove "auto" selection that defaults to less capable models
  - Prioritize using the most advanced GPT model for reasoning tasks (not another Claude model)
  - Make model selection explicit and transparent

- [ ] Fix Ducky Debug Methodology - CRITICAL PRIORITY
  - Implement the planned Enhanced Ducky Debug Workflow immediately
  - Enforce methodical problem-solving approach (not superficial summaries)
  - REQUIRE providing complete relevant code and logs for analysis
  - Force Claude to identify and focus on key clues provided by users
  - Implement proper template enforcement REGARDLESS of how ducky_debug.py is invoked
  - Make template completion MANDATORY - do not allow shortcuts
  - ADD PROOF that all sections have been completed before proceeding
  
  NOTE: This is especially urgent because IT WAS ALREADY PLANNED as part of the Phase 2 "Enhanced Ducky Debug Workflow" features but was NEVER IMPLEMENTED despite being reported as an issue previously

- [ ] Improve Research Script
  - Add explicit prompting to force external search behavior
  - Modify prompt to require checking current information
  - Prevent answering from memory without searching
  - Add clear "searching the web" indication in output

- [ ] Script Naming Clarity
  - Rename setup_clauducky.sh to first_time_setup.sh or install_dependencies.sh
  - Make script purpose self-explanatory without requiring documentation
  - Clearly distinguish between setup (one-time) and initialization (context restoration)

- [ ] Documentation Updates
  - Add troubleshooting guide for common issues
  - Create clear guidance on API key configuration
  - Provide explicit examples of correct usage

### Timeline
- Target start: IMMEDIATE - BLOCKING ALL OTHER WORK
- Target completion: HIGHEST PRIORITY - MUST BE FIXED BEFORE ANY OTHER DEVELOPMENT

## Phase 5: Advanced Features
**Status: Future**

### Goals
- Implement more advanced AI-assisted workflows
- Create specialized tooling for complex scenarios

### Deliverables
- [ ] UI Test Automation
  - Visual regression testing
  - Automated UI accessibility checks
- [ ] Code Review Enhancement
  - PR suggestion generation
  - Security analysis integration
  - Performance optimization suggestions
- [ ] Custom Workflow Builder
  - User-defined scripts and triggers
  - Project-specific templates

### Timeline
- Target start: Q1 2026
- Target completion: Ongoing

---

## Feedback & Contributions

We welcome feedback on this roadmap and contributions to help accelerate development. Please create issues or pull requests with your suggestions.

This roadmap is subject to change based on user feedback and emerging requirements.