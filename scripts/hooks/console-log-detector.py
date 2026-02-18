#!/usr/bin/env python3
"""
PostToolUse hook: Detect console.log statements in edited TypeScript/JavaScript files.
Warns when debugging statements are left in code.
"""

import json
import re
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from utils import print_warning, is_test_file


def check_for_console_logs(content: str, file_path: str) -> list:
    """
    Check content for console.log and similar debugging statements.
    Returns list of found patterns with line numbers.
    """
    # Skip test files
    if is_test_file(file_path):
        return []

    issues = []

    # Patterns to detect
    patterns = [
        (r'\bconsole\.log\s*\(', 'console.log'),
        (r'\bconsole\.debug\s*\(', 'console.debug'),
        (r'\bconsole\.info\s*\(', 'console.info (use logger instead)'),
        (r'\bdebugger\b', 'debugger statement'),
    ]

    lines = content.split('\n')
    for line_num, line in enumerate(lines, 1):
        # Skip if commented
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('*'):
            continue

        for pattern, name in patterns:
            if re.search(pattern, line):
                issues.append({
                    'line': line_num,
                    'type': name,
                    'content': stripped[:80]
                })

    return issues


def main():
    """Main entry point."""
    try:
        hook_data = json.load(sys.stdin)
        tool_input = hook_data.get('tool_input', {})
    except (json.JSONDecodeError, Exception):
        return

    if not tool_input:
        return

    file_path = tool_input.get('file_path', '')
    new_content = tool_input.get('content', '') or tool_input.get('new_string', '')

    if not file_path or not new_content:
        return

    issues = check_for_console_logs(new_content, file_path)

    if issues:
        print_warning(f"Debugging statements found in {Path(file_path).name}:")
        for issue in issues[:5]:  # Limit to 5 warnings
            print(f"  Line {issue['line']}: {issue['type']}", file=sys.stderr)

        if len(issues) > 5:
            print(f"  ... and {len(issues) - 5} more", file=sys.stderr)

        print("\nRemember to remove debugging statements before commit.", file=sys.stderr)


if __name__ == '__main__':
    main()
