# Context Saver Skill

Automatically save session progress before context limits are reached.

## When to Activate

- Context usage approaches 75%+
- User mentions "running out of context" or "context limit"
- Long session with significant progress made
- User indicates they need to take a break or switch tasks
- Before any planned context compaction or reset

## Actions

1. **Update active task documentation** in `dev/active/[task-name]/`:
   - Update `[task-name]-context.md` with:
     - Current implementation state
     - Key decisions made this session
     - Files modified and why
     - Blockers or issues discovered
     - Next immediate steps
     - Last Updated timestamp

   - Update `[task-name]-tasks.md` with:
     - Mark completed tasks
     - Add newly discovered tasks
     - Update in-progress task status
     - Reorder priorities if needed

2. **Capture session context**:
   - Complex problems solved
   - Architectural decisions made
   - Tricky bugs found and fixed
   - Integration points discovered
   - Testing approaches used

3. **Document unfinished work**:
   - What was being worked on when limit approached
   - Exact state of partially completed features
   - Commands needed to resume
   - Any temporary workarounds needing fixes

4. **Create handoff notes**:
   - Exact file and line being edited
   - Goal of current changes
   - Uncommitted changes that need attention
   - Test commands to verify work

## Related Commands

- `/dev-docs` - Create initial task documentation structure
- `/dev-docs-update` - Manually trigger documentation update
