# CDF (Claude Dev Framework)

## Overview
Comprehensive Claude Code plugin providing 19 commands, 22 agents, 20 skills, and 11 lifecycle hooks for intelligent development assistance. Transforms Claude into an opinionated development assistant with codebase memory, specialized expertise on demand, and reproducible workflows.

## Quick Start
```bash
claude --plugin-dir .         # Run with plugin (local dev)
/cdf:rules generate           # Generate project rules
/cdf:implement "feature"      # Implement a feature
python3 -m json.tool hooks/hooks.json  # Validate hooks
```

## Critical Rules
1. **Read before edit** - understand code before changes
2. **DRY** - search with `rg` before writing similar code
3. **No backwards compat** - delete deprecated code immediately
4. **Tests required** - no feature complete without tests

## Memory Split
| Concern | Owner | Storage |
|---------|-------|---------|
| Semantic memories (decisions, patterns, preferences) | Claude native auto-memory | `~/.claude/projects/<key>/memory/MEMORY.md` |
| Structured daily activity (file edits only) | CDF hooks | `.claude/memory/daily/YYYY-MM-DD.md` |
| Session context injection | CDF memory-init | `.claude/rules/memory-context.md` |

CDF hooks never write to native auto-memory. Claude owns semantic memory.

## Project Soul
- **Values**: Correctness over speed, composability over monoliths, explicit over implicit
- **Boundaries**: Never commit `dev/active/`, `.claude/memory/daily/`, `*.local.json`
- **Sacred files**: `hooks/hooks.json`, `scripts/lib/utils.py`, `.claude-plugin/plugin.json`
- Full details: `.claude/rules/soul.md`

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

## Commit Messages
See `/cdf:git` for commit message rules (conventional format, no Claude attribution).

## CDF Agents

When working in this project, use the appropriate CDF agent for specialized tasks:

| Task Type | Agent | Command |
|-----------|-------|---------|
| System design | system-architect | `/cdf:task` |
| API/backend work | backend-architect | `/cdf:task` |
| UI development | frontend-architect | `/cdf:task` |
| CI/CD setup | devops-architect | `/cdf:task` |
| Research topics | deep-research-agent | `/cdf:research` |
| Find code/patterns | codebase-navigator | `/cdf:task` |
| Debug issues | root-cause-analyst | `/cdf:troubleshoot` |
| Write tests | quality-engineer | `/cdf:test` |
| Refactor code | refactoring-expert | `/cdf:improve` |

**Auto-activation**: Agents activate automatically via `/cdf:task` based on task context.

## Project Rules
Auto-generated rules in `.claude/rules/` - Claude loads automatically.
Run `/cdf:rules generate` to refresh after major changes.

## Key Directories
- `commands/` - 29 slash command definitions (markdown + YAML frontmatter)
- `agents/` - 22 agent persona definitions
- `skills/` - 20 auto-invoked skill directories
- `scripts/` - Hook implementation (Python)
- `hooks/` - Lifecycle hook configuration (JSON)
- `rules-templates/` - 16 rule templates for project-type-aware generation
