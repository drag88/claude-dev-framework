# Workflow Orchestration

## Explore Before Edit

**Never make piecemeal changes without understanding the full picture first.**

LLM performance degrades as context fills. When you jump straight to coding without exploring, you solve the wrong problem or miss existing patterns. Separate exploration from execution.

### The 4-Phase Pattern

1. **Explore** — Read files, trace dependencies, understand what exists. Use Plan Mode or subagents so exploration doesn't pollute implementation context.
2. **Plan** — Write the approach before writing code. Identify failure points.
3. **Implement** — Code against the plan in clean context.
4. **Verify** — Prove it works before marking done.

### For Piecemeal/Incremental Changes

When making changes that touch multiple files or modules incrementally:
- Explore the full scope FIRST, even if you plan to change files one at a time
- Map all the files that will need changes before editing any of them
- Understand upstream and downstream dependencies of each change
- Use subagents to fan out and read related modules in parallel — keeps main context clean for the actual edits
- If the scope grows beyond what you mapped, STOP and re-explore before continuing

**Anti-pattern**: Editing file A, then discovering file B also needs changes, then finding file C — each discovery consuming main context. Instead: one exploration pass up front, then focused edits.

### Scoping Investigations

Avoid the "infinite exploration" trap — reading hundreds of files and filling context with raw content. Scope investigations narrowly or use subagents so exploration stays out of main context.

---

## Subagents vs Agent Teams

Two delegation mechanisms. Different tools for different problems.

### Subagents (Agent tool)

Single-session, isolated context. Best for focused, bounded tasks.

- Run in isolated context windows — exploration doesn't consume main conversation
- One atomic goal per subagent, return summaries not raw dumps
- Cannot spawn other subagents (no nesting)
- Can run foreground (blocking) or background (concurrent)

**Use subagents when:**
- Investigating a module, tracing a bug, researching a library
- Fan-out exploration: 3-5 agents reading different areas in parallel
- High-volume output handling (test results, large file analysis)
- The task is self-contained and returns a clear result

### Agent Teams (TeamCreate)

Multi-session coordination. Each worker gets its own independent, sustained context.

- Workers run in separate sessions with full context windows
- Support messaging and coordination between workers
- Each worker can use all tools independently
- Workers persist — you can send follow-up messages

**Use agent teams when:**
- Multiple workers need sustained context (not just a quick lookup)
- Tasks are too large for one context window
- Workers need to coordinate or share state
- Parallel implementation across independent files/modules
- The work is implementation, not just research

### Decision Table

| Situation | Use | Why |
|-----------|-----|-----|
| "Read these 5 files and summarize" | Subagent | Quick, isolated, returns summary |
| "Research how auth works" | Subagent | Bounded investigation |
| "Implement feature X across 4 modules" | Agent Team | Sustained parallel implementation |
| "Refactor module A while I work on module B" | Agent Team | Independent sustained work |
| "Check if this pattern exists anywhere" | Subagent | Quick grep, bounded result |
| "Build the API, frontend, and tests in parallel" | Agent Team | Three independent implementation streams |
| "What does this function do?" | Neither | Just read the file inline |

### Subagent Spawn Patterns

**General patterns:**
- Spawn agent to explore an unfamiliar directory — return purpose, key files, connections to rest of codebase
- Spawn parallel agents across `src/` and `tests/` for a holistic view
- Spawn agent to research a dependency's API before using it — return only relevant functions

**CDF plugin patterns:**
- Spawn agent to read `commands/*.md` or `agents/*.md` — return trigger conditions, behavioral flow, constraints
- Spawn parallel agents to audit `commands/` and `scripts/hooks/` — one maps command intent, other maps hook implementation, then compare
- Spawn agent to trace a hook's lifecycle: `hooks/hooks.json` → `scripts/` implementation → `additionalContext` injection → when it fires

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

When corrected — on approach, on a fact, on a code pattern — save it to your auto-memory immediately.

**What to save**: Key decisions, corrections, debugging insights, project patterns, and architectural notes.

**Where to save**: Your native auto-memory (`~/.claude/projects/<project>/memory/MEMORY.md` and topic files). Use the Write or Edit tool to update these files. This is Claude's domain — CDF hooks never write here.

**Session continuity** — at session start, CDF injects recent git history and your auto-memory as context. No manual file management needed.

---

## Verification Before Done

Never mark a task complete without running a verification step.

Verification means:
- Run the relevant test(s) if tests exist
- If no tests: run the code and observe output
- For visual/UI changes: verify in the browser before confirming to the user
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

---

## CDF Agents

When working in this project, use the appropriate CDF agent for specialized tasks:

| Task Type | Agent | Command |
|-----------|-------|---------|
| System design | system-architect | `/cdf:task` |
| API/backend work | backend-architect | `/cdf:task` |
| UI development | frontend-architect | `/cdf:task` |
| CI/CD setup | devops-architect | `/cdf:task` |
| Research topics | deep-research-agent | `/cdf:research` |
| Find code/patterns | codebase-navigator | `/cdf:task` |
| Evaluate libraries | library-researcher | `/cdf:task` |
| Debug issues | root-cause-analyst | `/cdf:troubleshoot` |
| Write tests | quality-engineer | `/cdf:test` |
| Security audit | security-engineer | `/cdf:analyze` |
| Performance | performance-engineer | `/cdf:analyze` |
| Refactor code | refactoring-expert | `/cdf:improve` |
| Documentation | technical-writer | `/cdf:docs` |
| TDD workflow | tdd-guide | `/cdf:tdd` |
| E2E testing | e2e-specialist | `/cdf:e2e` |

**Auto-activation**: Agents activate automatically via `/cdf:task` based on task context.

---

## Memory

- Check auto-memory for prior context at session start
- Save key decisions, debugging insights, and project patterns to auto-memory during work
