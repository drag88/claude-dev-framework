---
description: "Unified development workflow: brainstorm -> docs -> implement -> verify -> compound"
argument-hint: "[task] [--complexity simple|standard|complex] [--skip phases] [--resume] [--deepen]"
---

# /cdf:flow - Unified Development Workflow

> Orchestrate the complete development lifecycle from idea to verified, documented code.

## Default Behavior

**When invoked, `/cdf:flow` classifies task complexity and chains appropriate phases with quality gates.**

```bash
# Full workflow
/cdf:flow "implement user authentication with OAuth"

# Auto-detects simple task, optimizes phases
/cdf:flow "fix null pointer in UserService"
```

## Quick Start

```bash
# Complex feature (all phases)
/cdf:flow "implement real-time notifications"

# Bug fix (optimized phases)
/cdf:flow "fix race condition in cache refresh"

# Resume interrupted work
/cdf:flow --resume

# Parallel agent saturation for complex tasks
/cdf:flow "migrate to microservices" --deepen

# Skip specific phases
/cdf:flow "add API endpoint" --skip brainstorm
```

## When to Use

Use `/cdf:flow` when:
- Starting a new feature or significant change
- Want automated phase progression with quality gates
- Need resumable workflow for complex tasks
- Want knowledge captured at the end

**Don't use this command for**: Quick edits, exploratory questions, or when you want manual control over each phase.

## Complexity Classification

Before executing, classify task complexity using intent-gate patterns:

### Simple
**Signals**: "fix", "typo", "update", "correct", single-file, <50 estimated lines
**Phases**: docs(lite) -> implement -> verify(quick)

### Standard
**Signals**: "add", "implement", "create", multi-file, 50-500 estimated lines
**Phases**: docs -> implement -> verify -> compound(optional)

### Complex
**Signals**: "design", "architect", "migrate", "restructure", >500 lines, multi-domain
**Phases**: brainstorm -> docs -> implement -> verify -> compound

**Override**: Use `--complexity` flag to force a level.

## Behavioral Flow

### Phase 1: BRAINSTORM (Complex only)

Delegate to `/cdf:brainstorm` patterns:
1. Socratic dialogue to explore requirements
2. Identify constraints and edge cases
3. Generate requirements specification
4. **Gate**: Requirements documented and user confirmed

**Escape**: User says "proceed with current understanding"

### Phase 2: DOCS (Planning)

Delegate to `/cdf:docs plan` with enhanced output:
1. Analyze codebase for relevant patterns
2. Design implementation approach
3. Break down into tasks with checkbox tracking
4. Create persistent state in `dev/active/[task-slug]/`
5. **Gate**: Plan created with tasks defined

**Output Format** (checkbox tracking):
```markdown
## Phase 1: Setup [0/2]
- [ ] Create module directory structure
- [ ] Add dependencies to package.json

## Phase 2: Implementation [0/3]
- [ ] Implement core service
- [ ] Add API endpoints
- [ ] Create database migrations

**Progress**: 0/5 tasks (0%)
```

**Escape**: User says "quick plan" or "just outline"

### Phase 3: IMPLEMENT

Delegate to `/cdf:implement` patterns:
1. Execute tasks from plan in order
2. Update checkboxes as tasks complete (`[ ]` -> `[x]`)
3. Activate relevant personas (frontend, backend, security)
4. Create checkpoints every 20 tool calls
5. **Gate**: All tasks checked, code compiles

**Escape**: User says "checkpoint" or "save progress"

### Phase 4: VERIFY

Delegate to `/cdf:verify` with mode based on complexity:
- **Simple**: `--mode quick` (types + lint only)
- **Standard**: `--mode pre-commit` (types + lint + affected tests)
- **Complex**: `--mode pre-pr` (full pipeline + security)

1. Run verification pipeline
2. Report issues with fix suggestions
3. **Gate**: All checks pass or user overrides

**Escape**: User says "accept with warnings" or "commit anyway"

### Phase 5: COMPOUND (Knowledge Capture)

Delegate to `/cdf:compound`:
1. Extract patterns from implementation
2. Document decisions with rationale
3. Create solution doc in `docs/solutions/[category]/`
4. **Gate**: At least one pattern captured

**Escape**: User says "no compound needed" or auto-skip for simple tasks

## State Persistence

All state saved in `dev/active/[task-slug]/`:

```
dev/active/[task-slug]/
├── flow-state.md      # Phase status with YAML frontmatter
├── flow-plan.md       # Implementation plan with checkboxes
├── flow-tasks.md      # Task tracking (mirrors plan checkboxes)
├── flow-context.md    # Decisions, dependencies, key files
└── flow-compound.md   # Knowledge capture (created at end)
```

### flow-state.md Format

