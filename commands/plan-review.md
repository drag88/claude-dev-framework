---
description: "Pre-implementation plan review gauntlet across product, engineering, UX/DX, risk, and execution readiness"
argument-hint: "[plan-file-path or inline plan]"
---

# /cdf:plan-review - Plan Review Gauntlet

## Triggers
- Mandatory review gate before `/cdf:approve`
- Review of `docs/plans/*.md` and `docs/brainstorms/*.md`
- Review of inline plans before implementation
- Product, engineering, UX/DX, risk, or execution-readiness challenge requests

## Context Trigger Pattern
```
/cdf:plan-review [plan-file-path or inline plan]
```

## Delegation: compound-engineering

This command delegates to the `compound-engineering:ce-doc-review` host skill.

**Requires**: the compound-engineering plugin. If it is not installed, stop and tell the user to install the compound-engineering plugin for their host (install commands are in the README) — do not improvise a replacement flow.

**Flow**: Invoke the `compound-engineering:ce-doc-review` host skill, passing the document path (or the inline plan) as the argument. Do not forward `--flag`-style tokens — the skill parses a document path plus its own `mode:` tokens only.

**CDF constraints (bind on top of the skill)**:
- This is the mandatory gate before `/cdf:approve`.
- Review `docs/plans/*.md`, `docs/brainstorms/*.md`, and inline plans.
- Keep CDF approval readiness as the framing for the review result.
