---
name: plan
description: Turn a raw idea, bug, or error into a grounded, structured, durable plan — the front door to implementation
argument-hint: "[idea | bug URL | pasted error | task description] [--name task-name]"
---

# /cdf:plan - Plan Front Door

> The moment you have an idea, it is `/cdf:plan`. Ground it in your codebase, structure it, persist it as a durable artifact, then hand off to review or execution.

## Quick Start

```bash
# From a raw idea
/cdf:plan "add semantic re-ranking to the search pipeline"

# From a bug (paste the issue URL or the error text)
/cdf:plan "https://github.com/org/repo/issues/214"
/cdf:plan "psycopg2.OperationalError: connection timed out on the nightly dbt run"

# Name the artifact explicitly
/cdf:plan "multi-tenant billing" --name multi-tenant-billing
```

## When to Use

Use `/cdf:plan` the moment an idea, bug, or error appears and the work is more than a one-line change. It starts from raw intent — you do not need an existing plan or to have entered plan mode first.

This is the single entry point for planning. It replaces the old "exit plan mode, then run approve" dance: `/cdf:plan` grounds the work, writes the plan, and routes you onward.

Do not use it for one-line changes (just make them) or for challenging a plan that already exists (use `/cdf:plan-review`).

## Behavioral Flow

The command runs four beats. Each beat produces something the next consumes.

### Beat 1 — Ground

Before spending any research, **state the scope and call it out, then proceed** (do not silently fan out):

```
Scope: <one-line statement of what this plan covers>
Call-outs: <ambiguities, assumptions, or boundary decisions the user should correct now>
Proceeding to research unless you redirect.
```

For trivial, unambiguous work, state the scope and continue without waiting. For non-trivial work, give the user a beat to redirect before research is spent.

Then ground the plan in reality:
- Read the codebase for existing patterns, conventions, and code that already solves part of the problem. Prefer subagents for multi-file exploration — they return a summary, not raw dumps.
- Read `docs/solutions/` and `.claude/rules/` for prior learnings and standards.
- Run external research **only when warranted** — when the task needs option-discovery, an unfamiliar library, or current best practices that local code cannot answer. If three or more strong local patterns already cover the approach, skip external research. When it is warranted, use `/cdf:research` or the deep-research-agent.

Cap parallel exploration at the ceiling in `.claude/rules/workflow.md` — more agents is not more signal.

### Beat 2 — Structure

Write the plan against a **section contract**, not a template. Five sections are a hard floor and always appear:

1. **Summary** — what the plan proposes, 1-3 lines, forward-looking. Lead with the answer.
2. **Problem Frame** — why; the user/business outcome. May merge into Summary.
3. **Requirements** — what must be true after shipping; the checklist review verifies against.
4. **Key Decisions** — each as `<decision>: <rationale>`. The load-bearing choices.
5. **Implementation Units** — the discrete, independently landable units of work (see schema below).

Everything else (technical design, scope boundaries, risks, rollout, observability, open questions) appears **only when it carries real content**. A padded section is worse than an omitted one — do not fill a heading to look thorough.

Tag every open decision so the plan only stops the user for what matters:
- **Mechanical** — one defensible answer. Decide it silently and note the choice.
- **Taste** — a judgment call with live trade-offs. Decide it, but flag it for the user.
- **User-Challenge** — touches the user's premise, scope, or product intent. Never auto-decide; ask.

Surface only Taste and User-Challenge decisions to the user. Do not interrogate them on Mechanical ones.

### Beat 3 — Persist

Write the durable artifact via `/cdf:docs plan` (the underlying generator) to `dev/active/[task-name]/`:
- `[task-name]-plan.md` — the structured plan above
- `[task-name]-context.md` — key files, decisions, dependencies
- `[task-name]-tasks.md` — the checkbox tracker (authoritative progress state)

Each **Implementation Unit** carries:
- **Goal** — what this unit accomplishes
- **Files** — repo-relative paths to create/modify/test (never absolute)
- **Approach** — key decisions, data flow, boundaries
- **Patterns to follow** — existing code/conventions to mirror
- **Verification** — the concrete command or check that proves this unit done (e.g. `pytest tests/test_rerank.py`, `dbt test --select staging.orders`, an observed output). This is what makes "done" provable rather than asserted — it matches the workflow rule that pasted command output, not "it should work," is verification.

Keep the checkboxes as the authoritative progress state. The `Verification:` line is how an interrupted session confirms a unit really shipped before moving on — git history (injected at session start) stays advisory context, not the state store.

### Beat 4 — Hand off

Do not stop at announcing the next step — route the user there. Assess complexity from Beat 1 (file count, domain spread, whether it touches sacred files or public APIs) and set the default accordingly, then ask:

Use AskUserQuestion with options:
- **Run `/cdf:plan-review`** — the adversarial gauntlet. Default and recommended for high-stakes plans (8+ files, 3+ domains, sacred files, public API, data-loss or billing surface).
- **Go to `/cdf:task`** — straight to execution. Default for low-stakes, isolated plans.
- **Edit the plan first** — the user wants to revise before committing.

Set the recommended option as the default based on the complexity read, and say why in one line. Then act on the choice — fire the chosen command, do not just name it.

## Output Format

```markdown
## Plan: [task-name]

Scope: [one line]
Stakes: low | medium | high — [why]
Artifact: dev/active/[task-name]/

### Summary
[Forward-looking, lead with the answer]

### Requirements
- [What must be true after shipping]

### Key Decisions
- [decision]: [rationale]
- [Taste/User-Challenge decisions surfaced for confirmation]

### Implementation Units
#### U1. [Name]
- Goal:
- Files:
- Approach:
- Patterns to follow:
- Verification: [concrete command or check]

### Next
[AskUserQuestion: plan-review | task | edit — with the recommended default]
```

## Boundaries

**Will:**
- Start from raw intent and produce a grounded, structured, durable plan
- Gate research behind an explicit scope statement
- Surface only the decisions that need the user; decide the mechanical ones
- Give each unit a provable `Verification:` check
- Route to review or execution and fire the chosen command

**Will Not:**
- Implement code (that is `/cdf:task` / `/cdf:implement`)
- Force the adversarial gauntlet on every plan — review is opt-in per plan
- Pad sections to look thorough
- Recreate `/cdf:flow` or `/cdf:workflow` — this is the planning beat only, not a lifecycle orchestrator

## Related Commands

- `/cdf:plan-review` — optional adversarial gauntlet for high-stakes plans
- `/cdf:docs plan` — the underlying artifact generator
- `/cdf:task` — execute or delegate the plan
- `/cdf:research` — external research when local patterns are insufficient
- `/cdf:brainstorm` — discover requirements when the idea is still fuzzy
