# CDF (Claude Dev Framework)

A comprehensive development framework plugin for Claude Code featuring **29 commands**, **21 agent personas**, **19 skills**, and **13 lifecycle hooks**.

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
- [Agents](#agents)
- [Skills](#skills)
- [Hooks](#hooks)
- [Context Modes](#context-modes)
- [Rules Templates](#rules-templates)
- [MCP Configurations](#mcp-configurations)
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
| `/cdf:tdd` | Test-Driven Development with RED-GREEN-REFACTOR workflow |
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
| `/cdf:e2e` | End-to-end testing with Playwright patterns |

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

### Workflow Orchestration

| Command | Description |
|---------|-------------|
| `/cdf:flow` | Unified workflow: brainstorm → docs → implement → verify → compound |
| `/cdf:compound` | Capture institutional knowledge from solved problems |
| `/cdf:deepen` | Parallel agent saturation for comprehensive analysis |

### Utilities

| Command | Description |
|---------|-------------|
| `/cdf:help` | List all available commands |
| `/cdf:docs` | Documentation management |
| `/cdf:rules` | Generate and manage project rules |
| `/cdf:session` | Session management and context handling |
| `/cdf:select-tool` | Intelligent MCP tool selection |
| `/cdf:verify` | Pre-PR quality verification (build, types, lint, tests) |
| `/cdf:learn` | Continuous learning and pattern extraction |

---

## Agents

CDF includes 21 specialized agent personas. See [agents/INDEX.md](agents/INDEX.md) for the complete reference.

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

### Testing Specialists

| Agent | Use Case |
|-------|----------|
| `tdd-guide` | Test-Driven Development enforcement |
| `e2e-specialist` | End-to-end testing with Playwright |

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

### Core Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| **rules-generator** | Missing `.claude/rules/` | Auto-generates project documentation |
| **claudemd-generator** | After rules generation | Creates `CLAUDE.generated.md` |
| **context-saver** | Context approaching 75%+ | Saves session progress with strategic compaction |
| **external-memory** | Complex tasks (50+ tool calls) | File-based working memory |
| **intent-gate** | Every request | Classifies request type for optimal handling |
| **failure-recovery** | 3 consecutive failures | STOP → REVERT → DOCUMENT → CONSULT |

### Development Pattern Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| **coding-standards** | Code implementation | Enforces code quality, naming, immutability patterns |
| **backend-patterns** | Backend development | API design, database, authentication patterns |
| **frontend-patterns** | Frontend development | React patterns, hooks, state management |
| **tdd-workflow** | TDD mode | RED-GREEN-REFACTOR cycle enforcement |
| **e2e-patterns** | E2E testing | Playwright patterns, Page Object Model |
| **continuous-learning** | Session end | Pattern extraction and persistence |

### Specialized Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| **frontend-slides** | HTML presentation tasks | Zero-dependency HTML presentations with style presets and PPT conversion |
| **pptx** | Presentation tasks | PowerPoint creation and editing |
| **skill-creator** | Creating skills | Guide for building new skills |
| **social-writing** | LinkedIn/Twitter posts | Authentic social media content |
| **starhub-presentation** | StarHub decks | Executive presentations with templates |
| **frontend-design** | UI/UX design tasks | Design system guidance and component patterns |
| **project-memory** | Session persistence | Cross-session project memory and context |

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

CDF uses 13 lifecycle hooks for automation:

| Event | Script | Purpose |
|-------|--------|---------|
| **SessionStart** | `analyze-codebase.py` | Analyze project, generate rules |
| **SessionStart** | `memory-init.py` | Initialize session memory context |
| **PreToolUse** | `keyword-amplifier.py` | Inject mode-specific context based on keywords |
| **PreToolUse** | `git-push-review.py` | Remind to review before `git push` |
| **PostToolUse** | `console-log-detector.py` | Warn on debugging statements in .ts/.tsx |
| **PostToolUse** | `comment-checker.py` | Warn if comment ratio > 25% |
| **PostToolUse** | `memory-logger.py` | Log file changes to session memory |
| **PostToolUse** | `flow-checkpoint.py` | Auto-checkpoint every 20 tool calls during flow |
| **PostToolUse** | `flow-verify-gate.py` | Track test results during flow verify phase |
| **Stop** | `session-end.py` | Persist session state on exit |
| **Stop** | `memory-summarize.py` | Summarize session memory on exit |
| **Stop** | `flow-session-save.py` | Save flow state with resume instructions |
| **Stop** | `task-completeness-check.sh` | Verify all tasks completed before stop |

---

## Context Modes

CDF supports behavioral modes that adjust Claude's focus and approach.

| Mode | Behavior | Use Case |
|------|----------|----------|
| **dev** | Implementation-focused, code-first | Building features |
| **review** | Quality assessment, thorough checks | Code reviews, audits |
| **research** | Exploration, broad investigation | Learning, research |

Activate with session command:
```bash
/cdf:session load --mode dev
```

Context files located in `contexts/` directory.

---

## Rules Templates

Pre-built rule templates for common project standards. Copy to `.claude/rules/` and customize.

| Template | Purpose |
|----------|---------|
### Best Practice Templates

| Template | Purpose |
|----------|---------|
| `security.md` | OWASP guidelines, secrets handling, input validation |
| `testing.md` | 80% coverage requirement, TDD enforcement |
| `git-workflow.md` | Conventional commits, PR workflow |
| `performance.md` | Model selection, context management |
| `coding-style.md` | Immutability patterns, file size limits |

### Project-Type Templates

| Template | Purpose |
|----------|---------|
| `ml-rules.md` | ML/Data Science conventions (experiments, data contracts) |
| `frontend-rules.md` | Frontend conventions (components, accessibility) |
| `backend-rules.md` | Backend API conventions (endpoints, database) |
| `data-eng-rules.md` | Data engineering (pipelines, data quality) |
| `mobile-rules.md` | Mobile development (platform rules, navigation) |
| `cli-rules.md` | CLI/Library conventions (public API, versioning) |
| `monorepo-rules.md` | Monorepo management (workspaces, change impact) |
| `infra-rules.md` | Infrastructure as code (IaC, security baseline) |
| `soul-template.md` | Project soul/personality template |
| `agents-template.md` | Cross-tool AGENTS.md template |

Generate with:
```bash
/cdf:rules generate  # Auto-detects project type and applies relevant templates
```

Templates located in `rules-templates/` directory.

---

## MCP Configurations

Pre-configured MCP server templates for common integrations.

| Server | Purpose |
|--------|---------|
| GitHub | Repository management |
| Supabase | Database and auth |
| Vercel | Deployment |
| Cloudflare | Workers, KV, R2 |
| PostgreSQL | Database access |
| Redis | Cache and data store |
| Context7 | Library documentation |
| Memory | Persistent memory |

Copy `mcp-configs/mcp-servers.template.json` to `.mcp/settings.json` and configure your credentials.

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

### Command Enforcement Pattern

All workflow commands (flow, tdd, spawn, task, deepen, compound, session) use a **MANDATORY FIRST ACTIONS** pattern to ensure Claude doesn't skip critical steps:

```markdown
## MANDATORY FIRST ACTIONS (DO NOT SKIP)

**BEFORE doing ANYTHING else**, you MUST:

### Step 1: Create State File
mkdir -p dev/active/[task-slug]
Write state file with YAML frontmatter...

### Step 2: [Required Action]
...

CRITICAL ANTI-PATTERNS - DO NOT:
- Skip state file creation
- Use alternative paths (.claude/plans/ instead of dev/active/)
- Proceed without completing mandatory steps
```

This pattern prevents Claude from taking shortcuts or using built-in behaviors that bypass the workflow.

### Auto-Generated Rules

On session start, CDF analyzes your codebase and generates:

```
.claude/rules/
├── architecture.md   # Directory structure, components, data flow
├── tech-stack.md     # Languages, frameworks, libraries
├── patterns.md       # Code conventions, patterns
├── commands.md       # Setup, build, test, run commands
└── soul.md           # Project personality, values, boundaries

AGENTS.md             # Cross-tool AI agent compatibility (root)
```

Project type is auto-detected (ML, frontend, backend, data-eng, mobile, CLI, monorepo, infra) and type-specific rule files are generated alongside the standard ones. A root `AGENTS.md` is also generated for cross-tool compatibility with Cursor, Windsurf, etc.

These rules are automatically loaded as context for Claude.

---

## Plugin Structure

```
claude-dev-framework/
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata (name: "cdf", version: "1.9.0")
│
├── commands/                 # 29 slash commands
│   ├── README.md             # Categorized command reference
│   ├── implement.md, build.md, test.md, tdd.md, ...
│   └── verify.md, learn.md, e2e.md (new)
│
├── agents/                   # 21 agent personas
│   ├── README.md             # Categorized agent reference
│   ├── system-architect.md, backend-architect.md, ...
│   └── tdd-guide.md, e2e-specialist.md (new)
│
├── skills/                   # 19 auto-invoked skills
│   ├── rules-generator/, claudemd-generator/, ...
│   ├── coding-standards/, backend-patterns/, frontend-patterns/ (new)
│   ├── tdd-workflow/, e2e-patterns/, continuous-learning/ (new)
│   ├── frontend-slides/ (HTML presentations with style presets)
│   └── pptx/, skill-creator/, social-writing/, starhub-presentation/
│
├── contexts/                 # Behavioral modes (new)
│   ├── dev.md                # Implementation focus
│   ├── review.md             # Quality assessment focus
│   └── research.md           # Exploration focus
│
├── rules-templates/          # 15 rule templates (5 best-practice + 10 project-type)
│   ├── security.md, testing.md, git-workflow.md, performance.md, coding-style.md
│   ├── ml-rules.md, frontend-rules.md, backend-rules.md, data-eng-rules.md
│   ├── mobile-rules.md, cli-rules.md, monorepo-rules.md, infra-rules.md
│   └── soul-template.md, agents-template.md
│
├── mcp-configs/              # MCP server templates (new)
│   └── mcp-servers.template.json
│
├── docs/
│   └── solutions/            # Institutional knowledge from /cdf:compound
│       ├── build-errors/
│       ├── runtime-errors/
│       └── ...
│
├── hooks/
│   └── hooks.json            # 13 lifecycle hooks
│
├── scripts/
│   ├── analyze-codebase.py   # SessionStart hook
│   ├── hooks/                # Additional hook scripts (new)
│   │   ├── git-push-review.py
│   │   ├── console-log-detector.py
│   │   └── session-end.py
│   └── lib/                  # Shared utilities (new)
│       └── utils.py
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
