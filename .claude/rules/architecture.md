# Architecture

## Bird's Eye View

CDF (Claude Dev Framework) is a Claude Code plugin with a host-adaptable core. It provides modular commands, agents, skills, rules, and hooks that turn coding agents into structured, opinionated development assistants across Claude Code first and Codex through adapter guidance.

## Codemap

| Directory | Purpose |
|-----------|---------|
| `commands/` | 21 slash command definitions (markdown + YAML frontmatter). Each file is a complete behavioral spec. |
| `agents/` | 12 real-expertise agent definitions. Activated through `/cdf:task` or command-specific routing. |
| `skills/` | 24 auto-invoked skill directories (`skills/*/SKILL.md`). Trigger-based, no explicit invocation. |
| `hooks/` | Lifecycle hook configuration (`hooks.json`). |
| `scripts/` | Hook implementation scripts and shared utilities. |
| `rules-templates/` | 15 rule templates: best-practice, project-type, workflow, and 4.7 CLAUDE.md guidance. |
| `mcp-configs/` | MCP server configuration templates (7 pre-configured servers). |
| `.claude-plugin/` | Plugin metadata (`plugin.json` v1.13.0). |
| `.claude/` | Plugin settings, permissions, rules, and runtime memory. |
| `docs/` | Institutional knowledge and solved problem references. |

## Key Files

| File | Role |
|------|------|
| `.claude-plugin/plugin.json` | Plugin metadata, version (1.13.0) |
| `.claude-plugin/marketplace.json` | Marketplace metadata; version and count strings must match actual components |
| `hooks/hooks.json` | Lifecycle hook definitions — 7 hooks across 4 event types |
| `scripts/analyze-codebase.py` | SessionStart hook — project analysis and rule generation |
| `scripts/hooks/session-context.py` | SessionStart hook — injects git history + auto-memory context |
| `scripts/lib/utils.py` | Shared utility functions used by all hook scripts |

## Component Relationships

```
User Request
    ↓
Command Router → Loads command definition
    ↓
Agent Routing → Uses real-expertise agents or role-framed `/cdf:task` prompts
    ↓
Skill Activation → Triggers context-aware behaviors
    ↓
Hook Execution → Pre/Post tool use hooks
    ↓
MCP Integration → External tool coordination
```

## Data Flow

1. **SessionStart**: `analyze-codebase.py` analyzes project and generates rules; `session-context.py` injects git history + auto-memory context (60s timeout each)
2. **Request Processing**: command loaded, real agents or role-framed `/cdf:task` selected, skills activated
3. **PreToolUse**: `git-push-review.py` and `pre-push-checks.py` warn on risky git operations
4. **PostToolUse**: `console-log-detector.py`, `comment-checker.py` validate code quality
5. **Stop**: `task-completeness-check.sh` verifies completion

## Cross-Cutting Concerns

- **Session Context**: `session-context.py` injects recent git history and auto-memory at session start. No CDF-owned storage.
- **Routing Discipline**: Deleted orchestrator commands stay deleted. Complex lifecycle work goes through clear prompts with `xhigh` effort or `/cdf:task`.
- **Quality Gates**: `comment-checker.py` (35% threshold), `console-log-detector.py` (debug statements), and `scripts/health-check.py` catch framework drift.
- **Error Recovery**: `failure-recovery` skill activates after 3 consecutive failures (STOP → REVERT → DOCUMENT → CONSULT).

## Architectural Invariants

- Hook scripts use only Python stdlib — no external dependencies
- Commands, agents, and skills are pure markdown — no executable code
- `hooks/hooks.json` is the single source of truth for lifecycle configuration
- All hook scripts return JSON to stdout for Claude injection

## Architectural Patterns

- **Metadata-Driven**: YAML frontmatter declares command/agent behavior
- **Trigger-Based Skills**: Skills activate on conditions (missing files, thresholds, failures)
- **Real-Expertise Agents**: Agent files represent concrete capabilities; generic roles are expressed as prompt framing, not stub agents
- **Hook Lifecycle**: Pre/Post hooks for validation, enhancement, and logging
- **Convention over Configuration**: Sensible defaults require no setup

## Boundaries

- **Sacred files** (never modify without testing): `hooks/hooks.json`, `scripts/lib/utils.py`, `.claude-plugin/plugin.json`
- **Never commit**: `.env`, transient task state, `*.local.json`
- **Review-required**: Command/agent/skill definition changes, public hook interface changes

## Extension Points

- Add commands: `commands/*.md` (update count-bearing docs and run `scripts/health-check.py`)
- Add agents: `agents/*.md` (only for real expertise, not generic role stubs)
- Add skills: `skills/*/SKILL.md`
- Add hooks: `hooks/hooks.json` → `scripts/` or `scripts/hooks/`
