---
description: "Pre-implementation plan review gauntlet across product, engineering, UX/DX, risk, and execution readiness"
argument-hint: "[plan|file|topic] [--mode expand|hold|reduce|auto] [--focus product|engineering|ux|dx|risk|all]"
---

# /cdf:plan-review - Plan Review Gauntlet

> Stress-test a plan before implementation. Challenge scope, surface failure modes, and produce an approve-ready execution brief.

## Quick Start

```bash
# Review the current conversation plan
/cdf:plan-review

# Review a specific plan document
/cdf:plan-review dev/active/auth-refactor/auth-refactor-plan.md

# Push ambition and scope
/cdf:plan-review "multi-tenant billing" --mode expand

# Hold scope and harden execution
/cdf:plan-review --mode hold --focus engineering
```

## When to Use

Use `/cdf:plan-review` when:
- A plan touches multiple files, modules, teams, user journeys, or production behavior
- You want strategic challenge before writing code
- The plan needs UX, DX, security, observability, rollout, or test hardening
- You are about to run `/cdf:approve` on non-trivial work

Do not use this command for single-file fixes, already-approved implementation tasks, or post-implementation code review. Use `/cdf:troubleshoot`, `/cdf:task`, or `/cdf:analyze` instead.

## Modes

| Mode | Use | Posture |
|------|-----|---------|
| `auto` | Default | Infer from plan maturity and user language |
| `expand` | Product could be more ambitious | Find the 10x version and adjacent high-leverage additions |
| `hold` | Scope is accepted | Keep scope fixed and make execution bulletproof |
| `reduce` | Scope feels too large | Cut to the smallest version that preserves the outcome |

## Behavioral Flow

1. **Load Plan Context**
   - Read the plan from the current conversation or supplied file/path.
   - Read nearby docs when referenced: `README.md`, architecture docs, active task docs, and relevant `.claude/rules/`.
   - Run lightweight git context when useful: `git status --short`, `git diff --stat`, and recent commits for files the plan touches.

2. **Scope And Premise Review**
   - Name the user/business outcome.
   - Challenge whether the plan solves the real problem or a proxy.
   - Map existing code that already solves part of the problem.
   - Pick `expand`, `hold`, or `reduce` if mode is `auto`, and explain why.

3. **Engineering Review**
   - Map data flow, state transitions, dependencies, and ownership boundaries.
   - Identify hidden coupling, migration risks, concurrency risks, cache/state risks, and backwards-compatibility traps.
   - Name observability, rollback, and operational requirements.

4. **UX/DX Review**
   - If user-facing, review workflows, edge cases, accessibility, loading states, errors, and empty states.
   - If developer-facing, review time-to-first-success, docs, API ergonomics, examples, setup friction, and failure messages.
   - Skip irrelevant branches explicitly instead of inventing findings.

5. **Risk And Test Review**
   - Produce a test matrix: happy path, nil/empty input, upstream failure, permission failure, slow/retry path, and rollback path.
   - Identify security/privacy risks, data-loss risks, cost risks, and deployment risks.
   - Mark any blocker that must be resolved before implementation.

6. **Execution Brief**
   - Rewrite the plan only where needed.
   - List required changes, optional enhancements, open decisions, and out-of-scope items.
   - Recommend next command: `/cdf:approve`, `/cdf:task --breakdown`, `/cdf:design`, `/cdf:troubleshoot`, or stop for user decision.

## Output Format

```markdown
## Plan Review

Verdict: APPROVE | APPROVE_WITH_CHANGES | REVISE | STOP
Mode: expand | hold | reduce

### Required Changes
- [Concrete change with why]

### Key Findings
- [Severity] [Area] Finding with evidence and fix path

### Execution Brief
- Scope:
- Files/systems:
- Rollout:
- Observability:

### Test Matrix
| Path | Test | Owner/command |
|------|------|---------------|

### Open Decisions
- [Decision needed before implementation]

### Next Command
`/cdf:approve` or another specific command, with reason.
```

## Boundaries

Will:
- Challenge plan quality before implementation
- Produce concrete changes, risk calls, and a test matrix
- Preserve user-chosen scope unless mode is `expand` or `reduce`

Will not:
- Implement code
- Recreate `/cdf:flow` or `/cdf:workflow`
- Invent product requirements when user intent is missing
- Block the user from skipping review when they explicitly choose to proceed

## Related Commands

- `/cdf:brainstorm` - Discover requirements before a plan exists
- `/cdf:design` - Produce technical design before implementation
- `/cdf:approve` - Persist the reviewed plan and choose execution strategy
- `/cdf:task` - Execute or delegate the approved plan
