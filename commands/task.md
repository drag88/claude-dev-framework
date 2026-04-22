---
description: "Execute complex tasks with intelligent workflow management, breakdown, and delegation"
argument-hint: "[action] [target] [--strategy systematic|agile|enterprise] [--parallel] [--delegate] [--breakdown]"
---

# /cdf:task — Task Execution

> Execute defined tasks with structured delegation when fan-out is warranted. For multi-step work, write a clear prompt and let Opus 4.7 plan — orchestration scaffolding has been removed in favor of native planning.

## Quick Start

```bash
/cdf:task create "enterprise authentication system"
/cdf:task execute "feature backlog" --delegate --parallel
/cdf:task --breakdown "implement user authentication system"
```

## When to Use

- Task requires fan-out across multiple subagents working in parallel
- You want a documented delegation contract (tools whitelist + scope boundaries) for each subagent
- Long-running work where state persistence matters

For single-subagent work or simple sequential steps, just write the prompt — `xhigh` effort plans well without this command.

## Delegation contract (when fanning out)

When invoking the Task tool, include these seven sections so the subagent has everything it needs in one turn:

```markdown
### 1. Task
Atomic, specific goal — one action only.

### 2. Expected outcome
Concrete deliverables with measurable success criteria.

### 3. Required skills
Which CDF skill or agent to invoke (e.g. "codebase-navigator", "library-researcher").

### 4. Required tools
Explicit tool whitelist (e.g. "Read, Grep, Glob"). No tools outside this list.

### 5. Required actions
- Each requirement on its own line
- Be specific and actionable
- Reference real file paths and patterns

### 6. Out of scope
- Forbidden actions
- Scope boundaries
- Quality constraints

### 7. Context
- File paths: relevant paths
- Patterns: naming conventions, code patterns
- Constraints: time, scope, dependencies
```

### Example

```markdown
### 1. Task
Implement input validation for the user registration form.

### 2. Expected outcome
- Validation functions for email, password, username fields
- Error messages displayed inline
- Form prevents submission until valid

### 3. Required skills
frontend-patterns (skill, auto-invoked on React work)

### 4. Required tools
Read, Edit, Write, Grep

### 5. Required actions
- Use the existing validation utility in src/utils/validators.ts
- Follow the project's error message conventions
- Add unit tests for each validator
- Ensure accessibility (aria-invalid, aria-describedby)

### 6. Out of scope
- Form layout or styling changes
- New dependencies
- Backend validation logic

### 7. Context
- File paths: src/components/RegisterForm.tsx, src/utils/validators.ts
- Patterns: project uses Zod for schema validation
- Constraints: must work with existing form state management
```

## Breakdown mode (`--breakdown`)

Decomposes a complex operation into a coordinated subtask hierarchy (Epic → Story → Task → Subtask). Useful when scope spans multiple domains and dependencies need explicit tracking.

```bash
/cdf:task --breakdown "implement user authentication system"
/cdf:task --breakdown "migrate monolith to microservices" --strategy enterprise --parallel
```

For most multi-step features, skip `--breakdown` and let 4.7 plan from the prompt — the breakdown is only needed when you explicitly want a documented hierarchy you can review before execution.

## Behavioral flow

1. **Analyze**: parse task requirements, determine whether delegation is warranted.
2. **Delegate**: if fan-out is warranted, spawn subagents with the seven-section contract above. Otherwise execute inline.
3. **Coordinate**: track progress across delegated subagents, surface blockers.
4. **Validate**: apply quality gates from `/cdf:verify` if relevant. Paste output, do not paraphrase.

## Tool coordination

- **TodoWrite / TaskCreate**: hierarchical task breakdown when scope warrants it
- **Task / Agent**: subagent delegation
- **Read / Write / Edit**: implementation in main context

## Boundaries

**Will:**
- Execute complex tasks with multi-agent fan-out when delegation is warranted
- Provide hierarchical breakdown with documented contracts
- Coordinate multiple subagents and surface results

**Will not:**
- Add orchestration scaffolding for tasks 4.7 plans natively
- Compromise correctness for speed
- Skip the seven-section delegation contract when fanning out (the structure is what makes delegation reliable)
