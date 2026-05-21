---
name: generating-agents-doc
description: "Auto-generates AGENTS.generated.md from project rules when rules change or are missing"
---

# AGENTS.md Generator Skill

Auto-generate `AGENTS.generated.md` from project rules. This is the Codex / GPT-5.5 counterpart to `CLAUDE.md`. Also picked up by Cursor, Aider, Jules, Devin, Zed, GitHub Copilot, and other coding agents that follow the AGENTS.md convention.

## When to Activate

- `.claude/rules/` exists but no `AGENTS.md` or `AGENTS.generated.md` in project root
- User asks "generate agents.md" or similar
- User asks "create Codex docs" or "set up AGENTS.md"
- After `/cdf:rules generate` completes (auto-chain alongside claudemd)
- After `/cdf:rules claudemd` completes when AGENTS.md is also missing (sibling auto-chain)

## What It Does

Executes the `/cdf:rules agentsmd` behavioral flow. The command definition in `commands/rules.md` is the single source of truth for:
- What gets extracted from which rule files
- Host-specific translation rules (strip `@file` imports, replace XML tags with prose, neutralize Claude-only tool names)
- The output template and structure
- Line budget and guidelines

## Design Principles (Codex-aligned, from `rules-templates/agentsmd-codex-rulebook.md`)

- **Single source of truth, two host-tailored outputs.** Same `.claude/rules/` feeds both `CLAUDE.md` and `AGENTS.md`. Translate framing per host, not facts.
- **Target 40-60 lines.** Codex caps the combined `AGENTS.md` chain at 32 KiB (`project_doc_max_bytes`), so root AGENTS.md stays slim and pushes per-package detail into nested `AGENTS.md`.
- **No `@file` imports.** Codex parses Markdown literally — `@README.md` reads as the literal string, not a transclusion. Inline a 2-line summary if you need the content.
- **No `<xml_tag>` blocks.** XML processing tags (`<plans_instruction>`, `<use_parallel_tool_calls>`) are Claude-specific. Codex sees the angle brackets as text.
- **Neutral tool vocabulary.** Avoid `Task tool`, `TeamCreate`, `Agent tool`, `subagent_type`. Use `subagent`, `parallel investigation`, `host skill`.
- **Nested `AGENTS.md` replaces path-scoped rules.** Codex does not honor `paths:` frontmatter. Polyglot repos push per-package conventions into `<package>/AGENTS.md`.
- **`AGENTS.override.md` is the overlay convention.** When a sibling agent ecosystem (Cursor, Aider) needs different framing, ship it as `AGENTS.override.md` rather than forking the root file.
- **Every line passes**: "Would removing this cause Codex to make mistakes?" If not, cut it.

## What Belongs Where

| Content | Location | Why |
|---------|----------|-----|
| Role (one sentence) | `AGENTS.md` | Anchors tone and scope cheaply |
| Overview, Quick Start, Critical Rules | `AGENTS.md` | Essential context for every interaction |
| Tool and subagent policy (prose only) | `AGENTS.md` | Codex needs explicit parallel-work authorization without XML |
| CDF tools available (compressed routing table) | `AGENTS.md` | Without explicit routing, Codex falls back to generic approaches |
| Commit message conventions | `AGENTS.md` | 1-line pointer, high-frequency need |
| Key directories | `AGENTS.md` | Orientation for every task |
| Project-specific gotchas | `AGENTS.md` | Non-obvious things any model would get wrong |
| `@file` imports | NOT in `AGENTS.md` | Codex parses literally |
| `<xml_tag>` blocks | NOT in `AGENTS.md` | No host semantics in Codex |
| Claude-specific tool names | NOT in `AGENTS.md` | Confuses Codex users |
| Full workflow detail | `.claude/rules/workflow.md` + nested `AGENTS.md` | Codex picks up per-directory context naturally |
| Architecture, patterns, tech stack | `.claude/rules/*.md` | Reference material; do not re-inline in AGENTS.md |
| Per-package conventions (polyglot repos) | `<package>/AGENTS.md` | Nested AGENTS.md replaces path-scoped rules |

## Authoritative Rulebook (loaded at generation time)

**Step 0 of every generation**: Read `rules-templates/agentsmd-codex-rulebook.md` (vendored into CDF). Treat it as the single source of truth for Codex AGENTS.md authoring, including the four core differences from CLAUDE.md (no `@file` imports, no XML-tag semantics, nested AGENTS.md replaces path-scoped rules, `AGENTS.override.md` overlay convention). The Design Principles above become a fallback baseline only if the rulebook is missing.

**Updating the rulebook**: Replace `rules-templates/agentsmd-codex-rulebook.md` with the latest version when Codex / OpenAI publishes new guidance, and commit. The CDF version bump tracks the rulebook update.

**Generation flow:**
1. Read `rules-templates/agentsmd-codex-rulebook.md` as the rulebook. If missing, fall back to the embedded principles above.
2. Read the project's `.claude/rules/` files to extract overview, tech stack, quick-start commands, key directories, project-specific gotchas.
3. Translate host-specific framing: strip `@file` imports, replace XML tags with prose, neutralize Claude-only tool names.
4. Construct each section of `AGENTS.generated.md` against the rulebook. Stay under 60 lines.
5. Final pass: walk the rulebook's audit checklist. Fix every "no" before writing.
6. Write the file.
7. For polyglot repos (multiple `package.json` / `pyproject.toml` / `go.mod`), also recommend nested `AGENTS.md` files per package and list the candidate paths.

## Related Commands

- `/cdf:rules agentsmd` — manually trigger generation (behavioral spec lives here)
- `/cdf:rules generate` — regenerate rules (auto-chains to claudemd + agentsmd)
- `/cdf:rules` (no subcommand) — full chain: generate rules, then both host files
