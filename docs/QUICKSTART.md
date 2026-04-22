# CDF Quickstart

## The 30-Second Version

CDF gives you slash commands. Type them and Claude does the rest.

```
/cdf:implement "add feature X"     Build something
/cdf:ship                          Merge, test, review, push, open PR
/cdf:troubleshoot "it's broken"    Fix something
```

Everything else is optional until you need it.

---

## How to Think About CDF

CDF has four layers. You only need the first one to start.

**Layer 1 — Commands** (you type these)
Slash commands that trigger specific workflows. The command handles tool selection, agent activation, and quality checks automatically.

**Layer 2 — Agents** (real-expertise subagents you can invoke)
Specialized agents like `codebase-navigator`, `library-researcher`, `quality-engineer`, `e2e-specialist`, `tdd-guide`, `requirements-analyst`, `socratic-mentor`, `media-interpreter`. Persona-stub agents (security-engineer, backend-architect, etc.) were removed in the leanness pass — Opus 4.7 plays those roles from the Role line in your CLAUDE.md plus `xhigh` effort.

**Layer 3 — Skills** (trigger automatically)
Background behaviors like coding standards enforcement, failure recovery, and intent classification. You don't interact with these — they just run.

**Layer 4 — Hooks** (run on events)
Lifecycle scripts that fire on session start, before/after tool use, and on stop. Handles codebase analysis, context injection, and quality gates.

---

## Command Cheat Sheet

### Build

| Command | When to use |
|---------|-------------|
| `/cdf:implement "X"` | Build a feature from scratch |
| `/cdf:tdd` | Build with test-first workflow |
| `/cdf:improve src/` | Refactor existing code |

### Ship

| Command | When to use |
|---------|-------------|
| `/cdf:ship` | One-command release: merge → test → review → PR |
| `/cdf:git commit` | Just commit with a smart message |
| `/cdf:verify --mode pre-pr` | Run all quality checks without shipping |

### Think

| Command | When to use |
|---------|-------------|
| `/cdf:design "system X"` | Technical architecture (how to build it) |
| `/cdf:brainstorm "problem"` | Requirements discovery (what to build) |
| `/cdf:estimate "task"` | Effort estimation |
| Write a clear prompt + `xhigh` effort | Generate implementation steps from a spec (4.7 plans natively) |

### Fix

| Command | When to use |
|---------|-------------|
| `/cdf:troubleshoot "issue"` | Diagnose and fix a bug |
| `/cdf:analyze src/` | Code quality, security, performance audit |
| `/cdf:test` | Run tests with coverage analysis |
| `/cdf:e2e` | End-to-end testing with Playwright |

### Understand

| Command | When to use |
|---------|-------------|
| `/cdf:explain "concept"` | Explain code or concepts clearly |
| `/cdf:research "topic"` | Deep web research with sources |
| `/cdf:docs plan` | Generate documentation |

### Orchestrate

| Command | When to use |
|---------|-------------|
| `/cdf:task "complex thing"` | Break down and delegate with agents |
| `/cdf:task --breakdown "X"` | Just the breakdown, no execution |
| `/cdf:approve` | Persist a plan from plan mode, get execution strategy |
| Clear prompt + `xhigh` effort | Full lifecycle (brainstorm → docs → implement → verify) — 4.7 plans this natively, the `/cdf:flow` orchestrator was removed |

### Meta

| Command | When to use |
|---------|-------------|
| `/cdf:rules generate` | Generate project rules from codebase |
| `/cdf:rules status` | Check what rules exist |
| `/cdf:retro` | Engineering metrics from git history |

---

## Common Workflows

### "I need to build a feature"

```
/cdf:design "the feature"          # Optional: think first
/cdf:implement "the feature"       # Build it
/cdf:ship                          # Ship it
```

### "I need to build it right"

```
/cdf:brainstorm "requirements"     # Discover what to build
# Then write a clear prompt and let 4.7 plan the full lifecycle with xhigh effort
# (brainstorm → docs → implement → verify)
```

### "I need to challenge a plan"

Enter plan mode, discuss the approach, then:
```
/cdf:product-review                    # Founder-mode: is this the right thing?
/cdf:approve                       # Lock in the plan
/cdf:implement                     # Build it
```

### "I need to fix something fast"

```
/cdf:troubleshoot "the error"      # Diagnoses, fixes, adds regression test
```

### "I want to see how I'm doing"

```
/cdf:retro                             # Last 7 days
/cdf:retro 30d                         # Last 30 days
/cdf:retro compare                     # This week vs last week
```

### "New project, first session"

```
/cdf:rules generate                # Analyze codebase, create rules
```

This happens automatically on session start, but you can re-run it after major changes.

---

## What Happens Automatically

You don't need to configure these. They run on their own.

| What | When | Effect |
|------|------|--------|
| Codebase analysis | Session start | Generates `.claude/rules/` if missing; fast-confirms if present |
| Session context | Session start | Injects recent git history + memory |
| Code quality checks | After edits | Flags debug statements, low comment ratio (skips files >500 lines) |
| Push safety | Before git push | Warns on missing docs / changelog / version bumps (warn-only, never blocks) |
| Failure recovery | After 3 failures | STOP → REVERT → DOCUMENT → CONSULT |

---

## Tips

**Start simple.** `/cdf:implement` and `/cdf:ship` cover 80% of daily work.

**Let agents activate.** Don't try to pick agents manually — `/cdf:task` routes to the right one based on context, and most "persona" work (backend, frontend, devops, etc.) is handled by 4.7 directly from the Role line in CLAUDE.md.

**For big features, write a clear prompt and let 4.7 plan natively.** The `/cdf:flow` orchestrator was removed in the leanness pass — `xhigh` effort handles the brainstorm → docs → implement → verify chain when given a complete prompt.

**Run `/cdf:retro` weekly.** Takes 30 seconds, surfaces patterns you'd never notice.

**Trust the hooks but they warn, they don't block.** If a hook surfaces a warning, read it before dismissing. Hooks were tightened in the leanness pass to never block on documentation or count mismatches — gating belongs in CI.
