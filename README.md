# CDF (Claude Dev Framework)

A development framework plugin for Claude Code that provides commands, agent personas, auto-invoked skills, and lifecycle hooks -- turning Claude into a structured, opinionated development assistant.

---

## Installation

### From Source (Recommended for Development)

```bash
git clone https://github.com/drag88/claude-dev-framework.git
claude --plugin-dir ./claude-dev-framework
```

### From Marketplace

```bash
# Via CLI (outside Claude Code)
claude plugin marketplace add drag88/claude-dev-framework

# Inside Claude Code
/plugin install cdf@claude-dev-framework
```

### Verify Installation

```bash
/cdf:rules generate
```

Agents are automatically symlinked to `~/.claude/agents/` on first session, making them accessible globally via `@agent-name`.

---

## Quick Start

### Automatic Project Analysis

When you start a session, CDF analyzes your codebase and generates `.claude/rules/` documentation automatically.

### Example Workflows

```bash
# Implement a feature
/cdf:implement "add user authentication"

# Research a topic
/cdf:research "best practices for React state management"

# Debug an issue
/cdf:troubleshoot "API returning 500 errors"

# Run tests with analysis
/cdf:test
```

### Task Orchestration

```bash
# Break down and delegate complex tasks
/cdf:task --breakdown "design microservices architecture"

# Full workflow: brainstorm -> docs -> implement -> verify
/cdf:flow "add payment processing"
```

---

## Architecture

### Commands

Slash commands prefixed with `/cdf:` covering development, analysis, planning, and orchestration. Core commands include `implement`, `test`, `tdd`, `git`, `analyze`, `research`, `troubleshoot`, `design`, `task`, and `flow`.

See [commands/README.md](commands/README.md) for the complete reference.

### Agents

Specialized personas that activate automatically based on task context. Covers architecture, research, quality, testing, and communication domains.

See [agents/README.md](agents/README.md) for the complete reference.

### Skills

Context-triggered behaviors that activate automatically -- rules generation, intent classification, coding standards enforcement, failure recovery, TDD workflow, visual explanations, and more.

See [skills/](skills/) for details.

### Hooks

Lifecycle hooks that run at session start, before/after tool use, and on stop. They handle codebase analysis, context injection, code quality checks, and session memory.

Configuration: `hooks/hooks.json`

### Rules Templates

Pre-built rule templates for common project types (ML, frontend, backend, data-eng, mobile, CLI, monorepo, infra) and best practices (security, testing, git workflow, performance, coding style).

Located in `rules-templates/`. Auto-applied via `/cdf:rules generate`.

---

## Reference

| Resource | Description |
|----------|-------------|
| [commands/README.md](commands/README.md) | Complete command reference |
| [agents/README.md](agents/README.md) | Agent personas and activation |
| [skills/](skills/) | Skill definitions and triggers |
| [rules-templates/](rules-templates/) | Rule templates by project type |
| [mcp-configs/](mcp-configs/) | MCP server configuration templates |
| [docs/solutions/](docs/solutions/) | Institutional knowledge from solved problems |

---

## Configuration

### Hooks

Edit `hooks/hooks.json` to modify lifecycle hook behavior. Hooks use `$CLAUDE_PLUGIN_ROOT` for plugin-relative paths.

### MCP Servers

Copy `mcp-configs/mcp-servers.template.json` to `.mcp/settings.json` and configure credentials. Pre-configured templates available for GitHub, Supabase, Vercel, Cloudflare, PostgreSQL, Redis, and Context7.

### Environment

| Variable | Purpose |
|----------|---------|
| `$CLAUDE_PLUGIN_ROOT` | Plugin root directory (used by hooks) |

---

## Troubleshooting

### Plugin Not Loading

```bash
claude plugin marketplace list    # Verify installation
/plugin list                      # Check if recognized
```

### Hooks Not Running

```bash
python3 -m json.tool hooks/hooks.json   # Validate syntax
chmod +x scripts/*.sh                    # Fix permissions
```

### Rules Not Generating

```bash
/cdf:rules generate    # Manually trigger
python3 --version      # Verify Python 3 available
```

---

## Requirements

- **Claude Code CLI** - Latest version
- **Python 3.x** - For hook scripts
- **Bash** - For shell scripts (macOS/Linux)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test with `claude --plugin-dir ./claude-dev-framework`
4. Submit a pull request

## License

MIT
