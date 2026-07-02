---
name: tuning-coding-agent-codebases
description: Audits and refactors a codebase's coding agent configuration (CLAUDE.md, .claude/settings.json, skills, hooks) against Anthropic's published best practices. Primary use is rewriting an existing CLAUDE.md so the root holds only pointers and gotchas under 200 lines, conventions move into subdirectory CLAUDE.md files, procedures migrate from CLAUDE.md into skills, and rules added to compensate for older models get deleted. Also audits .claude/settings.json permission denies, scoped test and lint commands, skill bloat, hook obsolescence against the Claude Code changelog, and the decision matrix for CLAUDE.md vs skills vs hooks vs plugins vs MCP. Works on any codebase size, not just monorepos. Use this skill when the user asks to audit, clean up, refactor, rewrite, or improve CLAUDE.md or Claude Code config, says the agent feels slow or scattered in this repo, runs a periodic config review, sets up a coding agent in a new repo, or asks 'is my setup right'. Trigger even when the user says only 'clean up my CLAUDE.md' or 'review my Claude Code config'.
---

# Tuning coding agent codebases

Audits and refactors a codebase's coding agent configuration against Anthropic's published best practices. Works on any codebase size. The primary intervention is rewriting an existing CLAUDE.md so it follows the best practices, not greenfield setup.

Source: Anthropic, "How Claude Code works in large codebases: best practices and where to start." https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start

## Core principle

A coding agent's usefulness in a codebase is bounded by its ability to find the right context. Claude Code uses agentic search (file traversal, grep, reference following), not RAG embeddings. No staleness risk, but the setup work falls on the codebase. The codebase has to be legible to the agent the same way it has to be legible to a new engineer.

Setup time is not overhead. It is the work.

## Decision tree

| Situation | Workflow |
|-----------|----------|
| CLAUDE.md exists but feels bloated, stale, or has not been touched in months. User asks to clean it up, audit, refactor, or rewrite. | **A. Audit and refactor existing setup.** Most common case. |
| Agent has plateaued in this repo: slow responses, context overflow, repeated mistakes, missing context. | **B. Diagnose plateau.** |
| Quarterly or post-model-release review. | **C. Periodic review.** |
| No CLAUDE.md or .claude/ in the repo. | **D. Greenfield setup.** |

When in doubt, run A.

## Workflow A. Audit and refactor existing setup

### Step 1. Inventory

Read in this order, no shortcuts:

```bash
# 1. Every CLAUDE.md in the tree, with line counts
find . -type f \( -name 'CLAUDE.md' -o -name 'CLAUDE.local.md' \) \
  -not -path '*/node_modules/*' -not -path '*/.git/*' \
  -exec wc -l {} + | sort -n

# 2. Full chain Claude Code would load from cwd up
d=$(pwd); while [ "$d" != "/" ]; do
  [ -f "$d/CLAUDE.md" ] && echo "$d/CLAUDE.md ($(wc -l < "$d/CLAUDE.md") lines)"
  d=$(dirname "$d")
done

# 3. Settings, skills, hooks, rules
find . -path '*/.claude/settings*.json' -exec cat {} \;
find .claude/skills -name SKILL.md -exec wc -l {} + | sort -n 2>/dev/null
find .claude/rules -name '*.md' 2>/dev/null
jq '.hooks // empty' .claude/settings.json 2>/dev/null
```

Then read every file the inventory surfaced. Do not score until you have read them.

### Step 2. Score against the rules

For each file, find the violations below. Cite file:line for every finding.

**Root CLAUDE.md violations**
- Over 200 lines. Anthropic's official ceiling is 200; HumanLayer's well-tested target is 60. Past 200 you lose adherence; past 1000 behavior becomes unpredictable.
- Procedural content (numbered multi-step lists). Belongs in a skill. Grep: `grep -nE '^\s*[0-9]+\.' CLAUDE.md`.
- "How to do task X in general" content. Belongs in a skill.
- Long command lists that mirror package.json. Replace with a one-line pointer.
- Personal preferences mixed with project facts. Move preferences to `~/.claude/CLAUDE.md`.
- Multiple subdirectories' conventions stuffed into root instead of pointing to nested files.
- Time-aged content (specific versions, dates that have passed).

