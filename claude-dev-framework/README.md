# CDF (Claude Dev Framework)

Development framework plugin for Claude Code with 29 commands + 16 agent personas.

## Installation

```bash
claude plugins:add aswin-plugins/cdf
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

### Agent Personas

16 specialized agents for domain expertise. Invoke with `/cdf:[agent-name]`:

| Agent | Use Case |
|-------|----------|
| `/cdf:backend-architect` | APIs, databases, server-side |
| `/cdf:frontend-architect` | UI, UX, components |
| `/cdf:system-architect` | Full-stack, distributed systems |
| `/cdf:devops-architect` | CI/CD, infrastructure |
| `/cdf:python-expert` | Python best practices |
| `/cdf:deep-research-agent` | Web research, synthesis |
| `/cdf:requirements-analyst` | PRDs, specifications |
| `/cdf:root-cause-analyst` | Debugging, investigation |
| `/cdf:technical-writer` | Documentation |
| `/cdf:socratic-mentor` | Teaching via questioning |
| `/cdf:learning-guide` | Code explanation |
| `/cdf:quality-engineer` | Testing strategies |
| `/cdf:performance-engineer` | Optimization |
| `/cdf:security-engineer` | Security audits |
| `/cdf:refactoring-expert` | Code improvement |
| `/cdf:business-panel-experts` | Strategy panel |

**Chaining**: Combine agents with `/cdf:backend-architect,security-engineer`

## How It Works

1. **Session Start**: Hook runs `analyze-codebase.py` to check project state
2. **Rules Detection**: If no `.claude/rules/`, triggers automatic generation
3. **Context Loading**: Rules are loaded as context for Claude
4. **Command Execution**: Use slash commands for specialized workflows

## File Structure

```
cdf/
├── .claude-plugin/
│   └── plugin.json          # Plugin metadata
├── commands/
│   ├── agents/              # 16 agent personas
│   ├── sc/                  # 25 specialized commands
│   ├── dev-docs.md
│   ├── dev-docs-update.md
│   ├── generate-claude-md.md
│   └── regenerate-rules.md
├── hooks/
│   └── hooks.json           # Session start hook
├── scripts/
│   └── analyze-codebase.py  # Codebase analysis
└── skills/
    ├── claudemd-generator/
    ├── context-saver/
    └── rules-generator/
```

## Requirements

- Claude Code CLI
- Python 3.x (for hooks)

## License

MIT
