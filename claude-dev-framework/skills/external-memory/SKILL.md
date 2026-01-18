# External Memory Skill

Use file-based working memory for complex tasks that exceed typical context limits.

## When to Activate

- Task requires 50+ tool calls to complete
- Multi-phase implementation spanning multiple areas
- Complex debugging requiring extensive investigation notes
- Research tasks with many findings to synthesize
- User explicitly requests persistent task tracking

## File Structure

Create in `dev/memory/` directory:

```
dev/memory/
├── task_plan.md      # Goal, phases, and progress tracking
├── notes.md          # Research findings, observations, decisions
└── deliverable.md    # Final output draft (updated incrementally)
```

## File Templates

### task_plan.md

```markdown
# Task: [Clear description]

## Goal
[Single sentence describing success]

## Phases
- [ ] Phase 1: [Description]
- [ ] Phase 2: [Description]
- [ ] Phase 3: [Description]

## Current Phase
Phase [N]: [Name]

## Progress Log
- [timestamp] Started Phase 1
- [timestamp] Completed X, moving to Y
- [timestamp] Blocked on Z, investigating

## Blockers
- [Any current blockers]

## Next Actions
1. [Immediate next step]
2. [Following step]
```

### notes.md

```markdown
# Research Notes

## Key Findings
- [Finding 1 with evidence]
- [Finding 2 with evidence]

## Decisions Made
| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| [Choice] | [Why]     | [Other options]        |

## Code Patterns Found
- [Pattern 1]: [Location and description]
- [Pattern 2]: [Location and description]

## Questions to Resolve
- [ ] [Question 1]
- [ ] [Question 2]

## Raw Notes
[Unstructured observations during investigation]
```

### deliverable.md

```markdown
# [Deliverable Title]

## Status: [Draft/In Review/Complete]

## Summary
[Brief description of what this delivers]

## Contents
[The actual deliverable content, updated incrementally]

## Verification
- [ ] [Verification step 1]
- [ ] [Verification step 2]
```

## Actions

1. **Initialize Memory** at task start:
   - Create `dev/memory/` directory
   - Create `task_plan.md` with goal and phases
   - Initialize empty `notes.md` and `deliverable.md`

2. **Update Continuously**:
   - After each significant finding → update `notes.md`
   - After completing a phase → update `task_plan.md`
   - When producing output → append to `deliverable.md`

3. **Read Before Acting**:
   - Start each work session by reading memory files
   - Check progress log to understand current state
   - Review blockers before proceeding

4. **Sync at Milestones**:
   - Every 20 tool calls, sync notes
   - Before any risky operation, save progress
   - After completing a phase, update all files

## Best Practices

- Keep notes atomic and timestamped
- Link notes to specific file paths when relevant
- Update progress log with each significant step
- Mark blockers immediately when discovered
- Clear completed items from "Next Actions"
- Move resolved questions to "Decisions Made"

## Related Skills

- `context-saver` - Save progress when context runs low
- `rules-generator` - Document patterns discovered during research
