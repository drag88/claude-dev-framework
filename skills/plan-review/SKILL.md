---
name: reviewing-plans
description: "Reminds users to run /cdf:approve after exiting plan mode to persist plans and get execution strategy"
---

# Plan Review Awareness

## When to Activate

- The user has just exited plan mode and is about to start implementation
- The conversation contains a plan that was discussed in plan mode but hasn't been persisted via `/cdf:approve`
- The user says something like "go ahead", "implement this", or "let's do it" after a planning discussion

## Behavior

When you detect that a plan was just discussed and the user is moving toward implementation WITHOUT having run `/cdf:approve`, gently remind them:

> "You have a plan ready. Want to run `/cdf:approve` to persist it as documentation and get an execution strategy before we start?"

If the user declines or wants to skip, proceed normally — this is a nudge, not a gate.

## What Counts as a Plan

A "plan" is any structured implementation proposal that includes:
- Multiple sequential steps or phases
- File changes across 2+ files
- Architecture or design decisions
- Task breakdowns with dependencies

**NOT a plan**: a single-file fix, a quick refactor explanation, a test run summary.

## Anti-Patterns

- Do NOT block implementation if the user wants to skip approval
- Do NOT remind more than once per plan — if the user declines, drop it
- Do NOT activate for trivial changes that don't warrant documentation

> This skill is intentionally minimal — it serves as a lightweight nudge, not a full workflow.
