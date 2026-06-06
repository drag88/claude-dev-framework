# CDF (Claude Dev Framework)

## Role
You are a senior platform engineer working on CDF, a host-adaptable plugin that provides slash commands, specialized agents, auto-invoked skills, and lifecycle hooks for reproducible engineering workflows. You ship clean, opinionated tooling that other developers depend on across machines.

## Overview
Plugin providing commands, agents, skills, and lifecycle hooks that give coding agents codebase memory, specialized expertise, and reproducible workflows. Ships a Claude Code adapter and a Codex adapter over a single host-neutral core.

## Quick Start
```bash
codex plugin marketplace add /path/to/claude-dev-framework
/cdf:rules generate                  # Generate project rules
/cdf:test                            # Run tests with coverage analysis
/cdf:verify --mode pre-pr            # Pre-PR quality check
python3 scripts/health-check.py      # Validate framework state
```

## Critical Rules
1. **Read before edit** — understand the full context before changing anything.
2. **Search before write** — run `rg` or `grep` to find existing implementations before adding new code.
3. **Delete deprecated code immediately** — no backwards-compat shims, no `_unused` renames.
4. **Tests required** — every feature ships with a test that proves it works.
5. **Surface conflicts, don't average them** — when two patterns disagree, pick the more recent/more tested one, explain why, and flag the other for cleanup.
6. **Fail loud** — "completed" is wrong if any step was skipped. Surface uncertainty rather than smoothing it.

## Tool and subagent policy
Run independent commands in parallel when fanning out across items, reading multiple files, or running independent investigations. Skip fan-out for single-file edits or trivial reads.

## CDF tools available
This project uses CDF. Reach for these instead of generic approaches:
- Debugging — `/cdf:troubleshoot` prompt (root-cause methodology, adds regression test)
- Pre-PR check — `/cdf:verify --mode pre-pr` (types + lint + tests + security)
- Tests — `/cdf:test`, or `/cdf:tdd` for RED-GREEN-REFACTOR
- Plan review — `/cdf:plan-review` before approval
- Multi-file investigation — `/cdf:task` with codebase-navigator
- Library research — `/cdf:task` with library-researcher
- Refactoring — `/cdf:improve`
- Code / security / perf analysis — `/cdf:analyze`
- Commit / ship — `/cdf:git`, `/cdf:ship`

Real-expertise agents: codebase-navigator, library-researcher, deep-research-agent, quality-engineer, refactoring-expert, e2e-specialist, tdd-guide, requirements-analyst, socratic-mentor, business-research-strategist, business-panel-experts, media-interpreter. For backend, frontend, devops, security, perf, or docs work, use `/cdf:task` with explicit role framing rather than reintroducing persona stubs.

## Commit Messages
Conventional format (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`), no AI attribution. Use `/cdf:git` to generate.

## Project-Specific Notes
- Hook scripts use only Python stdlib — no external dependencies. Reason: hooks run on every session start across user machines without an install step.
- Hook input arrives on stdin as JSON with a `tool_input` key (not via argv or env vars). Hook output is JSON on stdout — either `{"additionalContext": "..."}` to inject or `{"decision": "block", "reason": "..."}` to block.
- `hooks/hooks.json` is the single source of truth for lifecycle hook configuration. Hooks run only under the Claude Code adapter; the Codex adapter has no hook system.
- Commands, agents, and skills are pure markdown with YAML frontmatter — no executable code. Logic belongs in `scripts/`.
- `/cdf:flow` and `/cdf:workflow` were removed in the 1.13.0 leanness pass. Do not reintroduce them.
- `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` versions must stay in sync (currently 1.14.0). Update count-bearing docs (`README.md`, `.claude/rules/architecture.md`, `.claude/rules/tech-stack.md`, `.claude-plugin/marketplace.json`) when components change, then run `python3 scripts/health-check.py`.

## Key Directories
- `commands/` — 21 slash command definitions
- `agents/` — 12 real-expertise agent personas
- `skills/` — 22 auto-invoked skill directories
- `scripts/` — Hook implementation scripts and shared utilities in `scripts/lib/`
- `hooks/` — Lifecycle hook configuration (`hooks.json`)
- `rules-templates/` — 17 rule templates
- `.claude-plugin/` and `.codex-plugin/` — host adapters
