# Context Saver Skill

Automatically save session progress before context limits are reached and suggest strategic compaction.

## When to Activate

- Context usage approaches 75%+
- User mentions "running out of context" or "context limit"
- Long session with significant progress made
- User indicates they need to take a break or switch tasks
- Before any planned context compaction or reset
- **Tool call counter exceeds 50 calls** (suggest compaction)
- At logical workflow boundaries (feature complete, PR ready)

---

## Strategic Compaction Triggers

### Automatic Suggestions
Suggest `/compact` when:
1. **Tool calls > 50**: High activity indicates significant context usage
2. **Large file reads**: Multiple 500+ line files read
3. **Workflow boundary**: Major task just completed
4. **Context warning**: System indicates high context usage

### Compaction Reminder Format
```
💡 Context Check

This session has been highly productive with 52 tool calls.
Consider compacting to preserve context for continued work.

Recommended actions:
1. Run `/cdf:session save --checkpoint` to preserve state
2. Run `/compact` to reclaim context space
3. Continue with fresh context

Current progress saved in: .claude/sessions/current-context.md
```

---

## Actions

### 1. Update Active Task Documentation

Update files in `dev/active/[task-name]/`:

**[task-name]-context.md**:
- Current implementation state
- Key decisions made this session
- Files modified and why
- Blockers or issues discovered
- Next immediate steps
- Last Updated timestamp

**[task-name]-tasks.md**:
- Mark completed tasks
- Add newly discovered tasks
- Update in-progress task status
- Reorder priorities if needed

### 2. Capture Session Context

Document:
- Complex problems solved
- Architectural decisions made
- Tricky bugs found and fixed
- Integration points discovered
- Testing approaches used
- Patterns worth remembering

### 3. Document Unfinished Work

When approaching limit, capture:
- What was being worked on when limit approached
- Exact state of partially completed features
- Commands needed to resume
- Any temporary workarounds needing fixes

### 4. Create Handoff Notes

Essential information for continuation:
- Exact file and line being edited
- Goal of current changes
- Uncommitted changes that need attention
- Test commands to verify work

---

## Context Checkpoint Format

```markdown
# Session Checkpoint

**Created**: 2024-01-15T14:30:00Z
**Session ID**: abc123
**Tool Calls**: 52

## Current State

### Active Task
[Description of what we're working on]

### Files Modified
| File | Change | Status |
|------|--------|--------|
| src/auth.ts | Added OAuth flow | Complete |
| src/api/users.ts | Updated endpoints | In Progress |

### In Progress
- Line 45 of `src/api/users.ts` - adding validation
- Next: complete error handling

### Decisions Made
1. Using JWT with 15-minute expiry
2. Refresh tokens stored in HTTP-only cookies
3. OAuth providers: Google, GitHub

### Known Issues
- [ ] Token refresh not handling network errors
- [ ] Need to add rate limiting

## Resume Instructions

1. Open `src/api/users.ts:45`
2. Complete the validation logic
3. Run tests: `npm test -- --testPathPattern=users`
4. Continue with error handling

## Related Context
- OAuth implementation: `dev/active/oauth/oauth-context.md`
- API documentation: `docs/api/authentication.md`
```

---

## Compaction Workflow

### Before Compacting
1. **Verify save**: Ensure all progress is captured
2. **Check git status**: Commit or stash changes
3. **Document state**: Create checkpoint with resume instructions
4. **Notify user**: Confirm readiness to compact

### Compaction Message
```
Ready to compact. Before proceeding:

✓ Session checkpoint created
✓ 3 files modified (all saved)
✓ Git status: clean (committed)

Resume file: .claude/sessions/checkpoint-20240115-143000.md

Proceed with /compact when ready.
```

---

## Tool Call Tracking

### Counter Implementation
Track tool usage patterns:
- Total tool calls in session
- Heavy tool usage (file reads, edits)
- Consecutive similar operations

### Threshold Actions

| Calls | Action |
|-------|--------|
| 30 | Internal tracking only |
| 50 | Suggest save checkpoint |
| 70 | Recommend compaction |
| 90 | Urgent compaction warning |

---

## Integration with Session Command

### Auto-checkpoint on Workflow Completion
When `/cdf:implement`, `/cdf:test`, or similar completes:
1. Check tool call counter
2. Assess context usage
3. Suggest checkpoint if > 50 calls

### Checkpoint vs Full Save
- **Checkpoint**: Quick snapshot, minimal overhead
- **Full Save**: Comprehensive state, all context

```bash
# Quick checkpoint
/cdf:session save --checkpoint

# Full save with all context
/cdf:session save --type all
```

---

## Related Commands

- `/cdf:docs plan` - Create initial task documentation structure
- `/cdf:docs update` - Manually trigger documentation update
- `/cdf:session save` - Save session state
- `/cdf:session load` - Resume from checkpoint
- `/compact` - Reclaim context space
