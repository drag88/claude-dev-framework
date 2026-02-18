# Workflow Orchestration

## Subagent Strategy (Primary)

**Default to subagents. Main context is precious.**

The main conversation thread is your working memory. Every file read, every exploratory grep, every tangential research question consumes it permanently. Subagents work in isolated contexts and return only the result you need.

### When to Spawn a Subagent

| Task Type | Spawn? | Reason |
|-----------|--------|--------|
| Exploring an unfamiliar module | Yes | Returns a summary, not raw file contents |
| Researching a library/API | Yes | Returns verdict + key facts, not entire docs |
| Parallel analysis (multiple files/dirs) | Yes | Multiple agents, simultaneous |
| Tracing a bug across files | Yes | Agent can read 10+ files without polluting main context |
| Confirming a fact you already know | No | Just do it |
| A single targeted grep | No | Faster inline |
| Writing/editing a file | No | Must stay in main context |
| Simple single-file read | No | Faster inline |

### How to Spawn Well

One task per subagent. Not "analyze this module and also the one it depends on."

Give each agent:
1. A single, atomic goal
2. The specific files or directories to focus on
3. What to return (a summary, a verdict, a list — not raw file dumps)

For complex problems, throw more compute at it: spawn 3-5 agents in parallel, each covering a different angle.

### Project-Specific Spawn Patterns

**CDF plugin patterns**:
- Spawn agent to read an unfamiliar `commands/*.md` or `agents/*.md` and return its trigger conditions, behavioral flow, and key constraints — not the raw file
- Spawn parallel agents to audit `commands/` and `scripts/hooks/` simultaneously: one maps command intent, other maps hook implementation, then compare coverage
- Spawn agent to trace a hook's full lifecycle: `hooks/hooks.json` entry → `scripts/` implementation → what `additionalContext` it injects → when it fires

---

## Plan Mode Default

Enter plan mode before acting on non-trivial tasks (3+ steps, or any change touching more than 2 files).

What "plan mode" means:
- Write the approach before writing any code
- Identify the 2-3 most likely failure points
- Get confirmation if the plan involves deletions, schema changes, or public API surface

Skip plan mode for: single-file fixes, typo corrections, running tests.

If something goes sideways, STOP and re-plan immediately — don't keep pushing.

---

## Task Management

For anything requiring more than ~5 steps:

1. **Plan First**: Write plan with checkable items before starting
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section after completion
6. **Capture Lessons**: Update lessons after corrections

---

## Self-Improvement Loop

When corrected — on approach, on a fact, on a code pattern — record it immediately.

**How to record**: Use the Edit tool to append to today's daily log at `.claude/memory/daily/{YYYY-MM-DD}.md`:
- Corrections and decisions → append to the `## Decisions Made` section
- Issues and workarounds → append to the `## Issues Encountered` section

Format:
```
- [short description of what was wrong and what's right]
```

These entries are automatically propagated to MEMORY.md by the session-end hook, creating persistent cross-session memory.

**Read learnings at session start** — check `.claude/rules/memory-context.md` (auto-loaded) for recent decisions and known issues.

---

## Verification Before Done

Never mark a task complete without running a verification step.

Verification means:
- Run the relevant test(s) if tests exist
- If no tests: run the code and observe output
- If untestable: explicitly state what was checked and how
- Diff behavior between main and your changes when relevant

"It should work" is not verification. "I ran `pytest tests/test_auth.py` and all 12 tests passed" is verification.

Ask yourself: "Would a staff engineer approve this?"

---

## Demand Elegance (Balanced)

For non-trivial changes (more than ~20 lines, or a new function/class), pause and ask: **"Is there a more elegant way?"**

Elegance criteria:
- Fewer moving parts
- Reuses existing patterns in this codebase
- A future maintainer would not be confused

If a fix feels hacky: "Knowing everything I know now, implement the elegant solution."

Skip this for simple, obvious fixes — don't over-engineer. Challenge your own work before presenting it.

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
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
- **Prove It**: Every claim about behavior should be backed by a test or observable output.
