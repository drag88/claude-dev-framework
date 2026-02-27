# CDF (Claude Dev Framework)

## Overview
Comprehensive Claude Code plugin providing 29 commands, 22 agents, 19 skills, and 13 lifecycle hooks for intelligent development assistance. Transforms Claude into an opinionated development assistant with codebase memory, specialized expertise on demand, and reproducible workflows.

## Quick Start
```bash
claude --plugin-dir .         # Run with plugin (local dev)
/cdf:help                     # List all commands
/cdf:rules generate           # Generate project rules
/cdf:implement "feature"      # Implement a feature
python3 -m json.tool hooks/hooks.json  # Validate hooks
```

## Critical Rules
1. **Read before edit** - understand code before changes
2. **DRY** - search with `rg` before writing similar code
3. **No backwards compat** - delete deprecated code immediately
4. **Tests required** - no feature complete without tests

## Project Soul
- **Values**: Correctness over speed, composability over monoliths, explicit over implicit
- **Boundaries**: Never commit `dev/active/`, `.claude/memory/daily/`, `*.local.json`
- **Sacred files**: `hooks/hooks.json`, `scripts/lib/utils.py`, `.claude-plugin/plugin.json`
- Full details: `.claude/rules/soul.md`

## Workflow
Orchestration rules (plan mode, subagents, verification): `.claude/rules/workflow.md`

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
See `/cdf:git` for commit message rules (conventional format, no Claude attribution).

## CDF Agents

When working in this project, use the appropriate CDF agent for specialized tasks:

| Task Type | Agent | Command |
|-----------|-------|---------|
| System design | system-architect | `/cdf:spawn` |
| API/backend work | backend-architect | `/cdf:spawn` |
| UI development | frontend-architect | `/cdf:spawn` |
| CI/CD setup | devops-architect | `/cdf:spawn` |
| Research topics | deep-research-agent | `/cdf:research` |
| Find code/patterns | codebase-navigator | `/cdf:spawn` |
| Debug issues | root-cause-analyst | `/cdf:troubleshoot` |
| Write tests | quality-engineer | `/cdf:test` |
| Refactor code | refactoring-expert | `/cdf:improve` |

**Auto-activation**: Agents activate automatically via `/cdf:spawn` and `/cdf:task` based on task context.

## Project Rules
Auto-generated rules in `.claude/rules/` - Claude loads automatically.
Run `/cdf:rules generate` to refresh after major changes.

## Key Directories
- `commands/` - 29 slash command definitions (markdown + YAML frontmatter)
- `agents/` - 22 agent persona definitions
- `skills/` - 19 auto-invoked skill directories
- `scripts/` - Hook implementation (Python)
- `hooks/` - Lifecycle hook configuration (JSON)
- `rules-templates/` - 15 rule templates for project-type-aware generation