```yaml
---
task: "implement user authentication"
task_slug: user-auth
complexity: complex
created: 2024-01-15T10:30:00Z
last_updated: 2024-01-15T14:30:00Z
current_phase: implement
tool_calls: 47
phases:
  brainstorm: { status: completed, gate_passed: true }
  docs: { status: completed, gate_passed: true }
  implement: { status: in_progress, progress: 65 }
  verify: { status: pending }
  compound: { status: pending }
---

# Flow: Implement User Authentication

## Current State
- **Phase**: Implementation (3/5)
- **Progress**: 65% complete (3/5 tasks)
- **Next Gate**: Pre-verify quality check

## Quick Resume
1. Read `flow-plan.md` for requirements
2. Check tasks starting at "Add API endpoints"
3. Continue from `src/auth/OAuthProvider.ts`
```

## Arguments

| Argument | Description |
|----------|-------------|
| `[task]` | Description of what to build/fix |
| `--complexity` | Override auto-detection: `simple`, `standard`, `complex` |
| `--skip` | Skip phases (comma-separated): `brainstorm`, `compound` |
| `--resume` | Resume interrupted workflow |
| `--deepen` | Activate parallel agent saturation (see `/cdf:deepen`) |
| `--list` | Show resumable workflows |

## Escape Hatches

| Command | Effect |
|---------|--------|
| `pause` | Save current state, exit with resume instructions |
| `checkpoint` | Create checkpoint without exiting |
| `skip [phase]` | Skip current or named phase with warning |
| `pivot` | Return to planning phase with new approach |
| `override` | Force past current gate (logged in flow-state) |
| `simplify` | Downgrade complexity level |
| `abort` | Clean exit with state preserved |

## Quality Gates

Each phase has gates that must pass before proceeding:

| Phase | Gate Criteria |
|-------|---------------|
| Brainstorm | Requirements documented, user confirmed |
| Docs | Plan created, tasks defined with checkboxes |
| Implement | All tasks checked, code compiles |
| Verify | Tests pass, lint clean, security OK (by mode) |
| Compound | At least one pattern captured |

**Gate Failure Handling**:
- First failure: Report issue, suggest fix
- Second failure: Offer alternative approach
- Third failure: Pause workflow, present options (fix, override, abort)

## Deepen Mode

When `--deepen` is specified, activate parallel agent saturation:

1. Discover ALL agents from project, user, and plugins
2. Spawn agents in parallel WITHOUT filtering
3. Let agents self-filter for relevance
4. Synthesize findings with deduplication

See `/cdf:deepen` for standalone usage.

## MCP Integration

- **Sequential MCP**: Complex reasoning for phase transitions
- **Context7 MCP**: Framework-specific implementation patterns
- **Playwright MCP**: E2E validation (complex tasks)

## Tool Coordination

| Tool | Purpose |
|------|---------|
| `Read/Grep/Glob` | Codebase analysis |
| `Write/Edit` | Code generation with checkpoint tracking |
| `Bash` | Build, test, verification commands |
| `Task` | Agent delegation for deepen mode |
| `TodoWrite` | Internal task tracking |

## Persona Activation

Automatically activated based on task domain:
- Architecture changes: @system-architect
- Backend work: @backend-architect
- Frontend work: @frontend-architect
- Security concerns: @security-engineer
- Quality checks: @quality-engineer

## Examples

### New Feature (Complex)
```bash
/cdf:flow "implement real-time notifications with WebSocket"
# Phases: brainstorm -> docs -> implement -> verify -> compound
# Creates dev/active/realtime-notifications/
```

### Bug Fix (Simple)
```bash
/cdf:flow "fix null pointer exception in UserService.getProfile()"
# Phases: docs(lite) -> implement -> verify(quick)
# No brainstorm or compound
```

### Major Refactor with Deep Analysis
```bash
/cdf:flow "migrate from REST to GraphQL API" --deepen
# All phases with parallel agent saturation
# 20-40 agents analyze in parallel during docs phase
```

### Resume After Interruption
```bash
/cdf:flow --resume
# Lists available flows, resumes selected one
# Restores exact state from flow-state.md
```

### Skip Brainstorm (Clear Requirements)
```bash
/cdf:flow "add pagination to /users endpoint" --skip brainstorm
# Starts at docs phase with provided requirements
```

## Boundaries

**Will:**
- Orchestrate complete development lifecycle
- Adapt workflow to task complexity
- Maintain state for interruption recovery
- Capture knowledge for future sessions
- Update plan checkboxes during implementation

**Will Not:**
- Skip quality gates without explicit override
- Continue past repeated failures without consultation
- Lose progress on context limits (auto-checkpoint)
- Make architectural decisions without appropriate phase
- Execute implementation without a plan

## Related Commands

- `/cdf:brainstorm` - Standalone requirements discovery
- `/cdf:docs plan` - Standalone planning
- `/cdf:implement` - Standalone implementation
- `/cdf:verify` - Standalone verification
- `/cdf:compound` - Standalone knowledge capture
- `/cdf:deepen` - Standalone parallel agent saturation
- `/cdf:session` - Manual session management
