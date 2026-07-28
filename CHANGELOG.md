# Changelog

## [2.1.0] - 2026-07-29

Framework-wide unhobbling pass for the Claude 5 generation, applying Anthropic's "The new
rules of context engineering for Claude 5 models" (the Claude Code team removed over 80% of
their system prompt for these models with no eval loss). Rebased onto 2.0.0, so the pass
covers the surfaces that survived the compound-engineering delegation.

### Breaking Changes
- **Retired `rules-templates/claudemd-4-7-rulebook.md`** in favor of the version-neutral
  `rules-templates/claudemd-rulebook.md`, rewritten for current models: judgement over rules,
  one home per fact, gotchas over derivable content, progressive disclosure, no
  tool/subagent authorization boilerplate, and a reasoning-extraction caution. Generators and
  references updated; the update path is now "edit the vendored rulebook against Anthropic's
  current docs" (the prompt47 dependency is gone).
- **Generated `CLAUDE.md` drops the `## Tool and subagent policy` section and
  `<use_parallel_tool_calls>` block** — current models parallelize and dispatch subagents
  natively; the generator now treats that boilerplate as a deletion target. The 2.0.0 Model
  Routing and Communication sections stay. The Codex/`AGENTS.md` path keeps prose
  authorization deliberately (no XML).

### Changed
- **rules-templates**: deleted stale Haiku/Sonnet/Opus model-routing and context-management
  sections (`performance.md`), the duplicated `## Critical Rules` tails restating each
  project-type file's own content, derivable tutorial bulk (React skeletons, HTTP tables,
  Dockerfiles, import-order rules linters own), fictional CODEOWNERS/SLO placeholder data,
  and contradictory checklists `extended-rules.md` itself condemns. `workflow-template.md`
  slimmed ~70%: no more TeamCreate reference, `<use_parallel_tool_calls>` block,
  spawn-pattern few-shots, self-improvement-loop section, or triple-stated plan-mode
  thresholds. `extended-rules.md` de-versioned.
- **commands**: removed the remaining persona/MCP-Integration scaffolding, boilerplate
  `## Key Patterns`/`## Tool Coordination` sections, and fabricated example transcripts from
  the native (non-delegated) commands. `verify.md` collapses its triple-stated pipeline and
  now detects the project's toolchain instead of assuming npm/eslint/jest; `tdd.md` collapses
  its triple-stated RED/GREEN/REFACTOR.
- **agents**: deduplicated against the skills they already load (`tdd-guide`,
  `e2e-specialist`, `quality-engineer`), converted rigid numbered recipes to judgement
  framing, and cut the generic OWASP tutorial bulk from `security-checklists.md` while
  keeping the Pre-Landing Review Patterns intact (file since removed upstream in 2.0.0 where
  applicable).
- **skills**: engineering skills updated — stale persona routing retitled to role framing,
  numeric coverage/file-size absolutes replaced with repo-calibrated guidance, emoji status
  rituals and duplicated ASCII/prose restatements removed (`tdd-workflow`,
  `coding-standards`, `frontend-design`, `retro`); Stop-hook nudge language neutralized.
- **All current-guidance "Opus 4.7" references made version-neutral** across README,
  QUICKSTART, CLAUDE.md, AGENTS.md, commands, skills, agents, and the Codex rulebook
  (changelog history untouched).

### Fixed
- CDF's own `CLAUDE.md` and `AGENTS.md` still carried `TeamCreate` +
  `<use_parallel_tool_calls>` boilerplate; both are gone everywhere now, including the
  embedded templates in `commands/rules.md`.

## [2.0.0] - 2026-07-02

### Breaking Changes
- Engineering-loop commands now delegate to and require the compound-engineering plugin.
- Native duplicated flows for implementation, brainstorming, planning, troubleshooting, plan review, review, commit, and PR delivery were removed.
- Knowledge base is unified on `compound-engineering:ce-compound` → `docs/solutions/` + `CONCEPTS.md`.
## [1.14.0] - 2026-05-21

### Added
- **Codex adapter** — first-class Codex support alongside Claude Code. `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, and a generated `AGENTS.md` let Codex load the same `/cdf:*` workflows. Marketplace metadata is host-neutral so a single repo serves both runtimes.
- **`/cdf:rules agentsmd` subcommand** — generates `AGENTS.generated.md` from `.claude/rules/` for Codex, GPT-5.5, Cursor, Aider, Jules, and similar agents. `/cdf:rules generate` now auto-chains `claudemd` + `agentsmd` so `CLAUDE.md` and `AGENTS.md` stay in sync from one source.
- **Codex authoring rulebook** at `rules-templates/agentsmd-codex-rulebook.md` covering the four authoring differences from `CLAUDE.md`: no `@file` imports, no XML-tag semantics, nested `AGENTS.md` replaces path-scoped rules, 32 KiB combined chain budget.
- **`tuning-coding-agent-codebases` skill** — packages Anthropic's large-codebase best practices as an auditable workflow (inventory, score, refactor).
- **`rules-templates/extended-rules.md`** — opt-in reference for the community 12-rule template, with verdicts (Default / Keep / Optional / Skip / Reject) flagging three rules as anti-patterns on Opus 4.7 (forced summaries, unenforceable token budgets, wrong-layer API guidance).
- **`/cdf:plan-review`** + host adapter guidance — pre-implementation plan gauntlet, and clearer doc story for which workflows belong to which host.

### Changed
- **Critical Rules core grows from 4 to 6** — adds *"Surface conflicts, don't average them"* and *"Fail loud"*. Each rule now carries its **Why** per the 4.7 rulebook.
- **CDF's own `AGENTS.md` cleaned up** — removed `.Codex/rules/`, `@README.md`, `TeamCreate`, `Task` tool references, and the `<use_parallel_tool_calls>` XML block (Codex doesn't honor any of these).
- **`visual-explainer` skill synced upstream v0.5.1 → v0.7.1** — new vector-based multi-diagram zoom/pan engine, fullscreen background-color fix, `share` command renamed to `share-page`, "Diagram Types" section consolidated back into `SKILL.md`, and the bare `<pre class="mermaid">` anti-pattern is now called out explicitly. CDF's "Activates"-style description wording is preserved for skill-loader consistency.
- **Count-bearing docs synced** — 25 skills, 17 rule templates, version refs bumped to 1.14.0.

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
