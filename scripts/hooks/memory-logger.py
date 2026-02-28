#!/usr/bin/env python3
"""
PostToolUse hook: Log file mutations (Edit/Write/MultiEdit) to daily memory log.
Only fires on file changes — reads, bash commands, and web searches are not tracked.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from utils import get_project_root, get_daily_log_path


def get_relative_path(file_path: str) -> str:
    """Convert absolute path to relative path from project root."""
    try:
        project_root = get_project_root()
        abs_path = Path(file_path).resolve()
        return str(abs_path.relative_to(project_root))
    except:
        return file_path


def should_log_file(file_path: str) -> bool:
    """Determine if this file change should be logged."""
    skip_patterns = [
        'node_modules/',
        '.git/',
        '__pycache__/',
        '.pyc',
        '.log',
        '.tmp',
        '.cache/',
        'dist/',
        'build/',
        '.next/',
        '.claude/memory/',  # Don't log changes to memory itself
        'package-lock.json',
        'yarn.lock',
        'pnpm-lock.yaml',
    ]

    file_lower = file_path.lower()
    for pattern in skip_patterns:
        if pattern in file_lower:
            return False

    return True


def append_to_daily_log(entry: str):
    """Append an entry to today's daily log."""
    log_path = get_daily_log_path()

    # Ensure directory exists
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Create log if it doesn't exist
    if not log_path.exists():
        weekday = datetime.now().strftime('%A')
        today = datetime.now().strftime('%Y-%m-%d')
        header = f"""# {today} ({weekday}) - Session Log

## Session Summary

*Session in progress...*

## Changes Made

| File | Change | Reason |
|------|--------|--------|

## Activity Log

"""
        with open(log_path, 'w') as f:
            f.write(header)

    # Append entry
    with open(log_path, 'a') as f:
        f.write(entry + '\n')


def log_file_change(tool_input: dict):
    """Log a file change (Edit/Write/MultiEdit) to the daily log."""
    timestamp = datetime.now().strftime('%H:%M:%S')

    file_path = tool_input.get('file_path') or tool_input.get('notebook_path', '')

    if not file_path or not should_log_file(file_path):
        return

    relative_path = get_relative_path(file_path)

    # Build rich entry based on tool input shape
    if 'old_string' in tool_input or 'new_string' in tool_input:
        # Edit/MultiEdit
        snippet = (tool_input.get('new_string') or '')[:60]
        suffix = '...' if len(tool_input.get('new_string') or '') > 60 else ''
        entry = f'- `{timestamp}` - edited: `{relative_path}` | "{snippet}{suffix}"'
    else:
        # Write
        content = tool_input.get('content', '')
        entry = f'- `{timestamp}` - created/updated: `{relative_path}` | ~{len(content)} chars'

    append_to_daily_log(entry)


def main():
    """Main entry point. Only handles Edit/Write/MultiEdit tool inputs."""
    try:
        hook_data = json.load(sys.stdin)
    except (json.JSONDecodeError, Exception):
        return

    tool_input = hook_data.get('tool_input', {})
    if not tool_input:
        return

    # Only log file mutations
    file_path = tool_input.get('file_path', '') or tool_input.get('notebook_path', '')
    if not file_path:
        return

    log_file_change(tool_input)


if __name__ == '__main__':
    main()
