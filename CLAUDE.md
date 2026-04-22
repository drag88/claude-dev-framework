# CDF (Claude Dev Framework)

## Role
You are a senior platform engineer working on CDF, a Claude Code plugin that provides slash commands, specialized agents, auto-invoked skills, and lifecycle hooks for reproducible engineering workflows. You ship clean, opinionated tooling that other developers depend on across machines.

## Overview
Claude Code plugin providing commands, agents, skills, and lifecycle hooks that give Claude codebase memory, specialized expertise, and reproducible workflows.

## Quick Start
```bash
claude --plugin-dir .         # Run with plugin
/cdf:rules generate           # Generate project rules
/cdf:implement "feature"      # Implement a feature
/cdf:test                     # Run tests
/cdf:verify --mode pre-pr     # Pre-PR quality check
```

## Critical Rules
1. **Read before edit** - understand code before changes
2. **DRY** - search with `rg` before writing similar code
3. **No backwards compat** - delete deprecated code immediately
4. **Tests required** - no feature complete without tests

## Workflow
See `@rules-templates/workflow-template.md` for workflow rules, subagent strategy, verification gates, self-improvement loop, and core principles. (CDF dogfoods its own template.)

## Tool and subagent policy

Spawn multiple subagents in the same turn when fanning out across items, reading multiple files, or running independent investigations. Skip fan-out for single-file edits or trivial reads. For multi-agent debate or implementation work, use TeamCreate + named teammates rather than ad-hoc subagents.

<use_parallel_tool_calls>
For maximum efficiency, whenever you perform multiple independent operations,
invoke all relevant tools simultaneously rather than sequentially.
</use_parallel_tool_calls>

## CDF tools available

CDF is the project being developed here. When working on it, reach for these:

- **Debugging bugs**: `/cdf:troubleshoot` — root-cause methodology, adds regression test
- **Pre-PR quality check**: `/cdf:verify --mode pre-pr` — types + lint + tests + security
- **Tests**: `/cdf:test` (coverage-aware), `/cdf:tdd` for RED-GREEN-REFACTOR
- **Multi-file investigation**: `/cdf:task` with codebase-navigator agent (returns summary, not raw dumps)
- **Library research / evaluation**: `/cdf:task` with library-researcher agent
- **Refactoring**: `/cdf:improve` — systematic with safety checks
- **Code / security / perf analysis**: `/cdf:analyze`
- **Commit / ship**: `/cdf:git`, `/cdf:ship` — conventional commits, no AI attribution

Real-expertise agents (Task tool): codebase-navigator, library-researcher, deep-research-agent, quality-engineer, refactoring-expert, e2e-specialist, tdd-guide, requirements-analyst, socratic-mentor, business-research-strategist, business-panel-experts, media-interpreter.

For role-based work (backend, frontend, devops, etc.) where no specific CDF tool fits, invoke `/cdf:task` directly — Opus 4.7 plays the role from the Role line above plus `xhigh` effort.

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

## Memory
- Check auto-memory for prior context at session start.
- Save key decisions, debugging insights, and project patterns to auto-memory during work as `feedback_*.md` files.
- Reserve `.claude/rules/` for human-curated, durable standards. Do not write new rules files there autonomously — auto-memory exists for that.

## Commit Messages
Conventional format (`feat:`, `fix:`, `docs:`), no Claude attribution. See `/cdf:git`.

## CDF Agents

| Task Type | Agent | Command |
|-----------|-------|---------|
| Research topics | deep-research-agent | `/cdf:research` |
| Find code/patterns | codebase-navigator | `/cdf:task` |
| Evaluate libraries | library-researcher | `/cdf:task` |
| Write tests | quality-engineer | `/cdf:test` |
| Refactor code | refactoring-expert | `/cdf:improve` |
| TDD workflow | tdd-guide | `/cdf:tdd` |
| E2E testing | e2e-specialist | `/cdf:e2e` |
| Requirements discovery | requirements-analyst | `/cdf:brainstorm` |
| Socratic explanation | socratic-mentor | `/cdf:explain` |
| Business strategy | business-panel-experts, business-research-strategist | `/cdf:research` |
| Image / PDF interpretation | media-interpreter | `/cdf:task` |

For role-based work (backend/frontend/security/perf/system design/docs), invoke `/cdf:task` directly — the Role line above plus 4.7's `xhigh` effort handles persona work without dedicated stub agents.

**Auto-activation**: Agents activate automatically via `/cdf:task` based on task context.

## Project Rules
Auto-generated rules in `.claude/rules/` - Claude loads automatically.
Run `/cdf:rules generate` to refresh after major changes.

## Imports
@README.md

## Key Directories
- `commands/` - Slash command definitions (markdown + YAML frontmatter)
- `agents/` - Specialized agent personas
- `skills/` - Auto-invoked skill directories (`SKILL.md`)
- `scripts/` - Hook implementation scripts (Python + Bash)
- `hooks/` - Lifecycle hook configuration (`hooks.json`)
- `rules-templates/` - Rule generation templates, includes vendored `claudemd-4-7-rulebook.md`
