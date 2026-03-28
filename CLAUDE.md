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

### Explore → Plan → Code → Verify
- Use plan mode for non-trivial tasks (3+ steps or multi-file changes)
- For small fixes (typo, rename, single-file change), skip planning and execute directly
- If something goes sideways, STOP and re-plan — do not push through a broken approach

### Subagent Strategy
- Use subagents for exploration and research to keep main context clean
- One atomic goal per subagent — return summaries, not raw file dumps
- For complex problems, spawn parallel subagents covering different angles
- Main context is for implementation only

### Verification Before Done
- Never mark a task complete without proving it works
- Run tests, check logs, demonstrate correctness
- For visual/UI changes: verify in the browser before confirming to the user
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"

### Self-Improvement Loop
- After ANY correction from the user: capture the pattern in `.claude/rules/`
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these rules until mistake rate drops
- Review rules at session start for relevant project

### Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting it

### Autonomous Bug Fixing
- Given a bug report: identify root cause, fix it, add regression test, verify
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user

### Context Management
- Run /clear between unrelated tasks
- Use /compact when context grows large
- After 2 failed corrections on the same issue, clear context and restart with a better prompt

### Core Principles
- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Only touch what's necessary. No side effects with new bugs.

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
- Check auto-memory for prior context at session start
- Save key decisions, debugging insights, and project patterns to auto-memory during work

## Commit Messages
Conventional format (`feat:`, `fix:`, `docs:`), no Claude attribution. See `/cdf:git`.

## CDF Agents

| Task Type | Agent | Command |
|-----------|-------|---------|
| System design | system-architect | `/cdf:task` |
| API/backend work | backend-architect | `/cdf:task` |
| UI development | frontend-architect | `/cdf:task` |
| CI/CD setup | devops-architect | `/cdf:task` |
| Research topics | deep-research-agent | `/cdf:research` |
| Find code/patterns | codebase-navigator | `/cdf:task` |
| Evaluate libraries | library-researcher | `/cdf:task` |
| Debug issues | root-cause-analyst | `/cdf:troubleshoot` |
| Write tests | quality-engineer | `/cdf:test` |
| Security audit | security-engineer | `/cdf:analyze` |
| Performance | performance-engineer | `/cdf:analyze` |
| Refactor code | refactoring-expert | `/cdf:improve` |
| Documentation | technical-writer | `/cdf:docs` |
| TDD workflow | tdd-guide | `/cdf:tdd` |
| E2E testing | e2e-specialist | `/cdf:e2e` |

**Auto-activation**: Agents activate automatically via `/cdf:task` based on task context.

## Project Rules
Auto-generated rules in `.claude/rules/` - Claude loads automatically.
Run `/cdf:rules generate` to refresh after major changes.

## Key Directories
- `commands/` - 22 slash command definitions (markdown + YAML frontmatter)
- `agents/` - 22 agent persona definitions
- `skills/` - 27 auto-invoked skill directories (`SKILL.md`)
- `scripts/` - Hook implementation scripts (Python + Bash)
- `hooks/` - Lifecycle hook configuration (`hooks.json`)
- `rules-templates/` - 14 rule generation templates
- `contexts/` - 3 behavioral context modes (dev/review/research)
