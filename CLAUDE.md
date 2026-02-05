# CDF (Claude Dev Framework)

## Overview
Comprehensive Claude Code plugin with 29 commands, 21 agents, 16 skills, and 13 hooks for intelligent development assistance.

## Quick Start
```bash
claude --plugin-dir .        # Run with plugin
/cdf:help                    # List commands
/cdf:rules generate          # Generate project rules
/cdf:implement "feature"     # Implement feature
```

## Critical Rules
1. **Read before edit** - understand code before changes
2. **DRY** - search with `rg` before writing similar code
3. **No backwards compat** - delete deprecated code immediately
4. **Tests required** - no feature complete without tests

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

## Project Rules
Auto-generated rules in `.claude/rules/` - Claude loads automatically.
Run `/cdf:rules generate` to refresh after major changes.

## Key Directories
- `commands/` - 29 slash command definitions (with MANDATORY FIRST ACTIONS enforcement)
- `agents/` - 21 specialized agent personas
- `skills/` - 16 auto-invoked behaviors
- `hooks/` - Lifecycle hook configuration (13 hooks)
- `scripts/` - Hook implementation (Python/Bash)
- `contexts/` - Behavioral modes (dev/review/research)
- `rules-templates/` - Best practice templates
- `docs/solutions/` - Institutional knowledge from /cdf:compound
- `dev/active/` - Flow state files (created by workflow commands)
- `dev/sessions/` - Session state files (created by /cdf:session)

## Command Enforcement
All workflow commands use MANDATORY FIRST ACTIONS pattern:
1. Create state file BEFORE any exploration
2. Follow explicit anti-patterns (DO NOT use .claude/plans/ for /cdf:flow)
3. Complete all steps before proceeding
