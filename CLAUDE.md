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

## Model Routing
- **Planning**: Fable if available, else Opus. **Execution + subagents**: Sonnet.

## Communication
Communication style: follows the user-level CLAUDE.md (plain simple English, answer first).

## CDF tools available

CDF is the project being developed here. When working on it, reach for these:

### CE-first routes

| Need | CDF route | CE skill |
|------|-----------|----------|
| Ideation | (no wrapper — invoke the skill directly) | `compound-engineering:ce-ideate` |
| Requirements discovery | `/cdf:brainstorm` | `compound-engineering:ce-brainstorm` |
| Design or plan | `/cdf:design`, `/cdf:docs plan` | `compound-engineering:ce-plan` |
| Pre-approval review | `/cdf:plan-review` | `compound-engineering:ce-doc-review` |
| Implementation | `/cdf:implement` | `compound-engineering:ce-work` |
| Debugging | `/cdf:troubleshoot` | `compound-engineering:ce-debug` |
| Git commit | `/cdf:git commit` | `compound-engineering:ce-commit` |
| Ship review and PR | `/cdf:ship` | `compound-engineering:ce-code-review`, `compound-engineering:ce-commit-push-pr` |

### CDF complement layer (the ++)

- Rules generation, lifecycle hooks, host adapters, `/cdf:learn`, and session memory.
- Real-expertise agents and `/cdf:task` fan-out for multi-file investigation.
- Quality gates: `/cdf:test`, `/cdf:tdd`, `/cdf:e2e`, `/cdf:verify`.
- Specialist commands: `/cdf:estimate`, `/cdf:explain`, `/cdf:research`, `/cdf:analyze` repo-wide audits.

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
- `compound-engineering:ce-compound` writes durable repo knowledge to `docs/solutions/` and `CONCEPTS.md`; commit those artifacts.
- `/cdf:learn` captures skill-preference corrections only.
- Auto-memory captures session decisions only; promote them to `compound-engineering:ce-compound` when they harden.
- `CONCEPTS.md` is seeded by `compound-engineering:ce-compound` on first capture; do not create it manually.

## Commit Messages
Conventional format (`feat:`, `fix:`, `docs:`), no Claude attribution. See `/cdf:git`.

## CDF Agents

Real-expertise agents: codebase-navigator, library-researcher, deep-research-agent, quality-engineer, refactoring-expert, e2e-specialist, tdd-guide, socratic-mentor, business-research-strategist, business-panel-experts, media-interpreter. Use via `/cdf:task` or the relevant CDF command; auto-activation follows context.

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
