#!/usr/bin/env python3
"""
PreToolUse hook: Injects learned preferences as additionalContext.
Fires when the writing-voice skill is active, ensuring Claude always
respects learned preferences without relying on instructions alone.

Input: JSON on stdin (tool_name, tool_input, etc.)
Output: JSON on stdout with additionalContext
"""
import json
import os
import sys


def main():
    skill_dir = os.environ.get("CLAUDE_SKILL_DIR", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    learned_path = os.path.join(skill_dir, "learned.md")

    if not os.path.exists(learned_path):
        print(json.dumps({}))
        return

    try:
        with open(learned_path, "r") as f:
            content = f.read().strip()
    except Exception:
        print(json.dumps({}))
        return

    # Skip if file is empty or only has the template header
    if "(none yet)" in content and content.count("(none yet)") >= 3:
        print(json.dumps({}))
        return

    # Extract just the Do/Don't/Style entries, skip the header
    lines = content.split("\n")
    entries = []
    for line in lines:
        line = line.strip()
        if line.startswith("- ") and not line.startswith("- (none"):
            entries.append(line)

    if not entries:
        print(json.dumps({}))
        return

    context = "WRITING VOICE: Learned preferences (MUST follow):\n" + "\n".join(entries)
    print(json.dumps({"additionalContext": context}))


if __name__ == "__main__":
    main()
