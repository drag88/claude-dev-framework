#!/usr/bin/env python3
"""
Plan Review Gate — Stop hook

Scans last_assistant_message for the <!-- PLAN_REVIEW --> marker.
If found and not already in a stop-hook continuation, injects context
telling Claude to ask for plan approval before proceeding.
"""

import sys
import json


PLAN_MARKER = "<!-- PLAN_REVIEW -->"

APPROVAL_CONTEXT = """## Plan Approval Required

You just presented an implementation plan. Before proceeding:

1. **Ask the user**: "Do you approve this plan?"
2. **If approved**: Invoke `/cdf:docs plan` to generate persistent documentation, then assess complexity and recommend execution strategy (direct, subagents, or agent teams) per the plan-review skill.
3. **If rejected or changes requested**: Revise the plan and present it again with the `<!-- PLAN_REVIEW -->` marker.

Do NOT proceed with implementation until explicit approval is received."""


def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        print(json.dumps({}))
        return

    # Prevent infinite loops — if we're already continuing from a stop hook, skip
    if hook_input.get("stop_hook_active", False):
        print(json.dumps({}))
        return

    last_message = hook_input.get("last_assistant_message", "")

    if PLAN_MARKER in last_message:
        print(json.dumps({"additionalContext": APPROVAL_CONTEXT}))
    else:
        print(json.dumps({}))


if __name__ == "__main__":
    main()
