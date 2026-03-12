# Architecture

## Bird's Eye View

CDF (Claude Dev Framework) is a Claude Code plugin that transforms Claude into a structured, opinionated development assistant. It provides modular components — commands, agents, skills, and hooks — that enforce workflows, inject specialized expertise, and maintain codebase memory across sessions.

## Codemap

| Directory | Purpose |
|-----------|---------|
| `commands/` | 20 slash command definitions (markdown + YAML frontmatter). Each file is a complete behavioral spec. |
| `agents/` | 22 agent persona definitions. Activated by `/cdf:task` or automatically via task context. |
| `skills/` | 24 auto-invoked skill directories (`skills/*/SKILL.md`). Trigger-based, no explicit invocation. |
| `contexts/` | 3 behavioral context modes (dev/review/research) with quality thresholds. |
| `hooks/` | Lifecycle hook configuration (`hooks.json`). |
| `scripts/` | Hook implementation scripts (5 Python + 1 Bash + 1 shared library). |
| `rules-templates/` | 14 rule templates: 5 best-practice + 8 project-type + 1 meta (workflow). |
| `mcp-configs/` | MCP server configuration templates (7 pre-configured servers). |
| `.claude-plugin/` | Plugin metadata (`plugin.json` v1.12.0). |
| `.claude/` | Plugin settings, permissions, rules, and runtime memory. |
| `docs/` | Institutional knowledge and solved problem references. |

## Key Files

| File | Role |
|------|------|
| `.claude-plugin/plugin.json` | Plugin metadata, version (1.12.0), component counts |
| `hooks/hooks.json` | Lifecycle hook definitions — 7 hooks across 4 event types |
| `scripts/analyze-codebase.py` | SessionStart hook — project analysis and rule generation |
| `scripts/hooks/session-context.py` | SessionStart hook — injects git history + auto-memory context |
| `scripts/keyword-amplifier.py` | PreToolUse hook — mode detection and context injection |
| `scripts/lib/utils.py` | Shared utility functions used by all hook scripts |

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

1. **SessionStart**: `analyze-codebase.py` analyzes project and generates rules; `session-context.py` injects git history + auto-memory context (60s timeout each)
2. **Request Processing**: Intent classified, command loaded, agents/skills activated
3. **PreToolUse**: `keyword-amplifier.py` injects mode context; `git-push-review.py` guards pushes
4. **PostToolUse**: `console-log-detector.py`, `comment-checker.py` validate code quality
5. **Stop**: `task-completeness-check.sh` verifies completion

## Cross-Cutting Concerns

- **Session Context**: `session-context.py` injects recent git history and auto-memory at session start. No CDF-owned storage.
- **Mode Amplification**: `keyword-amplifier.py` detects keywords (ultrawork, deep work, investigate) and injects behavioral context into all tool calls.
- **Quality Gates**: `comment-checker.py` (35% threshold), `console-log-detector.py` (debug statements), context modes set quality thresholds.
- **Error Recovery**: `failure-recovery` skill activates after 3 consecutive failures (STOP → REVERT → DOCUMENT → CONSULT).

## Architectural Invariants

- Hook scripts use only Python stdlib — no external dependencies
- Commands, agents, and skills are pure markdown — no executable code
- `hooks/hooks.json` is the single source of truth for lifecycle configuration
- All hook scripts return JSON to stdout for Claude injection

## Architectural Patterns

- **Metadata-Driven**: YAML frontmatter declares command/agent behavior
- **Trigger-Based Skills**: Skills activate on conditions (missing files, thresholds, failures)
- **Composable Agents**: Multiple agents can collaborate on tasks via `/cdf:task`
- **Hook Lifecycle**: Pre/Post hooks for validation, enhancement, and logging
- **Convention over Configuration**: Sensible defaults require no setup

## Boundaries

- **Sacred files** (never modify without testing): `hooks/hooks.json`, `scripts/lib/utils.py`, `.claude-plugin/plugin.json`
- **Never commit**: `.env`, `dev/active/` flow state, `*.local.json`
- **Review-required**: Command/agent/skill definition changes, public hook interface changes

## Extension Points

- Add commands: `commands/*.md` (update counts in plugin.json, CLAUDE.md, README.md)
- Add agents: `agents/*.md` (update counts)
- Add skills: `skills/*/SKILL.md`
- Add hooks: `hooks/hooks.json` → `scripts/` or `scripts/hooks/`
- Add context modes: `contexts/*.md`
