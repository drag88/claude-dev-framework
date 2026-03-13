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

## Subagent Strategy

**Default to subagents for exploration. Main context is for implementation.**

| Task | Use Subagent? | Why |
|------|:---:|-----|
| Exploring unfamiliar code | Yes | Returns summary, not raw files |
| Researching library/API | Yes | Returns verdict + key facts |
| Parallel analysis (multiple dirs) | Yes | Multiple agents, simultaneous |
| Tracing bugs across files | Yes | Reads 10+ files without polluting context |
| Single targeted grep/read | No | Faster inline |
| Writing/editing files | No | Must stay in main context |

**Rules:**
- One atomic goal per subagent. Return summaries, not raw dumps.
- For complex problems, spawn 3-5 agents in parallel covering different angles.
- Full workflow details: `.claude/rules/workflow.md`

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
- **Semantic memory**: Claude's native auto-memory (decisions, patterns, preferences)
- **Session context**: Auto-injected at session start from git history + auto-memory
- CDF reads auto-memory at session start but never writes to it

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
- `commands/` - 21 slash command definitions (markdown + YAML frontmatter)
- `agents/` - 22 agent persona definitions
- `skills/` - 26 auto-invoked skill directories (`SKILL.md`)
- `scripts/` - Hook implementation scripts (Python + Bash)
- `hooks/` - Lifecycle hook configuration (`hooks.json`)
- `rules-templates/` - 14 rule generation templates
- `contexts/` - 3 behavioral context modes (dev/review/research)
