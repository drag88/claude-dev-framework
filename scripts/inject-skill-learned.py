#!/usr/bin/env python3
"""
Reusable PreToolUse hook: Injects a skill's learned.md as additionalContext.

Any skill can use this by adding to its SKILL.md frontmatter:

    hooks:
      PreToolUse:
        - hooks:
            - type: command
              command: "python3 \"${CLAUDE_SKILL_DIR}/scripts/inject-learned.py\""
              timeout: 3
              once: true

Or reference this shared script:

    hooks:
      PreToolUse:
        - hooks:
            - type: command
              command: "python3 \"$CLAUDE_PLUGIN_ROOT/scripts/inject-skill-learned.py\" \"${CLAUDE_SKILL_DIR}\""
              timeout: 3
              once: true

Input: JSON on stdin (standard hook input)
Args: Optional skill directory path as first argument
Output: JSON on stdout with additionalContext containing learned preferences
"""
import json
import os
import sys


def main():
    # Determine skill directory from argument or environment
    if len(sys.argv) > 1:
        skill_dir = sys.argv[1]
    else:
        skill_dir = os.environ.get("CLAUDE_SKILL_DIR", "")

    if not skill_dir:
        print(json.dumps({}))
        return

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

    # Extract entries (lines starting with "- " that are not empty placeholders)
    entries = []
    for line in content.split("\n"):
        line_stripped = line.strip()
        if line_stripped.startswith("- ") and "none yet" not in line_stripped:
            entries.append(line_stripped)

    if not entries:
        print(json.dumps({}))
        return

    # Derive skill name from directory
    skill_name = os.path.basename(skill_dir)

    context = (
        f"LEARNED PREFERENCES ({skill_name}): The following preferences MUST be followed. "
        f"They were learned from prior corrections:\n" + "\n".join(entries)
    )
    print(json.dumps({"additionalContext": context}))


if __name__ == "__main__":
    main()
