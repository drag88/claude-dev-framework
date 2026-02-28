# AGENTS.md

## Project Overview

CDF (Claude Dev Framework) is a Claude Code plugin providing 19 commands, 22 agent personas, 20 skills, and 11 lifecycle hooks for structured, consistent AI-assisted development. It turns Claude into an opinionated development assistant with codebase memory, specialized expertise on demand, and reproducible workflows.

## Development Setup

```bash
# Run Claude with the plugin locally
claude --plugin-dir .

# Verify plugin loaded
/cdf:rules generate

# Generate/refresh project rules
/cdf:rules generate
```

No build step required — the plugin loads markdown/JSON files directly.

## Architecture

Key modules and their roles:

- `commands/` — 29 slash command definitions (markdown + YAML frontmatter). Each file is a complete behavioral spec for one command.
- `agents/` — 22 agent personas (markdown + YAML). Activated by `/cdf:task` or automatically via task context.
- `skills/` — 20 auto-invoked skill directories (`skills/*/SKILL.md`). Trigger-based activation without explicit invocation.
- `hooks/hooks.json` — Lifecycle hook configuration. SessionStart, PreToolUse, PostToolUse, Stop hooks.
- `scripts/` — Hook implementation in Python. `analyze-codebase.py` (SessionStart), `keyword-amplifier.py` (PreToolUse), `hooks/memory-logger.py` (PostToolUse: Edit/Write/Bash/WebSearch/WebFetch/Read), `hooks/memory-init.py` (SessionStart), `hooks/memory-summarize.py` (Stop: daily log summary + native auto-memory recap).
- `rules-templates/` — 16 reusable templates for `/cdf:rules generate` (5 best-practice + 11 project-type/generation-specific).

## Coding Standards

- **Command/agent/skill format**: YAML frontmatter + markdown body. Frontmatter declares metadata; body is behavioral instruction.
- **Hook scripts**: Python 3, no external dependencies beyond stdlib. Return `{"additionalContext": "..."}` for Claude injection or `{"decision": "block", "reason": "..."}` to block tool use.
- **No backwards compat**: Delete deprecated code immediately. No shims.
- **Conventional commits**: `feat:`, `fix:`, `docs:`, `refactor:` — no Claude attribution in commits.
- **Read before edit**: Always understand the full command/agent definition before modifying.

## Agent Guidelines

- **Never modify directly**: `hooks/hooks.json` (test lifecycle changes), `scripts/lib/utils.py` (shared by all hooks), `.claude-plugin/plugin.json` (version requires justification)
- **Never commit**: `dev/active/` flow state, `.claude/memory/daily/` logs, `*.local.json` settings files
- **Always run after hook changes**: Restart Claude session to reload hooks (`claude --plugin-dir .`)
- **Multi-agent safety**: `hooks/hooks.json` and `scripts/analyze-codebase.py` are high-blast-radius — coordinate before concurrent edits
- **Adding a command**: Create `commands/name.md` with YAML frontmatter, update count in `plugin.json`, `marketplace.json`, `CLAUDE.md`, `README.md`, `AGENTS.md`, `.claude/rules/architecture.md`, `.claude/rules/soul.md`
- **Adding a skill**: Create `skills/name/SKILL.md`, add to `skills/README.md` (table + Quick Selection Guide), update count in all docs above
