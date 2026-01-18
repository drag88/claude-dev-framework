#!/bin/bash
#
# Task Completeness Check Hook for Claude Code
#
# Stop hook that verifies all TodoWrite tasks are completed before
# allowing the session to end. Prevents premature session termination
# with incomplete work.
#
# Exit codes:
#   0 - All tasks complete or no tasks found
#   1 - Incomplete tasks found (blocks session stop)
#

# Read hook input from stdin
HOOK_INPUT=$(cat)

# Extract todo items from the hook input
# The hook receives session state including any active todos
TODOS=$(echo "$HOOK_INPUT" | jq -r '.todos // []')

# Count incomplete tasks
PENDING_COUNT=$(echo "$TODOS" | jq '[.[] | select(.status == "pending")] | length')
IN_PROGRESS_COUNT=$(echo "$TODOS" | jq '[.[] | select(.status == "in_progress")] | length')

INCOMPLETE_COUNT=$((PENDING_COUNT + IN_PROGRESS_COUNT))

# If there are incomplete tasks, generate a warning
if [ "$INCOMPLETE_COUNT" -gt 0 ]; then
    # Get the list of incomplete task names
    PENDING_TASKS=$(echo "$TODOS" | jq -r '[.[] | select(.status == "pending") | .content] | join("\n- ")')
    IN_PROGRESS_TASKS=$(echo "$TODOS" | jq -r '[.[] | select(.status == "in_progress") | .content] | join("\n- ")')

    # Build the warning message
    WARNING_MSG="## Incomplete Tasks Detected

The session has **$INCOMPLETE_COUNT incomplete task(s)**.

"

    if [ "$IN_PROGRESS_COUNT" -gt 0 ]; then
        WARNING_MSG+="### In Progress ($IN_PROGRESS_COUNT)
- $IN_PROGRESS_TASKS

"
    fi

    if [ "$PENDING_COUNT" -gt 0 ]; then
        WARNING_MSG+="### Pending ($PENDING_COUNT)
- $PENDING_TASKS

"
    fi

    WARNING_MSG+="**Options:**
1. Complete the remaining tasks before ending the session
2. Mark tasks as completed if they are actually done
3. Remove tasks that are no longer relevant
4. Use context-saver skill to preserve progress if context is running low

**Do not end the session with incomplete tasks unless absolutely necessary.**"

    # Output the warning as additional context
    echo "{\"additionalContext\": $(echo "$WARNING_MSG" | jq -Rs .)}"

    # Optionally block the session stop (uncomment to enforce)
    # exit 1
else
    # No incomplete tasks, allow session to end
    echo "{}"
fi
