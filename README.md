# CDF (Claude Dev Framework)

A comprehensive development framework plugin for Claude Code featuring **23 commands**, **19 agent personas**, **6 skills**, and **3 lifecycle hooks**.

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
- [Agents](#agents)
- [Skills](#skills)
- [Hooks](#hooks)
- [How It Works](#how-it-works)
- [Plugin Structure](#plugin-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## Installation

### From Marketplace (Recommended)

**Step 1: Add the marketplace**
```bash
# Via CLI (outside Claude Code)
claude plugin marketplace add drag88/claude-dev-framework
```

**Step 2: Install the plugin**
```bash
# Inside Claude Code
/plugin install cdf@claude-dev-framework
```

Or browse in `/plugin > Discover` and select CDF.

### Local Development

```bash
# Clone the repository
git clone https://github.com/drag88/claude-dev-framework.git

# Run Claude with the plugin
claude --plugin-dir ./claude-dev-framework
```

### Verify Installation

```bash
# Inside Claude Code
/cdf:help
```

### Agents (Automatic Setup)

Agents are automatically configured on first session start. The plugin creates symlinks from its agents to `~/.claude/agents/`, making them accessible globally via `@agent-name` syntax.

If you need to manually re-run setup:
```bash
/cdf:setup
```

---

## Quick Start

### 1. Automatic Project Analysis

When you start a Claude session in any project, CDF automatically:
- Analyzes your codebase structure
- Generates `.claude/rules/` documentation
- Loads project context for intelligent assistance

### 2. Use Commands

```bash
# Analyze code quality
/cdf:analyze src/

# Get implementation help
/cdf:implement "add user authentication"

# Research a topic
/cdf:research "best practices for React state management"

# Run tests with analysis
/cdf:test
```

### 3. Leverage Agents

```bash
# Get architecture guidance
/cdf:spawn "design microservices architecture"

# Debug complex issues
/cdf:troubleshoot "API returning 500 errors"
```

---

## Commands

All commands are prefixed with `/cdf:`. See [commands/INDEX.md](commands/INDEX.md) for the complete reference.

### Core Development

| Command | Description |
|---------|-------------|
| `/cdf:implement` | Feature implementation with persona activation and MCP integration |
| `/cdf:build` | Build, compile, and package projects with error handling |
| `/cdf:test` | Execute tests with coverage analysis and quality reporting |
| `/cdf:git` | Git operations with intelligent commit messages |
| `/cdf:cleanup` | Clean up code, remove dead code, optimize structure |
| `/cdf:improve` | Apply systematic improvements to code quality |

### Analysis & Understanding

| Command | Description |
|---------|-------------|
| `/cdf:analyze` | Comprehensive code analysis (quality, security, performance) |
| `/cdf:explain` | Clear explanations of code and concepts |
| `/cdf:research` | Deep web research with adaptive planning |
| `/cdf:troubleshoot` | Diagnose and resolve issues |

### Planning & Design

| Command | Description |
|---------|-------------|
| `/cdf:brainstorm` | Interactive requirements discovery |
| `/cdf:design` | Design system architecture and APIs |
| `/cdf:estimate` | Development effort estimation |
| `/cdf:workflow` | Generate implementation workflows from PRDs |

### Orchestration

| Command | Description |
|---------|-------------|
| `/cdf:task` | Execute complex tasks with delegation |
| `/cdf:spawn` | Break down complex tasks into subtasks |
| `/cdf:panel` | Multi-expert panel discussions |

### Utilities

| Command | Description |
|---------|-------------|
| `/cdf:help` | List all available commands |
| `/cdf:docs` | Documentation management |
| `/cdf:rules` | Generate and manage project rules |
| `/cdf:session` | Session management and context handling |
| `/cdf:select-tool` | Intelligent MCP tool selection |
| `/cdf:setup` | Set up agents for @agent-name usage |

---

## Agents

CDF includes 19 specialized agent personas. See [agents/INDEX.md](agents/INDEX.md) for the complete reference.

### Architecture & Design

| Agent | Use Case |
|-------|----------|
| `system-architect` | High-level system design and architecture |
| `backend-architect` | APIs, databases, server-side systems |
| `frontend-architect` | UI/UX, components, accessibility |
| `devops-architect` | CI/CD, infrastructure, deployment |

### Analysis & Research

| Agent | Use Case |
|-------|----------|
| `deep-research-agent` | Comprehensive multi-source research |
| `codebase-navigator` | Find code and trace dependencies |
| `library-researcher` | Evaluate open-source libraries |
| `root-cause-analyst` | Debug complex issues |
| `media-interpreter` | Interpret PDFs, images, diagrams |

### Quality & Performance

| Agent | Use Case |
|-------|----------|
| `quality-engineer` | Testing strategies and QA |
| `security-engineer` | Security audits and best practices |
| `performance-engineer` | Optimization and profiling |
| `refactoring-expert` | Code improvement and cleanup |

### Communication & Education

| Agent | Use Case |
|-------|----------|
| `technical-writer` | Documentation and guides |
| `learning-guide` | Teaching through examples |
| `socratic-mentor` | Learning through questions |

### Specialized

| Agent | Use Case |
|-------|----------|
| `python-expert` | Python-specific guidance |
| `requirements-analyst` | Requirements gathering |
| `business-panel-experts` | Business strategy analysis |

### Using Agents

Agents are automatically activated based on task context, or you can reference them in commands:

```bash
# Spawn activates relevant agents automatically
/cdf:spawn "design authentication system"

# Task delegates to appropriate agents
/cdf:task execute "security audit" --delegate
```

---

## Skills

Skills are automatically invoked based on context. They provide specialized behaviors without explicit commands.

| Skill | Trigger | Purpose |
|-------|---------|---------|
| **rules-generator** | Missing `.claude/rules/` | Auto-generates project documentation |
| **claudemd-generator** | After rules generation | Creates `CLAUDE.generated.md` |
| **context-saver** | Context approaching 75%+ | Saves session progress |
| **external-memory** | Complex tasks (50+ tool calls) | File-based working memory |
| **intent-gate** | Every request | Classifies request type for optimal handling |
| **failure-recovery** | 3 consecutive failures | STOP → REVERT → DOCUMENT → CONSULT |

### External Memory Pattern

For complex tasks, CDF uses file-based memory in `dev/memory/`:

```
dev/memory/
├── task_plan.md      # Goal, phases, progress tracking
├── notes.md          # Research findings, decisions
└── deliverable.md    # Final output draft
```

### Intent Classification

Every request is classified before action:
- **Trivial** → Direct execution
- **Explicit** → Specific command execution
- **Exploratory** → Research first, then act
- **GitHub Work** → Full workflow with validation
- **Ambiguous** → Ask for clarification

---

## Hooks

CDF uses 3 lifecycle hooks for automation:

| Event | Script | Purpose |
|-------|--------|---------|
| **SessionStart** | `analyze-codebase.py` | Analyze project, generate rules |
| **PreToolUse** | `keyword-amplifier.py` | Detect mode keywords, inject context |
| **PostToolUse** | `comment-checker.py` | Warn if comment ratio > 25% |

### Keyword Amplification

Use natural language triggers for enhanced behavior:

| Keyword | Effect |
|---------|--------|
| `ultrawork` | Maximum focus mode with comprehensive analysis |
| `deep work` | Single-task focus, minimize context switching |
| `think deeply` | Extended reasoning with multiple perspectives |
| `search` / `find` | Multi-strategy search approach |
| `analyze` | Structured analytical framework |
| `investigate` | Root cause analysis protocol |
| `quick` / `fast` | Efficient execution, minimal overhead |

Example:
```
"ultrawork: implement a secure authentication system"
```

---

## How It Works

### Session Lifecycle

```
1. SESSION START
   └── Hook: analyze-codebase.py
       ├── Detect project type
       ├── Analyze structure
       └── Generate/update .claude/rules/

2. TOOL USE
   ├── PreToolUse Hook: keyword-amplifier.py
   │   └── Inject mode-specific context
   │
   ├── [Tool Execution]
   │
   └── PostToolUse Hook: comment-checker.py
       └── Validate code quality
```

### Auto-Generated Rules

On session start, CDF analyzes your codebase and generates:

```
.claude/rules/
├── architecture.md   # Directory structure, components, data flow
├── tech-stack.md     # Languages, frameworks, libraries
├── patterns.md       # Code conventions, patterns
└── commands.md       # Setup, build, test, run commands
```

These rules are automatically loaded as context for Claude.

---

## Plugin Structure

```
claude-dev-framework/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata (name: "cdf", version: "1.3.0")
│
├── commands/                 # 22 slash commands
│   ├── INDEX.md              # Categorized command reference
│   ├── analyze.md
│   ├── brainstorm.md
│   ├── build.md
│   └── ... (19 more)
│
├── agents/                   # 19 agent personas
│   ├── INDEX.md              # Categorized agent reference
│   ├── system-architect.md
│   ├── backend-architect.md
│   └── ... (17 more)
│
├── skills/                   # 6 auto-invoked skills
│   ├── rules-generator/
│   │   └── SKILL.md
│   ├── claudemd-generator/
│   │   └── SKILL.md
│   ├── context-saver/
│   │   └── SKILL.md
│   ├── external-memory/
│   │   └── SKILL.md
│   ├── intent-gate/
│   │   └── SKILL.md
│   └── failure-recovery/
│       └── SKILL.md
│
├── hooks/
│   └── hooks.json            # 3 lifecycle hooks
│
├── scripts/                  # Hook implementations & utilities
│   ├── analyze-codebase.py   # SessionStart hook
│   ├── keyword-amplifier.py  # PreToolUse hook
│   ├── comment-checker.py    # PostToolUse hook
│   └── setup-agents.sh       # Agent symlink setup
│
└── README.md                 # This file
```

---

## Configuration

### Plugin Settings

The plugin includes default permissions in `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "WebFetch(domain:raw.githubusercontent.com)",
      "WebFetch(domain:api.github.com)"
    ]
  }
}
```

### Customizing Hooks

Edit `hooks/hooks.json` to modify hook behavior:

```json
{
  "hooks": {
    "SessionStart": [...],
    "PreToolUse": [...],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",  // Only run on these tools
        "hooks": [...]
      }
    ],
    "Stop": [...]
  }
}
```

### Environment Variables

Hooks use `$CLAUDE_PLUGIN_ROOT` to reference plugin-relative paths:

```json
{
  "command": "python3 \"$CLAUDE_PLUGIN_ROOT/scripts/analyze-codebase.py\""
}
```

---

## Troubleshooting

### Plugin Not Loading

```bash
# Verify installation
claude plugin marketplace list

# Check if plugin is recognized
/plugin list

# Reinstall if needed
claude plugin marketplace remove claude-dev-framework
claude plugin marketplace add drag88/claude-dev-framework
/plugin install cdf@claude-dev-framework
```

### Commands Not Found

```bash
# List available commands
/cdf:help

# Check command namespace
/plugin list  # Should show "cdf" namespace
```

### Hooks Not Running

```bash
# Check hooks.json syntax
cat hooks/hooks.json | python3 -m json.tool

# Verify script permissions
chmod +x scripts/*.sh
```

### Rules Not Generating

```bash
# Manually trigger analysis
/cdf:rules generate

# Check Python availability
python3 --version
```

---

## Requirements

- **Claude Code CLI** - Latest version recommended
- **Python 3.x** - For hook scripts
- **Bash** - For shell scripts (macOS/Linux)

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `claude --plugin-dir ./claude-dev-framework`
5. Submit a pull request

---

## License

MIT

---

## Resources

- [Claude Code Documentation](https://code.claude.com/docs)
- [Plugin Development Guide](https://code.claude.com/docs/en/plugins)
- [agents/INDEX.md](agents/INDEX.md) - Full agent reference
- [commands/INDEX.md](commands/INDEX.md) - Full command reference
