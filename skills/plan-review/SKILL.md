---
name: reviewing-plans
description: "Pre-implementation plan review gauntlet. Activates when a non-trivial plan needs product, engineering, UX/DX, risk, and execution review before approval."
---

# Plan Review

Review plans before implementation. This is the skill backing `/cdf:plan-review` and the automatic nudge before `/cdf:approve`.

## When to Activate

- User asks to review, challenge, harden, stress-test, or improve a plan
- User says "think bigger", "is this the right plan", "what are we missing", "make this bulletproof"
- A plan was discussed in plan mode and the user is moving toward implementation
- The plan touches 3+ files, public behavior, data/storage, auth, payments, deployment, or cross-module contracts

Skip trivial single-file fixes and direct execution requests where the user clearly wants implementation now.

## Review Modes

| Mode | Use | Behavior |
|------|-----|----------|
| `expand` | Plan may be under-ambitious | Identify the 10x version and high-leverage adjacent improvements |
| `hold` | User wants current scope protected | Keep scope fixed; harden failure modes, tests, observability, and rollout |
| `reduce` | Scope is too large or risky | Cut to the smallest plan that preserves the outcome |
| `auto` | No mode specified | Infer mode from user language and plan maturity |

If mode is unclear, default to `hold`. Do not expand scope silently.

## Core Passes

### 1. Plan Context

Read before judging:
- The current conversation plan or supplied plan file
- Referenced docs, issues, or task files
- Relevant `.claude/rules/` files
- Existing code paths the plan touches

Use git context when useful:
```bash
git status --short
git diff --stat
git log --oneline -20 -- <affected-files>
```

### 2. Premise And Scope

Answer concretely:
- What outcome is this plan supposed to create?
- Is the plan solving the real problem or a proxy?
- What existing code already solves part of this?
- Which mode applies: `expand`, `hold`, or `reduce`?
- What should remain explicitly out of scope?

### 3. Engineering Review

Map the actual system shape:
- Data flow and state transitions
- Module boundaries and ownership
- API/schema/migration impacts
- Concurrency, idempotency, cache, and retry behavior
- Observability, rollback, and operator paths

Every non-trivial data flow gets shadow paths: nil input, empty input, upstream failure, permission failure, and partial completion.

### 4. UX/DX Review

For user-facing work, review:
- Happy path, empty state, loading state, error state, retry, cancellation, back/refresh behavior
- Accessibility and keyboard behavior
- Copy clarity at failure points

For developer-facing work, review:
- Time to first success
- Setup friction
- API ergonomics
- Examples and docs
- Error message actionability

Skip irrelevant review branches explicitly.

### 5. Risk And Test Matrix

Create a concise matrix:

```markdown
| Path | Risk | Required test/check |
|------|------|---------------------|
| Happy path | [risk] | [command or test] |
| Empty/nil input | [risk] | [command or test] |
| Upstream failure | [risk] | [command or test] |
| Permission/auth failure | [risk] | [command or test] |
| Slow/retry path | [risk] | [command or test] |
| Rollback/deploy path | [risk] | [command or test] |
```

### 6. Execution Brief

End with a plan the user can approve:
- Required plan changes
- Optional enhancements
- Open decisions
- Test and verification commands
- Recommended next command

## Verdicts

- `APPROVE` - Plan is ready; only minor notes remain
- `APPROVE_WITH_CHANGES` - Ready after listed changes are applied
- `REVISE` - Important gaps remain; revise before implementation
- `STOP` - Premise, scope, or risk is wrong enough that implementation should not start

## Output Shape

```markdown
## Plan Review

Verdict: APPROVE | APPROVE_WITH_CHANGES | REVISE | STOP
Mode: expand | hold | reduce

### Required Changes
- [Concrete change and why]

### Key Findings
- [Severity] [Area] Finding with evidence and fix path

### Test Matrix
| Path | Risk | Required test/check |
|------|------|---------------------|

### Open Decisions
- [Decision needed]

### Next Command
`/cdf:approve` or another specific command, with reason.
```

## Automatic Nudge

When a plan exists and the user says "go ahead", "implement this", or similar without review or approval:

> "This is non-trivial. Run `/cdf:plan-review` first to harden the plan, or skip and I will proceed."

If the user declines, proceed. Ask once per plan.

## Boundaries

- Do not implement during plan review.
- Do not turn review into a new workflow wrapper.
- Do not expand scope unless the user requested `expand` mode or the review explicitly recommends it as optional.
- Do not ask more than three questions; prefer concrete assumptions with an `Open Decisions` section.
