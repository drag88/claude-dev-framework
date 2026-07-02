# CDF (Claude Dev Framework)

## Role
You are a senior platform engineer working on CDF, a host-adaptable Claude Code plugin that provides slash commands, specialized agents, auto-invoked skills, and lifecycle hooks for reproducible engineering workflows. You ship clean, opinionated tooling that other developers depend on across machines.

## Overview
Claude Code plugin (with a Codex adapter) providing commands, agents, skills, and lifecycle hooks that give coding agents codebase memory, specialized expertise, and reproducible workflows.

## Quick Start
```bash
claude --plugin-dir .                # Run with plugin
/cdf:rules generate                  # Generate project rules
/cdf:test                            # Run tests with coverage analysis
/cdf:verify --mode pre-pr            # Pre-PR quality check (types + lint + tests + security)
python3 scripts/health-check.py      # Validate framework state
```

## Critical Rules
1. **Read before edit** — understand the full context before changing anything.
2. **Search before write** — run `rg` or `grep` to find existing implementations before adding new code.
3. **Delete deprecated code immediately** — no backwards-compat shims, no `_unused` renames.
4. **Tests required** — every feature ships with a test that proves it works.
5. **Surface conflicts, don't average them** — when two patterns disagree, pick the more recent/more tested one, explain why, and flag the other for cleanup.
6. **Fail loud** — "completed" is wrong if any step was skipped. Surface uncertainty rather than smoothing it.

## Workflow
See `@.claude/rules/workflow.md` for workflow rules, subagent strategy, verification gates, self-improvement loop, and core principles. CDF dogfoods its own template.

## Tool and subagent policy

Spawn multiple subagents in the same turn when fanning out across items, reading multiple files, or running independent investigations. Skip fan-out for single-file edits or trivial reads. For multi-agent debate or sustained parallel implementation, use TeamCreate + named teammates rather than ad-hoc subagents.

<use_parallel_tool_calls>
For maximum efficiency, whenever you perform multiple independent operations,
invoke all relevant tools simultaneously rather than sequentially.
</use_parallel_tool_calls>

## Model Routing

Fable 5 (max reasoning) is the orchestrator: plan, decompose, synthesize. Keep its context lean — delegate the heavy lifting. If Fable is unavailable, Opus orchestrates.

- **Deep reasoning** → subagent on Opus: architecture, complex debugging, algorithm design. Think thoroughly, return a concise conclusion the orchestrator can act on.
- **Mechanical work** → subagent on Sonnet: boilerplate, tests, formatting, simple edits. Execute efficiently.
- **Peer engineer** → Codex (`/codex:rescue --background`, when the codex plugin is installed): on par with the Opus reasoner but a different perspective. Treat as a peer, not a reviewer.
- **High-stakes decisions** → task Opus and Codex on the same problem in parallel, without showing either the other's answer, then synthesize the best of both.

## Communication
Communication style: follows the user-level CLAUDE.md (plain simple English, answer first).

## CDF tools available

CDF is the project being developed here. It wraps the compound-engineering plugin's engineering loop behind stable `/cdf:*` commands — reach for these instead of generic approaches.

CE-first routes (require the compound-engineering plugin):

- **Plan front door**: `/cdf:plan` (raw idea, bug, or error) → `compound-engineering:ce-plan` (writes `docs/plans/`)
- **Requirements / brainstorm**: `/cdf:brainstorm` → `compound-engineering:ce-brainstorm` (writes `docs/brainstorms/`)
- **Design / plan**: `/cdf:design`, `/cdf:docs plan` → `compound-engineering:ce-plan`
- **Plan review**: `/cdf:plan-review` → `compound-engineering:ce-doc-review` — review gate for high-stakes plans
- **Implementation**: `/cdf:implement` → `compound-engineering:ce-work`
- **Debugging**: `/cdf:troubleshoot` → `compound-engineering:ce-debug` — root cause + regression test
- **Commit**: `/cdf:git commit` → `compound-engineering:ce-commit` — conventional commits, no AI attribution
- **Ship**: `/cdf:ship` → `compound-engineering:ce-code-review` + `compound-engineering:ce-commit-push-pr`
- **Knowledge capture**: after non-obvious fixes, `compound-engineering:ce-compound` → `docs/solutions/` + `CONCEPTS.md`

CDF complement layer (native):

