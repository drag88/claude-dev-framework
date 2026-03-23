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

## Design Principles (from code.claude.com/docs/en/best-practices)

- **Every line must pass**: "Would removing this cause Claude to make mistakes?" If not, cut it
- **Target < 200 lines** — first 200 lines are prioritized by Claude
- **Progressive disclosure** — CLAUDE.md has essentials; `.claude/rules/` has details
- **No duplication** — if content already lives in `.claude/rules/` (which loads automatically), do NOT repeat it in CLAUDE.md
- **Concrete and verifiable** — "Run `npm test` before committing" not "test your changes"
- **No code style** — let linters handle formatting; don't include style guides

## What Belongs Where

| Content | Location | Why |
|---------|----------|-----|
| Overview, Quick Start, Critical Rules | `CLAUDE.md` | Essential context for every interaction |
| Plans Format block (`<plans_instruction>`) | `CLAUDE.md` | XML processing tag — safest in guaranteed-load file |
| Commit message conventions | `CLAUDE.md` | 1-line pointer, high-frequency need |
| Key directories | `CLAUDE.md` | Orientation for every task |
| Full workflow details (8 subsections) | `.claude/rules/workflow.md` | Auto-loads; 45 lines saved |
| CDF Agents routing table | `.claude/rules/workflow.md` | Auto-loads; 20 lines saved |
| Memory guidance | `.claude/rules/workflow.md` | Auto-loads; saves duplication |
| Architecture, patterns, tech stack | `.claude/rules/*.md` | Auto-loads; too detailed for CLAUDE.md |

## Related Commands

- `/cdf:rules claudemd` — manually trigger generation (behavioral spec lives here)
- `/cdf:rules generate` — regenerate rules (auto-chains to claudemd)
