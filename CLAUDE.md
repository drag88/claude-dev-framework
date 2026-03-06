# CDF (Claude Dev Framework)

## Overview
Comprehensive Claude Code plugin providing commands, agents, skills, and lifecycle hooks for intelligent development assistance. Transforms Claude into an opinionated development assistant with codebase memory, specialized expertise on demand, and reproducible workflows.

## Quick Start
```bash
claude --plugin-dir .         # Run with plugin (local dev)
/cdf:rules generate           # Generate project rules
/cdf:implement "feature"      # Implement a feature
```

## Critical Rules
1. **Read before edit** - understand code before changes
2. **DRY** - search with `rg` before writing similar code
3. **No backwards compat** - delete deprecated code immediately
4. **Tests required** - no feature complete without tests

## Memory
- **Semantic memory** (decisions, patterns, preferences): Claude's native auto-memory
- **Daily file change log**: `.claude/memory/daily/` (CDF hook, append-only)

CDF hooks never write to native auto-memory. Claude owns semantic memory.

## Commit Messages
Conventional format (`feat:`, `fix:`, `docs:`), no Claude attribution. See `/cdf:git`.

## Plans Format

Unresolved questions at end of plans -- keep them extremely concise, sacrifice grammar for concision.

## Project Rules
Auto-generated rules in `.claude/rules/` -- Claude loads automatically.
Run `/cdf:rules generate` to refresh after major changes.

## Business Strategy Agent
For business model analysis, competitive positioning, or market strategy, activate **business-panel-experts** — synthesizes Christensen, Porter, Drucker, Godin, Kim & Mauborgne, Collins, Taleb, Meadows, and Doumont in sequential, debate, or Socratic modes. Details: `agents/business-panel-experts.md`

## Key Directories
- `commands/` - Slash command definitions
- `agents/` - Agent persona definitions
- `skills/` - Auto-invoked skill directories
- `scripts/` - Hook implementation scripts
- `hooks/` - Lifecycle hook configuration
- `rules-templates/` - Rule generation templates
