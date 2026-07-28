---
description: Workflow rules, subagent strategy, verification gates
---

# Workflow Orchestration Template

> Template for generating `.claude/rules/workflow.md`.

---

## Tool and parallel call policy

Spawn multiple subagents in the same turn when fanning out across items, reading multiple files, or running independent investigations. Skip fan-out for single-file edits or trivial reads.

---

## Subagent Strategy

Subagents return summaries, not raw file contents — reach for one when the reading budget matters more than fidelity.

Route by task shape: quick fixes direct or `/cdf:implement`; bugs `/cdf:troubleshoot`; plan-first work `/cdf:plan`. Pre-PR: `/cdf:verify`.

### Compound-Engineering Integration

Compound-engineering is the required engineering-loop engine for delegated commands. CDF references it by public skill name only and never copies its behavior.

Knowledge split:
- `compound-engineering:ce-compound` writes durable repo knowledge to `docs/solutions/` and `CONCEPTS.md`; commit these artifacts.
- `/cdf:learn` captures skill-preference corrections only.
- Auto-memory captures session decisions only; promote them to `compound-engineering:ce-compound` when they harden.
- `CONCEPTS.md` is seeded by `compound-engineering:ce-compound` on first capture; do not create it manually.

### How to Spawn Well

One task per subagent. Not "analyze this module and also the one it depends on."

Give each agent:
1. A single, atomic goal
2. The specific files or directories to focus on
3. What to return (a summary, a verdict, a list — not raw file dumps)

For complex problems, throw more compute at it: spawn 3-5 agents in parallel, each covering a different angle.

---

## Plan Mode Default

Enter plan mode before acting on non-trivial tasks.

What "plan mode" means:
- Write the approach before writing any code
- Identify the 2-3 most likely failure points
- Get confirmation if the plan involves deletions, schema changes, or public API surface

If something goes sideways, stop and re-plan immediately rather than pushing through a broken approach.

---

## Verification Before Done

Verification is a command you ran plus its output, not an assertion. "It should work" is not verification. UI changes: screenshot at 1440px and 390px.

---

## Autonomous Bug Fixing

Given a bug report: fix it. Don't ask for hand-holding.

Standard approach:
1. Point at logs, errors, failing tests — then resolve them
2. Identify root cause (not just symptom)
3. Fix at root cause
4. Add a regression test
5. Verify the fix

Zero context switching required from the user. Go fix failing CI tests without being told how.

---

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
- **Prove It**: Every claim about behavior should be backed by a test or observable output.
- **Elegance over novelty**: Prefer the change that reuses an existing pattern here over a new abstraction; fix root causes, not symptoms.
- **Human-curated rules**: Reserve `.claude/rules/` for human-curated standards; never write there autonomously.
- **Report everything, filter later**: For review or coverage tasks, surface all findings (low-severity, uncertain, edge cases) with confidence and severity. Do not self-filter before reporting.
</content>
</invoke>