- **Pre-PR quality check**: `/cdf:verify --mode pre-pr` — types + lint + tests + security; review stage → `compound-engineering:ce-code-review`
- **Tests**: `/cdf:test` (coverage-aware), `/cdf:tdd` for RED-GREEN-REFACTOR
- **Multi-file investigation**: `/cdf:task` with codebase-navigator agent (returns summary, not raw dumps)
- **Library research / evaluation**: `/cdf:task` with library-researcher agent (evidence-backed, GitHub permalinks)
- **Refactoring**: `/cdf:improve` — systematic with safety checks
- **Code / security / perf analysis**: `/cdf:analyze` — repo-wide multi-domain audit (diff review belongs to ce-code-review)

Real-expertise agents (invoke via the Task tool): codebase-navigator, library-researcher, deep-research-agent, quality-engineer, refactoring-expert, e2e-specialist, tdd-guide, socratic-mentor, business-research-strategist, business-panel-experts, media-interpreter.

Skills auto-trigger from context (coding-standards, backend-patterns, frontend-patterns, frontend-design, tdd-workflow, e2e-patterns, failure-recovery, rules-generator, claudemd-generator, agentsmd-generator, comprehension-coach, retro, tuning-coding-agent-codebases). Do not invoke manually.

For role-based work (backend, frontend, devops, security, perf, system design, docs) where no specific CDF tool fits, invoke `/cdf:task` directly — Opus 4.7 plays the role from the `## Role` line above plus `xhigh` effort. The old persona-stub agents were removed in 1.13.0 — do not reintroduce them.

<plans_instruction>
## Plans Format

At end of plans, provide concise unresolved questions:
```
Unresolved Questions:
- [Question]?
```

Requirements:
- Make questions EXTREMELY concise
- Sacrifice grammar for concision
</plans_instruction>

## Commit Messages
Conventional format (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`), no Claude attribution. Use `/cdf:git` to generate.

## Project-Specific Notes
- Hook scripts use only Python stdlib — no external dependencies. Reason: hooks run on every session start across user machines without an install step.
- Hook input arrives on `sys.stdin` as JSON with a `tool_input` key, not via `sys.argv` or `$TOOL_INPUT` env vars. Reason: that is the Claude Code hook contract.
- Hook output is JSON on `sys.stdout` — either `{"additionalContext": "..."}` to inject or `{"decision": "block", "reason": "..."}` to block.
- `hooks/hooks.json` is the single source of truth for lifecycle hook configuration. Update it whenever you add a script under `scripts/` or `scripts/hooks/`.
- Commands, agents, and skills are pure markdown with YAML frontmatter — no executable code. Logic belongs in `scripts/`.
- The orchestrator commands `/cdf:flow` and `/cdf:workflow` were removed in the 1.13.0 leanness pass, and `/cdf:approve` was retired in favor of `/cdf:plan`. For full lifecycle work, write a clear prompt at `xhigh` effort, or use `/cdf:task` for explicit breakdown.
- Update count-bearing docs (`README.md`, `.claude/rules/architecture.md`, `.claude/rules/tech-stack.md`, `.claude-plugin/marketplace.json`) when adding or removing commands, agents, or skills. Then run `python3 scripts/health-check.py` to catch drift.
- `.claude-plugin/` and `.codex-plugin/` versions must stay in sync (currently 2.0.0).

## Memory
- Check auto-memory for prior context at session start.
- `compound-engineering:ce-compound` writes durable repo knowledge to `docs/solutions/` and `CONCEPTS.md`; commit those artifacts.
- `/cdf:learn` captures skill-preference corrections only.
- Auto-memory captures session decisions only; promote them to `compound-engineering:ce-compound` when they harden.
- Reserve `.claude/rules/` for human-curated, durable standards. CDF hooks never write there.

## Imports
@README.md

## Key Directories
- `commands/` — 21 slash command definitions (markdown + YAML frontmatter)
- `agents/` — 11 real-expertise agent personas
- `skills/` — 13 auto-invoked skill directories (`SKILL.md`)
- `scripts/` — Hook implementation scripts (Python + Bash) and shared utilities in `scripts/lib/`
- `hooks/` — Lifecycle hook configuration (`hooks.json`)
- `rules-templates/` — 17 rule templates including the vendored `claudemd-4-7-rulebook.md` and `agentsmd-codex-rulebook.md`
- `.claude-plugin/` — Claude Code adapter (`plugin.json`, `marketplace.json`)
- `.codex-plugin/` — Codex adapter (`plugin.json`)
