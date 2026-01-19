---
description: "Set up CDF agents for @agent-name usage"
---

# /cdf:setup - Agent Setup

> Configure CDF agent personas for use with @agent-name syntax.

## Overview

Claude Code looks for agents in `~/.claude/agents/` (global) or `.claude/agents/` (project-level). Since CDF installs agents in the plugin directory, this command creates symlinks to make them accessible.

## Usage

```bash
/cdf:setup
```

## What It Does

1. Locates the CDF plugin installation directory
2. Creates `~/.claude/agents/` if it doesn't exist
3. Symlinks all agent `.md` files from `cdf/agents/` to `~/.claude/agents/`
4. Reports created, updated, and skipped symlinks

## After Setup

You can use CDF agents directly:

```bash
@backend-architect "design an API for user management"
@system-architect "review this architecture"
@security-engineer "audit authentication flow"
@performance-engineer "optimize database queries"
```

## Available Agents

After setup, these agents become available:

| Agent | Domain |
|-------|--------|
| `@backend-architect` | APIs, databases, server systems |
| `@business-panel-experts` | Business strategy analysis |
| `@codebase-navigator` | Code search and dependency tracing |
| `@deep-research-agent` | Multi-source research |
| `@devops-architect` | CI/CD, infrastructure |
| `@frontend-architect` | UI/UX, components |
| `@learning-guide` | Teaching through examples |
| `@library-researcher` | Open-source library evaluation |
| `@media-interpreter` | PDFs, images, diagrams |
| `@performance-engineer` | Optimization and profiling |
| `@python-expert` | Python-specific guidance |
| `@quality-engineer` | Testing strategies and QA |
| `@refactoring-expert` | Code improvement |
| `@requirements-analyst` | Requirements gathering |
| `@root-cause-analyst` | Complex debugging |
| `@security-engineer` | Security audits |
| `@socratic-mentor` | Learning through questions |
| `@system-architect` | High-level system design |
| `@technical-writer` | Documentation |

## Manual Setup

If needed, you can run the setup script directly:

```bash
# Via plugin environment variable
bash "$CLAUDE_PLUGIN_ROOT/scripts/setup-agents.sh"

# Or from known install location
bash ~/.claude/plugins/marketplaces/drag88-plugins/cdf/scripts/setup-agents.sh
```

## Troubleshooting

### Agents still not recognized

1. Verify symlinks exist:
   ```bash
   ls -la ~/.claude/agents/
   ```

2. Restart Claude Code session after setup

3. Check that agent files have `.md` extension

### Permission issues

Ensure the script has execute permission:
```bash
chmod +x "$CLAUDE_PLUGIN_ROOT/scripts/setup-agents.sh"
```

## Boundaries

**Will:**
- Create symlinks for agent files
- Report setup status
- Create `~/.claude/agents/` directory if missing

**Will Not:**
- Copy files (uses symlinks to stay in sync)
- Overwrite existing non-symlink files
- Modify plugin installation