**Subdirectory CLAUDE.md violations**
- Missing for subdirectories with different languages, build systems, or test runners.
- Duplicates root content instead of carrying additive local detail.

**.claude/settings.json violations**
- File missing or only in `settings.local.json` (per-developer) when it should be in version-controlled `settings.json`.
- Missing deny rules for `node_modules/`, `vendor/`, `.venv/`, `dist/`, `build/`, `.next/`, secrets, large data files.
- Missing `disableBypassPermissionsMode: "disable"` for shared projects (lets any developer run `--dangerously-skip-permissions`).
- Overly broad allow rules like `Bash(*)` or `Bash(npm *)` for destructive commands.

**Skills violations**
- Skill with vague description that will not trigger ("Helps with stuff").
- Skill description over 1,536 characters (gets truncated, key trigger phrases lost).
- Destructive skill (`deploy`, `release`, `push`, `delete`) without `disable-model-invocation: true`.
- Skill that duplicates content already in CLAUDE.md.
- Skill named with reserved words `claude` or `anthropic`.
- Skill orphan: no `owner:` field, no review cadence, not invoked in 6+ months.

**Hooks violations**
- Hook compensates for a limitation Claude Code now handles natively (see Reference: Hook obsolescence).
- Hook enforces something that should be a `permissions.deny` rule (hard enforcement belongs in settings, not hooks).
- Hook in `settings.json` but the script it points at does not exist.

**Old-model-compensating rules in CLAUDE.md** (grep these specifically):

```bash
grep -rniE 'break (refactors|changes|edits)? into single[- ]file|echo (the )?plan (back )?before|do not modify multiple files at once|always run tests before changing|verify by reading the file (again|first)|read the entire file before|output (the |a )?full file|do not refactor|ask before (making|doing) any change|narrate (your )?plan|confirm (your understanding|the task) before|work one (file|change|task) at a time|do not parallelize|read (every|all) (file|test) first|always summarize what you did|re[- ]read the file after editing' CLAUDE.md .claude/rules/ 2>/dev/null
```

Every match is a candidate for deletion. These compensated for Claude 3 / 3.5 era limitations. Sonnet and Opus 4.x handle the underlying behavior natively. Flag, do not auto-delete; show the user each match and let them approve.

### Step 3. Produce the audit report

Output a single markdown report. Three sections, no preamble:

```markdown
## Findings
- `CLAUDE.md:1-200` Oversized at 280 lines. Contains 4 procedural sections (lines 50-130) and a 30-item command list (lines 180-210) that should not be in CLAUDE.md.
- `CLAUDE.md:42` "Always break refactors into single-file changes" compensates for an old-model limitation. Sonnet/Opus 4.x handle multi-file refactors natively. Delete.
- `services/api/` Missing CLAUDE.md. The directory has a different build system (Poetry) and test runner (pytest) than root.
- `.claude/settings.json` No `permissions.deny` for `node_modules`, `dist`, or `.venv`. Agent reads these on grep, wasting context.
- `.claude/skills/deploy/SKILL.md` Missing `disable-model-invocation: true`. Risk of autonomous deployment.

## Recommended changes
- Refactor `CLAUDE.md` from 280 -> ~80 lines. Move lines 50-130 to a new `.claude/skills/release/SKILL.md`. Move lines 180-210 to a pointer (`See @package.json for scripts`).
- Create `services/api/CLAUDE.md` with Poetry/pytest conventions. Cite the path from root CLAUDE.md as a pointer.
- Add deny rules to `.claude/settings.json`.
- Add `disable-model-invocation: true` to the deploy skill frontmatter.

## Migration plan (ordered)
1. Apply `.claude/settings.json` deny rules (zero-risk, immediate noise reduction).
2. Create `services/api/CLAUDE.md` (additive, no breakage).
3. Add `disable-model-invocation: true` to deploy skill.
4. Extract release procedure from CLAUDE.md into the new skill.
5. Slim root CLAUDE.md.
6. Delete old-model-compensating lines.
```

