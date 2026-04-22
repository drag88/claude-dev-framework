---
name: generating-project-docs
description: "Auto-generates CLAUDE.generated.md from project rules when rules change or are missing"
---

# CLAUDE.md Generator Skill

Auto-generate `CLAUDE.generated.md` from project rules.

## When to Activate

- `.claude/rules/` exists but no `CLAUDE.md` or `CLAUDE.generated.md` in project root
- User asks "generate claude.md" or similar
- User asks "create project documentation"
- After `/cdf:rules generate` completes (auto-chain)

## What It Does

Executes the `/cdf:rules claudemd` behavioral flow. The command definition in `commands/rules.md` is the single source of truth for:
- What gets extracted from which rule files
- The output template and structure
- Line budget and guidelines

## Design Principles (Opus 4.7-aligned, from code.claude.com/docs/en/best-practices + Anthropic prompt-engineering docs)

- **Every line must pass**: "Would removing this cause Claude to make mistakes?" If not, cut it.
- **Target 80-180 lines** — under 200 is the documented sweet spot. First 200 lines get prioritized by Claude.
- **Progressive disclosure** — CLAUDE.md has essentials; `.claude/rules/` has details. Workflow content lives in `workflow.md`, not duplicated in root.
- **No duplication** — if content lives in `.claude/rules/` (auto-loaded), do not repeat it. Conflicts between files cause 4.7 to pick one arbitrarily.
- **Concrete and verifiable** — "Run `npm test` and paste the output" beats "test your changes." 4.7 self-filters vague checks.
- **No code style** — let linters handle formatting.
- **Open with a Role sentence** — One sentence anchoring tone and scope ("You are a senior X engineer working on Y..."). 4.7 responds well to a clear role.
- **Authorize tools and subagents explicitly** — Include a "Tool and subagent policy" block with `<use_parallel_tool_calls>`. 4.7's defaults are conservative.
- **Frame rules as positive imperatives** — "Use X" beats "Never Y." 4.7 wastes tokens on prohibitions and may pattern-match into them.
- **State scope explicitly on every rule** — "Apply to every component, including third-party wrappers" beats "apply to components." 4.7 will not silently generalize.
- **Tone down forceful language** — Avoid CAPS, MUST, CRITICAL, "ANY", "ALWAYS". Forceful negatives cause overcompliance and hostile reading.
- **Provide the why** behind non-obvious constraints. 4.7 generalizes correctly from explained constraints.
- **Use `@imports`** for top-level docs (`@README.md`) rather than restating them.

## What Belongs Where

| Content | Location | Why |
|---------|----------|-----|
| Role (one sentence) | `CLAUDE.md` | Anchors tone and scope cheaply |
| Overview, Quick Start, Critical Rules | `CLAUDE.md` | Essential context for every interaction |
| Tool and subagent policy + `<use_parallel_tool_calls>` | `CLAUDE.md` | Authorizes 4.7's conservative defaults |
| CDF tools available (routing table) | `CLAUDE.md` | Without explicit routing, 4.7 falls back to generic approaches instead of `/cdf:troubleshoot`, `/cdf:verify`, codebase-navigator, etc. — defeats the point of having CDF installed |
| Plans Format block (`<plans_instruction>`) | `CLAUDE.md` | XML processing tag — safest in guaranteed-load file |
| Commit message conventions | `CLAUDE.md` | 1-line pointer, high-frequency need |
| Imports (`@README.md`) | `CLAUDE.md` | Always-relevant top-level docs |
| Key directories | `CLAUDE.md` | Orientation for every task |
| Full workflow details (subagent strategy, verification, self-improvement, core principles) | `.claude/rules/workflow.md` | Auto-loads; eliminates duplication |
| CDF Agents routing table | `.claude/rules/workflow.md` | Auto-loads |
| Memory guidance | `.claude/rules/workflow.md` | Auto-loads |
| Architecture, patterns, tech stack | `.claude/rules/*.md` | Auto-loads; too detailed for CLAUDE.md |
| Path-scoped rules (frontend, API, DB) | `.claude/rules/*.md` with `paths:` frontmatter | Loads only when matching files are touched |

## Authoritative Rulebook (loaded at generation time)

**Step 0 of every generation**: Read `rules-templates/claudemd-4-7-rulebook.md` (vendored into CDF). Treat it as the single source of truth for 4.7 rules, anti-patterns, audit checklist, and the recommended skeleton. The Design Principles above become a fallback baseline only if the rulebook file is missing.

The point: generate a correct file by construction rather than auditing a possibly-wrong file after the fact. The rulebook is vendored into CDF so it travels with the framework — no dependency on a user-global skill being installed.

**Updating the rulebook**: Replace `rules-templates/claudemd-4-7-rulebook.md` with the latest version from `~/.claude/skills/prompt47/references/claudemd-4-7.md` and commit. The CDF version bump tracks the rulebook update.

**Generation flow:**
1. Read `rules-templates/claudemd-4-7-rulebook.md` as the rulebook. If missing, fall back to the embedded principles above.
2. Read the project's `.claude/rules/` files to extract overview, tech stack, quick-start commands, key directories, project-specific gotchas.
3. Construct each section of `CLAUDE.generated.md` against the rulebook. For every line, verify: positive framing? Explicit scope? Concrete and verifiable? The why is included where non-obvious?
4. Final pass: walk the rulebook's audit checklist (17 questions). Fix any "no" before writing.
5. Write the file.

## Related Commands

- `/cdf:rules claudemd` — manually trigger generation (behavioral spec lives here)
- `/cdf:rules generate` — regenerate rules (auto-chains to claudemd)
- `/prompt47 audit claudemd` (user-global) — independent audit if needed; not part of normal generation flow
