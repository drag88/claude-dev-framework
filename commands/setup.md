---
description: "View CDF setup information and available agents"
---

# /cdf:setup - Setup Information

> View CDF plugin configuration and available agents.

## Overview

CDF agents are automatically available from the plugin - no manual setup required. This command displays setup information and lists available agents.

## Usage

```bash
/cdf:setup
```

## Available Agents

When the CDF plugin is enabled, these agents are available via `@agent-name` syntax:

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

## Example Usage

```bash
@backend-architect "design an API for user management"
@system-architect "review this architecture"
@security-engineer "audit authentication flow"
@performance-engineer "optimize database queries"
```

## Troubleshooting

### Agents not recognized

1. Verify the CDF plugin is enabled:
   ```bash
   /plugin list
   ```

2. Restart Claude Code session

3. Browse available agents:
   ```bash
   /agents
   ```

## Plugin Location

The plugin is installed at:
```
~/.claude/plugins/marketplaces/claude-dev-framework/
```
