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

**Layer 2 — Agents** (activated for you)
Specialized personas (security-engineer, backend-architect, etc.) that activate based on what the command needs. You never call agents directly.

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
| `/cdf:workflow "PRD"` | Generate implementation steps from a spec |

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
| `/cdf:flow "feature"` | Full lifecycle: brainstorm → docs → implement → verify |
| `/cdf:task "complex thing"` | Break down and delegate with agents |
| `/cdf:task --breakdown "X"` | Just the breakdown, no execution |
| `/cdf:approve` | Persist a plan from plan mode, get execution strategy |

### Meta

| Command | When to use |
|---------|-------------|
| `/cdf:rules generate` | Generate project rules from codebase |
| `/cdf:rules status` | Check what rules exist |
| `/retro` | Engineering metrics from git history |

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
/cdf:flow "the feature"            # Full lifecycle with quality gates
```

### "I need to challenge a plan"

Enter plan mode, discuss the approach, then:
```
/product-review                    # Founder-mode: is this the right thing?
/cdf:approve                       # Lock in the plan
/cdf:implement                     # Build it
```

### "I need to fix something fast"

```
/cdf:troubleshoot "the error"      # Diagnoses, fixes, adds regression test
```

### "I want to see how I'm doing"

```
/retro                             # Last 7 days
/retro 30d                         # Last 30 days
/retro compare                     # This week vs last week
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
| Codebase analysis | Session start | Generates `.claude/rules/` |
| Session context | Session start | Injects recent git history + memory |
| Intent classification | Every request | Routes to right command/agent |
| Code quality checks | After edits | Flags debug statements, low comment ratio |
| Push safety | Before git push | Reviews what you're about to push |
| Failure recovery | After 3 failures | STOP → REVERT → DOCUMENT → CONSULT |

---

## Tips

**Start simple.** `/cdf:implement` and `/cdf:ship` cover 80% of daily work.

**Let agents activate.** Don't try to pick agents manually — `/cdf:task` routes to the right one based on context.

**Use `/cdf:flow` for big features.** It chains brainstorm → docs → implement → verify so nothing gets skipped.

**Run `/retro` weekly.** Takes 30 seconds, surfaces patterns you'd never notice.

**Trust the hooks.** If a hook blocks something, it's usually right. Read the message before dismissing.
