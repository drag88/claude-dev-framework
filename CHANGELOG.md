# Changelog

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
