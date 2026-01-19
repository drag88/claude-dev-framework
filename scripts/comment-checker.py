#!/usr/bin/env python3
"""
Comment Checker Hook for Claude Code

PostToolUse hook that checks comment-to-code ratio in edited files.
Triggers a warning if comments exceed 25% of the file content.

This encourages writing self-documenting code with minimal but meaningful comments.
"""

import json
import os
import sys
import re
from pathlib import Path

# Comment threshold (25%)
COMMENT_THRESHOLD = 0.25

# Language-specific comment patterns
COMMENT_PATTERNS = {
    # Python
    ".py": {
        "line": r"^\s*#.*$",
        "block_start": r'^\s*"""',
        "block_end": r'"""',
        "alt_block_start": r"^\s*'''",
        "alt_block_end": r"'''"
    },
    # JavaScript/TypeScript
    ".js": {
        "line": r"^\s*//.*$",
        "block_start": r"/\*",
        "block_end": r"\*/"
    },
    ".ts": {
        "line": r"^\s*//.*$",
        "block_start": r"/\*",
        "block_end": r"\*/"
    },
    ".jsx": {
        "line": r"^\s*//.*$",
        "block_start": r"/\*",
        "block_end": r"\*/"
    },
    ".tsx": {
        "line": r"^\s*//.*$",
        "block_start": r"/\*",
        "block_end": r"\*/"
    },
    # Go
    ".go": {
        "line": r"^\s*//.*$",
        "block_start": r"/\*",
        "block_end": r"\*/"
    },
    # Rust
    ".rs": {
        "line": r"^\s*//.*$",
        "block_start": r"/\*",
        "block_end": r"\*/"
    },
    # Ruby
    ".rb": {
        "line": r"^\s*#.*$",
        "block_start": r"^=begin",
        "block_end": r"^=end"
    },
    # Java/Kotlin
    ".java": {
        "line": r"^\s*//.*$",
        "block_start": r"/\*",
        "block_end": r"\*/"
    },
    ".kt": {
        "line": r"^\s*//.*$",
        "block_start": r"/\*",
        "block_end": r"\*/"
    },
    # C/C++
    ".c": {
        "line": r"^\s*//.*$",
        "block_start": r"/\*",
        "block_end": r"\*/"
    },
    ".cpp": {
        "line": r"^\s*//.*$",
        "block_start": r"/\*",
        "block_end": r"\*/"
    },
    ".h": {
        "line": r"^\s*//.*$",
        "block_start": r"/\*",
        "block_end": r"\*/"
    },
    # Shell
    ".sh": {
        "line": r"^\s*#.*$",
    },
    ".bash": {
        "line": r"^\s*#.*$",
    },
    # YAML
    ".yaml": {
        "line": r"^\s*#.*$",
    },
    ".yml": {
        "line": r"^\s*#.*$",
    },
}


def count_comment_lines(content: str, patterns: dict) -> tuple[int, int]:
    """
    Count comment lines and total non-empty lines in content.
    Returns (comment_lines, total_lines).
    """
    lines = content.split("\n")
    comment_lines = 0
    total_lines = 0
    in_block_comment = False
    block_end_pattern = None

    line_pattern = patterns.get("line")
    block_start = patterns.get("block_start")
    block_end = patterns.get("block_end")
    alt_block_start = patterns.get("alt_block_start")
    alt_block_end = patterns.get("alt_block_end")

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        total_lines += 1

        # Check for block comment end
        if in_block_comment:
            comment_lines += 1
            if block_end_pattern and re.search(block_end_pattern, line):
                in_block_comment = False
                block_end_pattern = None
            continue

        # Check for block comment start
        if block_start and re.search(block_start, line):
            comment_lines += 1
            if not (block_end and re.search(block_end, line)):
                in_block_comment = True
                block_end_pattern = block_end
            continue

        # Check for alternate block comment start (Python triple quotes)
        if alt_block_start and re.search(alt_block_start, line):
            comment_lines += 1
            if not (alt_block_end and line.count('"""') >= 2 or line.count("'''") >= 2):
                in_block_comment = True
                block_end_pattern = alt_block_end
            continue

        # Check for line comment
        if line_pattern and re.match(line_pattern, line):
            comment_lines += 1

    return comment_lines, total_lines


def check_file(file_path: str) -> dict | None:
    """
    Check a file's comment ratio and return warning if too high.
    """
    path = Path(file_path)

    if not path.exists():
        return None

    suffix = path.suffix.lower()
    if suffix not in COMMENT_PATTERNS:
        return None

    try:
        content = path.read_text(encoding="utf-8")
    except (IOError, UnicodeDecodeError):
        return None

    patterns = COMMENT_PATTERNS[suffix]
    comment_lines, total_lines = count_comment_lines(content, patterns)

    if total_lines == 0:
        return None

    ratio = comment_lines / total_lines

    if ratio > COMMENT_THRESHOLD:
        percentage = int(ratio * 100)
        return {
            "file": file_path,
            "comment_lines": comment_lines,
            "total_lines": total_lines,
            "ratio": percentage
        }

    return None


def main() -> None:
    """Main entry point for the hook."""
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({}))
        return

    # Get the tool call info
    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Only check Write and Edit tools
    if tool_name not in ["Write", "Edit", "MultiEdit"]:
        print(json.dumps({}))
        return

    # Get the file path from the tool input
    file_path = tool_input.get("file_path")
    if not file_path:
        print(json.dumps({}))
        return

    # Check the file's comment ratio
    warning = check_file(file_path)

    if warning:
        result = {
            "additionalContext": f"""## Comment Ratio Warning

The file `{warning['file']}` has a high comment-to-code ratio:
- **{warning['ratio']}%** of lines are comments ({warning['comment_lines']}/{warning['total_lines']} lines)
- Threshold: {int(COMMENT_THRESHOLD * 100)}%

**Recommendations:**
1. Prefer self-documenting code with clear variable/function names
2. Remove obvious comments that duplicate what the code says
3. Keep comments for WHY, not WHAT
4. Consider if complex code needs refactoring instead of commenting

Only add comments when they provide value the code cannot express itself."""
        }
    else:
        result = {}

    print(json.dumps(result))


if __name__ == "__main__":
    main()
