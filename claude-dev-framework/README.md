# Claude Dev Framework

A comprehensive development framework plugin for Claude Code with automatic rules generation, task management, and 29 specialized commands.

## Installation

```bash
claude plugins:add aswin-plugins/claude-dev-framework
```

## Features

### Auto-Generated Project Rules

On session start, the plugin analyzes your codebase and automatically generates `.claude/rules/` documentation:

- `architecture.md` - Directory structure, components, data flow
- `tech-stack.md` - Languages, frameworks, libraries
- `patterns.md` - Code conventions, architectural patterns
- `commands.md` - Setup, build, test, run commands

### Commands

#### Core Commands

| Command | Description |
|---------|-------------|
| `/dev-docs` | Create strategic plans with structured task breakdown |
| `/dev-docs-update` | Update existing dev documentation |
| `/regenerate-rules` | Refresh `.claude/rules/` documentation |
| `/generate-claude-md` | Generate `CLAUDE.generated.md` from rules |

#### SC Commands (`/sc:*`)

Specialized commands for different development workflows:

| Command | Description |
|---------|-------------|
| `/sc:analyze` | Code analysis across quality, security, performance |
| `/sc:brainstorm` | Requirements discovery through Socratic dialogue |
| `/sc:build` | Build projects with error handling |
| `/sc:business-panel` | Multi-expert business strategy analysis |
| `/sc:cleanup` | Remove dead code, optimize structure |
| `/sc:design` | Design system architecture and APIs |
| `/sc:document` | Generate component/API documentation |
| `/sc:estimate` | Development effort estimation |
| `/sc:explain` | Clear explanations of code and concepts |
| `/sc:git` | Git operations with intelligent commits |
| `/sc:help` | List all available commands |
| `/sc:implement` | Feature implementation with MCP integration |
| `/sc:improve` | Code quality and performance improvements |
| `/sc:index` | Generate project knowledge base |
| `/sc:load` | Load project context for session |
| `/sc:reflect` | Task reflection and validation |
| `/sc:research` | Deep web research with adaptive strategies |
| `/sc:save` | Persist session context |
| `/sc:select-tool` | Intelligent MCP tool selection |
| `/sc:spawn` | Task orchestration with delegation |
| `/sc:spec-panel` | Multi-expert specification review |
| `/sc:task` | Complex task workflow management |
| `/sc:test` | Execute tests with coverage analysis |
| `/sc:troubleshoot` | Diagnose and resolve issues |
| `/sc:workflow` | Generate implementation workflows from PRDs |

### Skills

Auto-activated behaviors based on context:

- **rules-generator** - Auto-generates rules when `.claude/rules/` missing
- **claudemd-generator** - Creates `CLAUDE.generated.md` from rules
- **context-saver** - Preserves session context

## How It Works

1. **Session Start**: Hook runs `analyze-codebase.py` to check project state
2. **Rules Detection**: If no `.claude/rules/`, triggers automatic generation
3. **Context Loading**: Rules are loaded as context for Claude
4. **Command Execution**: Use slash commands for specialized workflows

## File Structure

```
claude-dev-framework/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/
│   ├── dev-docs.md          # Strategic planning
│   ├── dev-docs-update.md   # Update documentation
│   ├── generate-claude-md.md # Generate CLAUDE.md
│   ├── regenerate-rules.md  # Refresh rules
│   └── sc/                  # 25 specialized commands
├── hooks/
│   └── hooks.json           # Session start hook
├── scripts/
│   └── analyze-codebase.py  # Codebase analysis
└── skills/
    ├── claudemd-generator/  # Auto CLAUDE.md generation
    ├── context-saver/       # Context preservation
    └── rules-generator/     # Auto rules generation
```

## Requirements

- Claude Code CLI
- Python 3.x (for hooks)

## License

MIT
