# Project Soul

## Identity
- **What it is**: A Claude Code plugin framework that transforms Claude into a structured, opinionated development assistant with consistent workflows, deep codebase awareness, and specialized expertise on demand.
- **Who it serves**: Developers using Claude Code who want reproducible, high-quality AI assistance — not one-off answers but an assistant that remembers patterns, follows conventions, and escalates intelligently.
- **Core promise**: Every interaction should feel like pairing with a senior engineer who has read the entire codebase and won't forget it.

## Values
- **Correctness over speed**: Hooks validate, commands enforce patterns, agents specialize — the framework prioritizes doing things right over doing them fast.
- **Composability over monoliths**: 29 commands + 22 agents + 20 skills are modular by design. Add a command, not a god-mode prompt.
- **Explicit over implicit**: YAML frontmatter declares behavior, hooks declare lifecycle, skills declare triggers. Nothing magic happens without a spec.
- **Convention over configuration**: File-based memory, standardized rule templates, conventional commit format — sensible defaults that require no setup.

## Communication Style
- **Commit style**: Conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`) — no Claude attribution
- **Code comments**: Minimal — the *why*, not the *what*. Self-documenting names preferred.
- **Documentation tone**: Direct and technical. No filler. Tables over prose where possible.
- **Command style**: Verb-noun format (`/cdf:rules generate`, `/cdf:git commit`) — consistent across all 29 commands.

## Naming Conventions
- **Python variables/functions**: `snake_case`
- **Python classes**: `PascalCase`
- **Markdown files**: `kebab-case` (e.g., `memory-logger.py`, `rules-templates/`)
- **Command names**: `cdf:verb` or `cdf:verb-noun` (e.g., `cdf:rules`, `cdf:tdd`)
- **Hook scripts**: Descriptive verb-noun (`memory-logger.py`, `keyword-amplifier.py`)
- **Agent names**: Domain-specific nouns (`backend-architect`, `root-cause-analyst`)
- **Skill names**: Action-oriented (`intent-gate`, `failure-recovery`)

## Boundaries
- **Sacred files** (never modify directly):
  - `hooks/hooks.json` — changes require testing hook lifecycle
  - `scripts/lib/utils.py` — shared library, changes affect all hooks
  - `.claude-plugin/plugin.json` — version bumps must reflect actual changes
- **Never commit**: `.env`, `dev/active/` flow state files, `.claude/memory/daily/` logs, `*.local.json` settings
- **Review-required changes**: Any command/agent/skill definition changes (affects all plugin users), public hook interface changes
- **Memory files**: `.claude/memory/` is runtime state — never commit, never manually edit
