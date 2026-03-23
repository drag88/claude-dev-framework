# CDF (Claude Dev Framework)

## Overview
Claude Code plugin providing commands, agents, skills, and lifecycle hooks that transform Claude into an opinionated development assistant with codebase memory, specialized expertise, and reproducible workflows.

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
Explore → Plan → Code → Verify. Always explore full scope before piecemeal edits.
Plan mode for 3+ step tasks. Subagents for exploration; agent teams for parallel implementation.
Full workflow, agent routing table, and delegation patterns in `.claude/rules/workflow.md`.

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
Conventional format (`feat:`, `fix:`, `docs:`), no Claude attribution.

## Project-Specific Notes
- Hook scripts use only Python stdlib — no external dependencies allowed
- Sacred files (never modify without testing): `hooks/hooks.json`, `scripts/lib/utils.py`, `.claude-plugin/plugin.json`
- When adding commands/agents/skills, update counts in `plugin.json`, `CLAUDE.md`, and `README.md`

## Key Directories
- `commands/` - 21 slash command definitions (markdown + YAML frontmatter)
- `agents/` - 22 agent persona definitions
- `skills/` - 27 auto-invoked skill directories (`SKILL.md`)
- `scripts/` - Hook implementation scripts (Python + Bash)
- `hooks/` - Lifecycle hook configuration (`hooks.json`)
- `rules-templates/` - 14 rule generation templates
- `contexts/` - 3 behavioral context modes (dev/review/research)
