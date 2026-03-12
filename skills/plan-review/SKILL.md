---
description: "Enforce plan approval workflow — mark plans with <!-- PLAN_REVIEW --> marker, trigger approval gate, auto-generate docs, and recommend execution strategy"
---

# Plan Review & Approval Gate

## When to Activate

- You have just created an implementation plan (multi-step, touches 2+ files, or involves non-trivial changes)
- You are about to present a plan to the user for review
- The user asks you to plan something before implementing

## What Counts as a Plan

A "plan" is any structured implementation proposal that includes:
- Multiple sequential steps or phases
- File changes across 2+ files
- Architecture or design decisions that need user buy-in
- Task breakdowns with dependencies

**NOT a plan**: a single-file fix, a quick refactor explanation, a test run summary, a status update with checkboxes.

## The Marker

When you present a plan, you MUST end your response with this exact marker on its own line:

```
<!-- PLAN_REVIEW -->
```

This marker triggers the enforcement hook. Without it, the approval workflow does not activate. The marker is an HTML comment — invisible in rendered output.

## Post-Approval Workflow

When the user approves the plan, execute these steps in order:

### Step 1: Generate Documentation

Invoke `/cdf:docs plan` with the plan details. This creates:
- `dev/active/[task-name]/[task-name]-plan.md` — full strategic plan
- `dev/active/[task-name]/[task-name]-context.md` — key files and decisions
- `dev/active/[task-name]/[task-name]-tasks.md` — checklist for tracking

Use the approved plan content as the basis. Do not re-ask the user what the plan is — you just presented it.

### Step 2: Assess Complexity & Recommend Execution Strategy

Evaluate the plan on these dimensions:
- **File count**: How many files need changes?
- **Domain spread**: Does it cross boundaries (frontend + backend, hooks + skills, etc.)?
- **Risk level**: Does it touch sacred files, public APIs, or shared infrastructure?
- **Parallelizability**: Can parts be done independently?

Then recommend one of:

| Complexity | Indicators | Recommendation |
|------------|-----------|----------------|
| **Low** | 1-3 files, single domain, isolated changes | Execute directly in main context |
| **Medium** | 4-8 files, 1-2 domains, some dependencies | Use subagents for exploration, implement in main context |
| **High** | 8+ files, 3+ domains, cross-cutting concerns | Use agent teams — spawn parallel agents per domain, coordinate via tasks |

For **medium** complexity, specify which subagents to spawn and what each should return.

For **high** complexity, lay out the agent team structure:
- Which agent types (from `agents/`) to activate
- What each agent owns
- Dependencies between agents
- Merge/integration strategy

### Step 3: Confirm Execution

After presenting the docs and execution strategy, ask:

> "Documentation generated. Ready to execute with [recommended strategy]. Proceed?"

## Anti-Patterns

- Do NOT add the `<!-- PLAN_REVIEW -->` marker to non-plan responses (status updates, explanations, single-file fixes)
- Do NOT skip the docs generation step — the whole point is to capture the plan persistently
- Do NOT re-ask the user to describe the plan after they already approved it
- Do NOT default to agent teams for simple tasks — direct execution is faster for low complexity

## Related Commands

- `/cdf:docs plan` — generates the plan documentation
- `/cdf:task --breakdown` — breaks complex tasks into subtasks
- `/cdf:flow` — full workflow orchestration (brainstorm → docs → implement → verify)