Show the report. Wait for approval before any edit.

### Step 4. Apply changes

In the order above. For each file modified, show a diff before writing. Stop on the first rejection.

Concrete refactoring patterns to follow:

**Pattern: Extract procedure to skill.**

Before (in CLAUDE.md):
```markdown
## Deploying to production
1. Run `npm test` and ensure all pass
2. Run `npm run build`
3. Bump version in package.json (semver: patch=fix, minor=feature, major=breaking)
4. Commit with message "release: vX.Y.Z"
5. `git tag vX.Y.Z && git push --tags`
6. Watch the GHA pipeline; if it fails, see docs/deploy.md
7. Smoke-test `/health` endpoint
8. Post in #releases with diff link
```

After (CLAUDE.md keeps one line):
```markdown
- Deploys: run `/deploy` (skill at `.claude/skills/deploy/`).
```

And `.claude/skills/deploy/SKILL.md`:
```yaml
---
name: deploy
description: Deploy the application to production. Use when the user asks to deploy, release, or ship a version.
disable-model-invocation: true
allowed-tools: Bash(npm run *) Bash(git tag *) Bash(git push *)
---

## Pre-flight
!`npm test -- --silent && npm run build`

## Steps
1. Bump version (semver: patch=fix, minor=feature, major=breaking)
2. `git tag v${VERSION} && git push --tags`
3. Monitor GHA at https://github.com/.../actions
4. Smoke-test `/health` post-deploy
5. Post in #releases
```

**Pattern: Collapse command list to pointer.**

Before:
```markdown
## Commands
- `npm run lint` - runs eslint
- `npm run lint:fix` - runs eslint with --fix
- `npm run test` - runs all tests
- `npm run test:watch` - runs tests in watch mode
- `npm run test:e2e` - runs end-to-end tests
- `npm run typecheck` - runs tsc --noEmit
- `npm run format` - runs prettier --write
- `npm run format:check` - runs prettier --check
[20 more lines]
```

After:
```markdown
- Available scripts: see @package.json.
- Required before commit: `pnpm lint:fix && pnpm typecheck`.
```

**Pattern: Promote cross-team policy to user-level.**

