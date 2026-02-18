# Architecture

## Project Overview

CDF (Claude Dev Framework) is a comprehensive plugin for Claude Code that provides intelligent development assistance through modular components: commands, agents, skills, and hooks.

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `commands/` | 29 slash command definitions (markdown with YAML frontmatter) |
| `agents/` | 21 agent persona definitions for specialized expertise |
| `skills/` | 19 auto-invoked skills with trigger-based activation |
| `contexts/` | Behavioral context modes (dev/review/research) |
| `hooks/` | Lifecycle hook configuration (JSON) |
| `scripts/` | Hook implementation scripts (Python/Bash) |
| `rules-templates/` | 16 rule templates: 5 best-practice + 11 project-type/generation-specific (ML, frontend, backend, data-eng, mobile, CLI, monorepo, infra, soul, agents, workflow) |
| `mcp-configs/` | MCP server configuration templates |
| `.claude-plugin/` | Plugin metadata (plugin.json, marketplace.json) |
| `.claude/` | Plugin settings and permissions |

## Key Files

| File | Role |
|------|------|
| `.claude-plugin/plugin.json` | Plugin metadata and version |
| `hooks/hooks.json` | Lifecycle hook definitions |
| `scripts/analyze-codebase.py` | SessionStart hook - codebase analysis |
| `scripts/keyword-amplifier.py` | PreToolUse hook - context injection |
| `scripts/lib/utils.py` | Shared utility functions |
| `scripts/hooks/memory-init.py` | SessionStart hook - memory initialization and context injection |
| `scripts/hooks/memory-logger.py` | PostToolUse hook - logs file changes to daily memory |
| `scripts/hooks/memory-summarize.py` | Stop hook - session summarization and learnings propagation |

## Component Relationships

```
User Request
    ↓
Intent Gate (skill) → Classifies request type
    ↓
Command Router → Loads command definition
    ↓
Agent Activation → Selects relevant personas
    ↓
Skill Activation → Triggers context-aware behaviors
    ↓
Hook Execution → Pre/Post tool use hooks
    ↓
MCP Integration → External tool coordination
```

## Data Flow

1. **SessionStart**: `analyze-codebase.py` analyzes project, generates rules
2. **Request Processing**: Intent classified, command loaded, agents/skills activated
3. **Tool Execution**: PreToolUse hooks inject context, PostToolUse hooks validate
4. **Session End**: Stop hooks persist state, verify task completion

## Architectural Patterns

- **Metadata-Driven**: YAML frontmatter defines command/agent behavior
- **Trigger-Based Skills**: Skills activate on conditions (missing files, thresholds, failures)
- **Composable Agents**: Multiple agents can collaborate on tasks
- **Hook Lifecycle**: Pre/Post hooks for validation and enhancement
- **External Memory**: File-based memory (`dev/memory/`) for complex tasks

## Extension Points

- Add commands in `commands/*.md`
- Add agents in `agents/*.md`
- Add skills in `skills/*/SKILL.md`
- Add hooks in `hooks/hooks.json`
- Add context modes in `contexts/*.md`
