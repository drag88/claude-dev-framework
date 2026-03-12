---
name: approve
description: Approve a plan from plan mode, generate persistent documentation, and recommend execution strategy
---

# /cdf:approve - Plan Approval & Documentation

> Run after exiting plan mode to persist the plan as documentation and get an execution strategy.

## Quick Start

```bash
# After exiting plan mode
/cdf:approve

# With a specific task name
/cdf:approve "auth-refactor"
```

## When to Use

Use `/cdf:approve` immediately after exiting Claude Code's native plan mode (Shift+Tab). This command:
1. Captures the plan from the current conversation
2. Generates persistent documentation via `/cdf:docs plan`
3. Assesses complexity and recommends an execution strategy
4. Asks for final confirmation before implementation

**Don't use this command for**: Plans you want to discard, trivial single-file changes, or when you haven't created a plan yet.

## Behavioral Flow

### Step 1: Capture the Plan

Read the plan from the current conversation context. The plan was just discussed in plan mode — do NOT ask the user to re-describe it.

If no plan is visible in the conversation, tell the user: "No plan found in this conversation. Run this command right after exiting plan mode."

### Step 2: Generate Documentation

Invoke `/cdf:docs plan` with the task name (from args or inferred from the plan). This creates:
- `dev/active/[task-name]/[task-name]-plan.md` — full strategic plan
- `dev/active/[task-name]/[task-name]-context.md` — key files and decisions
- `dev/active/[task-name]/[task-name]-tasks.md` — checklist for tracking

### Step 3: Assess Complexity & Recommend Execution Strategy

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

### Step 4: Confirm Execution

Present a summary:

```
Plan: [task name]
Docs: dev/active/[task-name]/
Strategy: [direct | subagents | agent teams]
[Brief strategy details]

Ready to execute. Proceed?
```

Wait for the user's response before implementing anything.

## Tool Coordination

- **Read**: Access conversation context for plan content
- **Write**: Generate documentation files via `/cdf:docs plan`
- **Glob/Grep**: Analyze files referenced in the plan for complexity assessment
- **Agent**: Spawn subagents or teams based on recommended strategy

## Examples

### After a Simple Plan
```
/cdf:approve "fix-auth-timeout"
# Generates docs, recommends direct execution
```

### After a Complex Plan
```
/cdf:approve "migrate-database-layer"
# Generates docs, recommends agent teams with per-domain ownership
```

## Boundaries

**Will:**
- Capture and persist plans from the current conversation
- Generate structured documentation for tracking
- Recommend appropriate execution strategy based on complexity

**Will Not:**
- Execute the plan without explicit confirmation
- Work without a plan in the current conversation context
- Override user's choice of execution strategy

## Related Commands

- `/cdf:docs plan` — underlying documentation generator
- `/cdf:task --breakdown` — alternative for breaking complex tasks into subtasks
- `/cdf:flow` — full workflow orchestration (brainstorm → docs → implement → verify)
- `/cdf:implement` — execute implementation after approval