Personal preferences ("I like 2-space indents") belong in `~/.claude/CLAUDE.md`, not in the project CLAUDE.md. Org-wide policies ("never commit secrets") belong in managed settings (`/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS). Project CLAUDE.md is for project facts only.

**Pattern: Split monorepo by package.**

Root holds only what applies across every package. Per-package CLAUDE.md carries language- and tool-specific rules:

```
CLAUDE.md (root, ~80 lines max)
packages/api/CLAUDE.md       # Python, Poetry, pytest conventions
packages/web/CLAUDE.md       # TypeScript, Next.js, Tailwind tokens
packages/shared/CLAUDE.md    # Zero deps, 100% coverage requirement
infra/CLAUDE.md              # Terraform plan-before-apply rule
```

For monorepos where developers should not load other teams' CLAUDE.md when working from root, add to `.claude/settings.local.json`:
```json
{ "claudeMdExcludes": ["**/legacy/**/CLAUDE.md", "packages/sandbox/**/CLAUDE.md"] }
```

### Step 5. Verify

```bash
# Root CLAUDE.md should now be small.
wc -l CLAUDE.md

# Per-subdirectory files should exist where flagged.
find . -name CLAUDE.md -not -path '*/node_modules/*' -exec wc -l {} +

# Run /doctor in a Claude Code session to check skill description budget.
echo "Manual: run /doctor and /context all inside a session."
```

Start a Claude Code session in a subdirectory and ask a question grounded in the local CLAUDE.md. Confirm the answer is correct and concise.

## Workflow B. Diagnose plateau

Walk the table in order. The first three causes account for most plateaus.

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Slow first response every session | Root CLAUDE.md > 200 lines or many `@`-imports loading at launch | Trim root, move imports behind path-scoped rules or skills |
| Agent ignores explicit rules | File > 200 lines, contradictory rules across nested files, or rule is procedural (soft compliance only) | Audit with `/memory`; convert hard requirements to hooks |
| Context overflow mid-task | Skills + CLAUDE.md + history exhausting window | Add `context: fork` to heavy skills; lower per-skill budget |
| Repeated "obvious" mistakes | Rule treated as one option among many because it's procedural, not enforced | Hook for hard enforcement; skill for guided procedure |
| Skills don't auto-activate | Description lacks trigger keywords or exceeds 1,536 chars | Front-load description with trigger phrase; run `/doctor` |
| Cross-team CLAUDE.md loading from monorepo root | No `claudeMdExcludes` | Add excludes in `settings.local.json` |
| Stale env after `--resume` | Volatile context replays as stale | Move SHAs and timestamps to a SessionStart hook |
| Skill stops mattering after first turn | Loaded once, model preferring other strategies | Strengthen description; consider hook for deterministic enforcement |
| Sudden cost spike | Auto-memory ballooning or skill descriptions filling budget | `/memory` audit; set low-priority skills to `"name-only"` via `skillOverrides` |
| Wrong starting directory | Agent loads ancestor CLAUDE.md from unrelated team | Restart Claude in the actual working subdirectory |

## Workflow C. Periodic review (3-6 months)

Run after every major model release, or quarterly. Audit:

- **Hooks that compensated for old limitations.** Cross-reference against the Claude Code CHANGELOG. The Perforce hook (enforcing `p4 edit`) became redundant in 2.1.98 when `CLAUDE_CODE_PERFORCE_MODE` shipped. Effort-detection hooks became redundant when `$CLAUDE_EFFORT` shipped. Terminal-notification wrappers became redundant when `terminalSequence` hook output shipped in 2.1.141. Delete obsolete hooks; do not let them accumulate.
- **Skills built around specific failure modes.** Still relevant? If the model fixed the underlying issue, retire the skill.
- **CLAUDE.md "do X carefully" rules.** Re-test by removing the rule for a session and seeing whether the agent does X carefully on its own. If yes, delete.
- **Skill description text.** Run `/doctor` to check budget overflow. Trim or downgrade low-priority skills to `name-only`.
- **DRI assignment.** Confirm one person still owns settings, skills, and CLAUDE.md conventions. Without a DRI, configuration goes stale.

## Workflow D. Greenfield setup

Only when no CLAUDE.md or `.claude/` exists. Build in this order:

1. **Root CLAUDE.md** (under 80 lines). Top-level layout as pointers, critical gotchas. Template at the end of this skill.
2. **Per-subdirectory CLAUDE.md** where languages or build systems differ. Local conventions only.
3. **.claude/settings.json** with deny rules. Template below.
4. **LSP for symbol-level navigation.** Install a code intelligence plugin and the language server binary.
5. **Codebase map** (`MAP.md` or root CLAUDE.md section) only if directory layout is non-conventional.
6. **Skills** for any procedure you would otherwise paste repeatedly.
7. **Hooks** for behavior that must run regardless of model choice.
8. **Plugin** if multiple teams will use the same setup.

## Reference

### CLAUDE.md size targets

- **Under 60 lines** - well-tuned root (HumanLayer benchmark).
- **Under 200 lines** - Anthropic's official ceiling. *"Longer files consume more context and reduce adherence."*
- **~500 lines** - workable only with careful structure (path-scoped rules, nested files).
- **Over 1000 lines** - model skimming behavior. Refactor immediately.

### What belongs where

CLAUDE.md takes facts that apply across most sessions. Skills take procedures. Hooks take enforcement. Settings take permissions. Plugins take distribution.

| Content | Belongs in |
|---------|-----------|
| "Auth lives in `src/lib/auth.ts`" | CLAUDE.md |
| "Use 2-space indentation" (if no formatter enforces it) | CLAUDE.md |
| "Use 2-space indentation" (if Prettier enforces it) | Replace with `Run \`pnpm lint:fix\` after edits` in CLAUDE.md |
| "How to scaffold a new API endpoint" | Skill |
| "How to deploy to production" | Skill with `disable-model-invocation: true` |
| "Run `make lint` before every commit" | Hook (`PreToolUse` on `Bash(git commit *)`) |
| "Never run `curl` to fetch secrets" | Settings deny rule |
| "Append Jira ticket to every commit message" | Hook |
| "Postgres uses soft-delete with `deleted_at`" | CLAUDE.md |
| "Code review checklist (20 items)" | Skill (`/review`) |

### Old-model-compensating phrases to flag

Grep for these in CLAUDE.md and `.claude/rules/`. Each is a candidate for deletion on modern models.

1. "Break refactors into single-file changes"
2. "Echo the plan before editing"
3. "Do not modify multiple files at once"
4. "Always run tests before changing code"
5. "Verify by reading the file"
6. "Output the full file when editing"
7. "Do not refactor existing code"
8. "Read the entire file before making changes"
9. "Confirm your understanding before starting"
10. "Work one task at a time"
11. "Do not run more than one bash command per turn"
12. "Always plan step-by-step before any tool use"
13. "Never assume anything about the codebase"
14. "Ask before making any change"
15. "Narrate your plan to the user"
16. "Copy the existing pattern exactly"
17. "Do not parallelize tool calls"
18. "Read every test before changing code"
19. "Always summarize what you did at the end"
20. "Re-read the file after editing to verify"

### Hook obsolescence catalog

Specific obsolete patterns with the Claude Code version that retired each.

- **`p4 edit` enforcement hook.** Retired by `CLAUDE_CODE_PERFORCE_MODE` in 2.1.98 (April 2026).
- **Effort-detection hook.** Retired by `$CLAUDE_EFFORT` env var and `effort.level` hook JSON field.
- **Custom desktop-notification wrapper hooks.** Retired by `terminalSequence` hook output in 2.1.141.
- **Custom retry logic on hook denial.** Retired by `continueOnBlock` for `PostToolUse` in 2.1.139.
- **Shell-quoting workaround hooks.** Retired by exec-form `args: string[]` in 2.1.139.
- **Path-injection hooks for MCP servers.** Retired by `CLAUDE_PROJECT_DIR` in MCP stdio env (2.1.139).
- **Stop-hook manual loop prevention.** Retired by `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` (default 8).
- **Echo-plan-before-editing hooks.** Obsolete; Sonnet/Opus 4.x plan reliably without them.
- **Single-file-edit enforcement hooks.** Obsolete; multi-file refactors handled natively.
- **Branch-name injection via UserPromptSubmit.** Redundant; status line and SessionStart cover this.

When auditing hooks, check each against the [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) for native equivalents.

### Skill extraction recipes

Content categories that almost always belong in a skill, not CLAUDE.md.

- **Deployment procedures.** Skill with `disable-model-invocation: true`.
- **Testing playbooks** (TDD recipes, snapshot-test policies, E2E setup).
- **Code-review checklists.** Skill at `/review`.
- **Migration recipes** ("Next.js 13 -> 14", "Prisma 4 -> 5"). Skill with `$ARGUMENTS` for versions.
- **Debugging workflows** ("when you see error X, check Y").
- **Domain-specific writing guides** (voice and tone for blog posts, marketing copy).
- **Onboarding rituals** ("first time on this repo, run these checks").

Conversion test: *"Create a skill when you keep pasting the same instructions, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact."*

### Harness component decision matrix

| Component | When it loads | Best for | Common confusion |
|-----------|---------------|----------|------------------|
| CLAUDE.md | Every session | Project facts and conventions | Procedural content (belongs in a skill) |
| Hooks | Event-triggered | Hard enforcement, automation | Soft guidance (belongs in CLAUDE.md or skill) |
| Skills | On demand | Reusable procedures | Loading everything into CLAUDE.md |
| Plugins | Always (once configured) | Cross-team distribution | Tribal setups that never get packaged |
| MCP servers | Always (once configured) | External tools and data | Building before basics work |
| LSP | Always (once configured) | Symbol-level navigation | Assuming it is automatic |
| Subagents | When invoked | Splitting exploration from editing | Running both in the same session |

### Minimal .claude/settings.json

```json
{
  "permissions": {
    "deny": [
      "Read(node_modules/**)",
      "Read(vendor/**)",
      "Read(.venv/**)",
      "Read(dist/**)",
      "Read(build/**)",
      "Read(.next/**)",
      "Read(**/.env)",
      "Read(**/.env.*)",
      "Read(secrets/**)",
      "Bash(curl *)",
      "Bash(wget *)"
    ],
    "ask": [
      "Bash(git push *)",
      "Bash(npm publish *)",
      "Bash(git push --force *)"
    ],
    "disableBypassPermissionsMode": "disable"
  }
}
```

For shared projects, `disableBypassPermissionsMode: "disable"` is the single most important field. Without it, any developer can bypass every safety rule with `--dangerously-skip-permissions`.

### Polyglot monorepo pattern

Root CLAUDE.md (~80 lines): top-level layout, cross-cutting rules (conventional commits, secret-handling, ADR location).

Per-package CLAUDE.md: language-specific conventions only.

Path-scoped rules in `.claude/rules/` for cross-file rules within a language:

```yaml
---
paths: ["packages/api/**/*.py"]
---
- Use `from typing import Annotated`.
- Pydantic v2 only.
- Test files mirror source: `packages/api/src/foo.py` -> `packages/api/tests/test_foo.py`.
```

Add `claudeMdExcludes` in `settings.local.json` to keep developers from loading other teams' files when starting at repo root.

### Root CLAUDE.md template

```markdown
# Project name

One paragraph: what this codebase is and who uses it.

## Top-level layout
- services/api: backend API service. See services/api/CLAUDE.md.
- services/web: web frontend. See services/web/CLAUDE.md.
- packages/shared: cross-service utilities. See packages/shared/CLAUDE.md.
- infra: deployment and infra config. See infra/CLAUDE.md.

## Critical gotchas
- Migrations run against a shared staging DB. Coordinate before applying.
- The Stripe webhook signing secret rotates monthly. Read services/api/CLAUDE.md before touching billing.
- Never push directly to main. `git push origin main` is denied at the GitHub branch protection layer.

## Commands
- Pre-commit: `pnpm lint:fix && pnpm typecheck`.
- See @package.json for the full script list.

## Procedures
- Deploys: `/deploy`.
- Code review: `/review`.
- Schema migrations: `/migrate`.
```

That is the entire shape. Add nothing else to root unless it qualifies as a project fact applicable to most sessions.

### Codebase map example

For repos with non-conventional layout. Drop at root as `MAP.md` or fold into the root CLAUDE.md "Top-level layout" section. Real example from enso-org/enso:

```markdown
* `app/` - Desktop app (Electron), GUI (Vue, Dashboard is React), ydoc server, markdown/table CodeMirror grammars, Rust->WASM bindings. pnpm monorepo.
* `engine/` - The Enso language engine. Mixed Scala/Java under `sbt`. Runtime uses GraalVM Truffle.
* `lib/rust/` - Rust workspace libraries (parser, prelude, reflect/metamodel, zst). Some crates ship to crates.io.
```

Each line is map plus reason. ~15 lines covers the entire top level.

### Governance

The minimum-viable unit is one DRI: a single person with authority over `.claude/settings.json`, the plugin marketplace, CLAUDE.md conventions, and the team's installed set of skills and hooks. Without a DRI, configuration goes stale and bottoms-up adoption fragments.

For larger orgs, the role is an "agent manager" (hybrid PM/engineer). Anthropic's rollout pattern: pilot with 5-10 developers for two weeks -> expand to a department -> org-wide via managed settings deployed through MDM.

Skills governance: separate the person who writes a skill from the person who approves it for production use. Require an `owner:` field on every project skill, even though it is not enforced by the runtime.

## Source attribution

Anthropic, "How Claude Code works in large codebases: best practices and where to start." https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start

Supporting research: Claude Code official memory docs (https://code.claude.com/docs/en/memory), skills docs (https://code.claude.com/docs/en/skills), settings docs (https://code.claude.com/docs/en/settings), and the Claude Code CHANGELOG. Community sources cited inline.

This skill is the operational pass on the article. The article is the canonical source.
