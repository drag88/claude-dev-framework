#!/usr/bin/env python3
"""
PostToolUse hook: Log significant file changes to daily memory log.
Tracks file edits, creates, and deletes with timestamps.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from utils import get_project_root, print_info


def get_daily_log_path() -> Path:
    """Get today's daily log path."""
    today = datetime.now().strftime('%Y-%m-%d')
    return get_project_root() / '.claude' / 'memory' / 'daily' / f'{today}.md'


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
    # Skip common non-essential files
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

## Decisions Made

*Recording decisions...*

## Issues Encountered

*No issues recorded yet.*

## TODO / Follow-up

- [ ] Review changes made today

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


def log_bash_command(tool_input: dict):
    """Log a Bash command execution to the daily log."""
    timestamp = datetime.now().strftime('%H:%M:%S')
    command = tool_input.get('command', '')
    if not command:
        return

    # Skip logging commands that touch memory files
    if '.claude/memory/' in command:
        return

    cmd_display = command[:80]
    suffix = '...' if len(command) > 80 else ''

    entry = f'- `{timestamp}` - ran: `{cmd_display}{suffix}`'

    # Include exit code if available
    exit_code = tool_input.get('exit_code')
    if exit_code is not None:
        entry += f' | exit:{exit_code}'

    append_to_daily_log(entry)


def main():
    """Main entry point."""
    try:
        hook_data = json.load(sys.stdin)
    except (json.JSONDecodeError, Exception):
        return

    tool_input = hook_data.get('tool_input', {})
    if not tool_input:
        return

    # Distinguish Bash vs file operations by checking for 'command' key
    if 'command' in tool_input:
        log_bash_command(tool_input)
        return

    file_path = tool_input.get('file_path', '') or tool_input.get('notebook_path', '')
    if not file_path:
        return

    log_file_change(tool_input)


if __name__ == '__main__':
    main()
