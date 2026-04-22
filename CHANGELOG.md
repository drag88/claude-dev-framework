# Changelog

## [1.13.0] - 2026-04-22

### Breaking Changes
- Removed 10 persona-stub agents (backend-architect, frontend-architect, devops-architect, system-architect, security-engineer, performance-engineer, root-cause-analyst, python-expert, technical-writer, learning-guide). Opus 4.7 plays these roles from the `## Role` line in CLAUDE.md plus `xhigh` effort.
- Removed orchestrator commands `/cdf:flow` and `/cdf:workflow`. 4.7 plans multi-step workflows natively from a clear prompt.
- Removed dead-weight skills: `continuous-learning` (self-deprecated), `intent-gate` (redundant), `find-skills` (CLI dependency).
- Removed unreachable `contexts/` directory and `scripts/keyword-amplifier.py` (magic-string hidden modes; 4.7 has explicit `effort` levels).
- Removed component-count linter (in `pre-push-checks.py` and CI) — self-inflicted maintenance tax.

### Added
- Vendored `rules-templates/claudemd-4-7-rulebook.md` from the prompt47 reference. Generators read this bundled rulebook at generation time so generation is correct by construction (no cross-machine dependency on a separately-installed user-global skill).
- New required `## CDF tools available` section in generated `CLAUDE.md` template. Tells Claude which `/cdf:*` commands and agents to prefer for which tasks (debugging, pre-PR check, multi-file investigation, etc.). Without this section, Claude falls back to generic approaches instead of using CDF tools.
- New required `## Role` section in generated `CLAUDE.md` template (one-sentence anchor for tone and scope).
- New required `## Tool and subagent policy` section with `<use_parallel_tool_calls>` block (4.7's defaults are conservative).
- Cross-machine setup section in `README.md` (three-tier state model, bootstrap sequence, versioning + rollback).

### Changed
- Workflow content now lives only in `rules-templates/workflow-template.md` and `.claude/rules/workflow.md`. Generated `CLAUDE.md` contains a one-line pointer instead of duplicating the content (eliminates conflict risk).
- Toned down forceful CAPS/MUST/MANDATORY language across `task.md`, `tdd.md`, `verify.md`, `rules.md`, `docs.md` (4.7 over-complies on forceful imperatives).
- Self-improvement loop now writes to auto-memory `feedback_*.md`, never autonomously to `.claude/rules/` (eliminates rule sprawl).
- `analyze-codebase.py`: fast-exit when `.claude/rules/` already exists (skips file-tree walk and project-type detection on every SessionStart).
- `comment-checker.py`: skip files >500 lines.
- `pre-push-checks.py`: warn-only, never `decision: block`. Gating belongs in CI.
- `plugin.json` description: dropped literal counts (no longer needs maintenance per add/remove).

### Stats
- 49 files changed, +756 / -2480 (net -1724 LOC).
- Commands: 23 → 21. Agents: 23 → 12. Skills: 27 → 24.

## [1.11.0] - 2026-03-06

### Breaking Changes
- Removed `starhub-presentation` and `social-writing` skills (personal/company content)
- Removed `project-memory` skill (superseded by Claude native auto-memory)
- Removed `memory-init` and `memory-summarize` hooks (redundant with native auto-memory)
- Skill count: 18 -> 15, Hook count: 11 -> 9

### Added
- Error logging to all hook scripts (`~/.cdf-logs/hook-errors.log`)
- `scripts/health-check.py` for plugin validation
- CI workflow (`.github/workflows/validate.yml`)
- LICENSE (MIT) and CHANGELOG.md
- Progressive disclosure: oversized skills and agents split into `references/` subdirectories
- Keyword amplifier deactivation mechanism ("normal"/"reset" keywords)

### Changed
- CLAUDE.md trimmed from ~80 lines to ~50 lines (essential context only)
- README.md restructured to ~175 lines (removed duplicate tables)
- Context modes trimmed to under 50 lines each
- 5 bloated agent files trimmed to under 55 lines each (templates moved to `agents/references/`)
- 3 oversized SKILL.md files split: frontend-slides (1097->186), frontend-patterns (692->113), backend-patterns (675->107)
- Keyword amplifier: removed generic triggers (search, find, quick, fast, analyze)
- Comment checker threshold raised from 25% to 35% for partial content
- `memory-logger.py` now self-sufficient (lazy-creates directories)

### Fixed
- Dead links to `INDEX.md` changed to `README.md`
- Deleted orphaned `flow-verify-gate.py` script
- Count mismatches resolved across all documentation files
- Removed personal references (email, Obsidian paths) from framework files
- Empty `docs/solutions/` scaffolding directories removed

## [1.10.0]

### Added
- Context modes (dev, review, research)
- MCP server configuration templates
- Flow checkpoint and session save hooks
- Memory system with daily activity logs

### Note
- Prior versions were not tracked in a changelog
