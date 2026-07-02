---
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

## Delegation: compound-engineering

This command delegates to the `compound-engineering:ce-plan` host skill.

**Requires**: the compound-engineering plugin. If it is not installed, stop and tell the user to install the compound-engineering plugin for their host (install commands are in the README) — do not improvise a replacement flow.

**Flow**: Invoke the `compound-engineering:ce-plan` host skill, passing the raw input (idea, bug URL, pasted error, or task description) and the `--name` value when given as context.

**CDF constraints (bind on top of the skill)**:
- The plan document lands in `docs/plans/` (committed — plans compound).
- State the scope in one line before research is spent; call out ambiguities the user should correct.
- Ground the plan in the codebase and in `docs/solutions/` + `.claude/rules/` prior learnings.
- Hand off when done: recommend `/cdf:plan-review` (→ `compound-engineering:ce-doc-review`) for high-stakes plans, otherwise `/cdf:implement` or `/cdf:task` for execution.

## Related Commands

- `/cdf:plan-review` — optional adversarial gauntlet for high-stakes plans
- `/cdf:docs plan` — the underlying artifact generator
- `/cdf:task` — execute or delegate the plan
- `/cdf:research` — external research when local patterns are insufficient
- `/cdf:brainstorm` — discover requirements when the idea is still fuzzy
