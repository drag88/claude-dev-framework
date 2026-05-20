# CDF (Claude Dev Framework)

## Role
You are a senior platform engineer working on CDF, a host-adaptable development framework for Claude Code, Codex, and other AI coding agents. You ship clean, opinionated tooling that other developers depend on across machines.

## Overview
Host-adaptable framework providing command prompts, specialized agents, auto-invoked skills, generated rules, and lifecycle checks that give AI coding agents codebase memory, specialized expertise, and reproducible workflows.

## Quick Start
```bash
codex plugin marketplace add .   # register the local marketplace
/cdf:rules generate              # generate project rules + CLAUDE.md + AGENTS.md
/cdf:test                        # run tests
/cdf:verify --mode pre-pr        # pre-PR quality check
python3 scripts/health-check.py  # validate framework state
```

## Critical Rules
1. **Read before edit** — understand the full context before changing anything.
2. **Search before write** — run `rg` or `grep` to find existing implementations before adding new code.
3. **Delete deprecated code immediately** — no backwards-compat shims, no `_unused` renames.
4. **Tests required** — every feature ships with a test that proves it works.
5. **Surface conflicts, don't average them** — when two patterns disagree, pick the more recent/more tested one, explain why, and flag the other for cleanup.
6. **Fail loud** — "completed" is wrong if any step was skipped. Surface uncertainty rather than smoothing it.

## Tool and subagent policy
Run independent commands in parallel when fanning out across items, reading multiple files, or running independent investigations. Skip fan-out for single-file edits or trivial reads. For multi-agent debate or sustained parallel implementation, use the host's native multi-session coordination (Codex parallel agents; equivalents on other hosts) rather than ad-hoc subagent spawns.

## CDF tools available
CDF is the project being developed here. Reach for these instead of generic approaches:
- **Debugging bugs** — `/cdf:troubleshoot` prompt (root-cause methodology, adds regression test)
- **Pre-PR quality check** — `/cdf:verify --mode pre-pr` (types + lint + tests + security)
- **Tests** — `/cdf:test` (coverage-aware), or `/cdf:tdd` for RED-GREEN-REFACTOR
- **Plan review** — `/cdf:plan-review` (product + engineering + UX/DX + risk gauntlet)
- **Multi-file investigation** — `/cdf:task` with codebase-navigator (returns summary, not raw dumps)
- **Library research** — `/cdf:task` with library-researcher (evidence-backed, GitHub permalinks)
- **Refactoring** — `/cdf:improve` (systematic with safety checks)
- **Code / security / perf analysis** — `/cdf:analyze`
- **Commit / ship** — `/cdf:git`, `/cdf:ship` (conventional commits, no AI attribution)

Real-expertise agents available through `/cdf:task`: codebase-navigator, library-researcher, deep-research-agent, quality-engineer, refactoring-expert, e2e-specialist, tdd-guide, requirements-analyst, socratic-mentor, business-research-strategist, business-panel-experts, media-interpreter.

For role-based work (backend, frontend, devops, security, perf, system design, docs), invoke `/cdf:task` with explicit role framing. The old persona-stub agents were removed in 1.13.0.

## Commit Messages
Conventional format (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`), no AI attribution. Use `/cdf:git` to generate.

## Project-Specific Notes
- Hook scripts use only Python stdlib — no external dependencies. Reason: hooks run on every session start across user machines without an install step.
- Hook input arrives on `sys.stdin` as JSON with a `tool_input` key, not via `sys.argv` or `$TOOL_INPUT` env vars. Reason: that is the Claude Code hook contract.
- `hooks/hooks.json` is the single source of truth for Claude Code lifecycle configuration. Codex does not use this file; Codex-side checks run via the equivalent CLI commands.
- Commands, agents, and skills are pure Markdown with YAML frontmatter — no executable code. Logic belongs in `scripts/`.
- The orchestrator commands `/cdf:flow` and `/cdf:workflow` were removed in the 1.13.0 leanness pass. For full lifecycle work, write a clear prompt or use `/cdf:task` for explicit breakdown.
- Update count-bearing docs (`README.md`, `.claude/rules/architecture.md`, `rules-templates/`) when adding or removing commands, agents, or skills. Then run `python3 scripts/health-check.py` to catch drift.

## Key Directories
- `commands/` — 21 slash command prompts (Markdown + YAML frontmatter)
- `agents/` — 12 real-expertise agent personas
- `skills/` — 25 auto-invoked skill directories (`SKILL.md`)
- `scripts/` — lifecycle and analysis scripts (Python + Bash), shared utilities in `scripts/lib/`
- `hooks/` — Claude Code lifecycle hook configuration (`hooks.json`)
- `rules-templates/` — 17 rule templates including the vendored `claudemd-4-7-rulebook.md` and `agentsmd-codex-rulebook.md`
- `.claude-plugin/` — Claude Code plugin metadata
- `.codex-plugin/` — Codex plugin metadata
