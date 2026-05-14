# CDF (Claude Dev Framework)

A host-adaptable development framework for AI coding agents. CDF provides commands, agent personas, auto-invoked skills, rules, and lifecycle hooks -- turning Claude Code, Codex, and other coding agents into structured, opinionated development assistants.

---

## Installation

### Host Support

| Host | Status | Entry Points |
|------|--------|--------------|
| Claude Code | Packaged adapter | `.claude-plugin/`, `/cdf:*` commands, `.claude/rules/`, `hooks/hooks.json`, `CLAUDE.md` |
| Codex | Packaged adapter | `.codex-plugin/`, `.agents/plugins/marketplace.json`, `AGENTS.md`, Codex skills, `/cdf:*` command prompts |

See [docs/HOSTS.md](docs/HOSTS.md) for the adapter model and Codex rollout path.

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

### Codex

CDF also ships Codex metadata. From this checkout:

```bash
codex plugin marketplace add /path/to/claude-dev-framework
```

Then enable the plugin in `~/.codex/config.toml`:

```toml
[plugins."cdf@claude-dev-framework"]
enabled = true
```

Restart Codex after changing plugin configuration.

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

# Multi-step work: write a clear prompt and let 4.7 plan natively
# (the /cdf:flow and /cdf:workflow orchestrators were removed in the leanness pass —
#  Opus 4.7 with xhigh effort plans these workflows from a clear prompt)
```

---

## Cross-Machine Setup

CDF is designed to travel cleanly across machines. Three tiers of state:

| Tier | Location | Travels via |
|------|----------|-------------|
| **Repo** | `.claude/memory/`, `.claude/rules/`, project `CLAUDE.md` | Git (committed with the project) |
| **User** | `~/.claude/skills/`, `~/.claude/agents/`, `~/.claude/CLAUDE.md`, auto-memory | Sync the CDF repo + symlinks (see Bootstrap) |
| **Machine-local** | `.env`, MCP server credentials, `~/.cdf-logs/` | Never travels — set up per machine |

### Bootstrap on a new machine

```bash
# 1. Install Claude Code CLI (machine-specific)
# Follow https://docs.claude.com/en/docs/claude-code/installation

# 2. Clone CDF
git clone https://github.com/drag88/claude-dev-framework.git ~/code/claude-dev-framework
cd ~/code/claude-dev-framework

# 3. Pull latest skills + adopt any global ones
./scripts/adopt-skills.sh

# 4. Activate CDF as a plugin
claude --plugin-dir .

# 5. Configure MCP servers (machine-local)
cp mcp-configs/mcp-servers.template.json .mcp/settings.json
# edit .mcp/settings.json with your credentials

# 6. Verify
/cdf:rules generate     # in any project to confirm CDF is loaded
```

### Versioning and rollback

CDF version is in `.claude-plugin/plugin.json`. To pin a specific version on a machine:

```bash
git checkout v1.12.0    # or whatever version
```

Third-party skills are tracked in `skills-lock.json` with computed hashes. Update with:

```bash
npx skills update --frozen-lockfile
```

---

## Architecture

### Host-Neutral Core

CDF's durable core is the methodology in `commands/`, `agents/`, `skills/`, `rules-templates/`, and `docs/`. Host adapters load that core into a specific agent runtime. Claude Code gets slash commands and hooks; Codex gets `.codex-plugin/`, `AGENTS.md` routing, skills, agents, and explicit command prompts. Do not put host-specific assumptions in core command or skill behavior unless the file is clearly adapter-specific.

### Commands

Slash commands prefixed with `/cdf:` covering development, analysis, planning, review, and quality verification. Core commands include `implement`, `test`, `tdd`, `git`, `analyze`, `research`, `troubleshoot`, `design`, `plan-review`, `task`, `verify`, and `ship`.

See [commands/README.md](commands/README.md) for the complete reference.

### Agents

Real-expertise agents that you invoke when fan-out or specialized investigation is warranted. Covers research, quality, testing, requirements, and business strategy. Persona stubs (backend, frontend, devops, etc.) were removed in the leanness pass — Opus 4.7 plays those roles from the Role line in `CLAUDE.md` plus `xhigh` effort.

See [agents/README.md](agents/README.md) for the complete reference.

### Skills

Context-triggered behaviors that activate automatically — rules generation, coding standards enforcement, failure recovery, TDD workflow, visual explanations, pattern guidance for backend/frontend/E2E, and more.

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
| [docs/HOSTS.md](docs/HOSTS.md) | Host adapter model for Claude Code, Codex, and future runtimes |
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
