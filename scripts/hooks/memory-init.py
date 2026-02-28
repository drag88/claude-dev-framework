#!/usr/bin/env python3
"""
SessionStart hook: Initialize project memory structure and inject session context.
Creates .claude/memory/ directory and generates memory-context.md for session continuity.

Does NOT touch native auto-memory (~/.claude/projects/<project>/memory/MEMORY.md) —
that's Claude's domain for semantic memories (decisions, patterns, preferences).
CDF owns structured daily activity logs only.
"""

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from utils import get_project_root, get_memory_dir, read_json_file, print_info, print_warning


def get_daily_dir() -> Path:
    """Get the daily logs directory path."""
    return get_memory_dir() / 'daily'


def get_rules_dir() -> Path:
    """Get the rules directory path."""
    return get_project_root() / '.claude' / 'rules'


def init_memory_structure():
    """Create memory directory structure if it doesn't exist."""
    memory_dir = get_memory_dir()
    daily_dir = get_daily_dir()

    # Create directories
    memory_dir.mkdir(parents=True, exist_ok=True)
    daily_dir.mkdir(exist_ok=True)

    return memory_dir


def init_daily_log():
    """Create today's daily log if it doesn't exist."""
    today = datetime.now().strftime('%Y-%m-%d')
    daily_file = get_daily_dir() / f'{today}.md'

    if daily_file.exists():
        return False

    weekday = datetime.now().strftime('%A')

    content = f"""# {today} ({weekday}) - Session Log

## Session Summary

*Session in progress...*

## Changes Made

| File | Change | Reason |
|------|--------|--------|
| - | - | - |

## TODO / Follow-up

- [ ] Review changes made today

## Activity Log

- `{datetime.now().strftime('%H:%M')}` - Session started
"""

    with open(daily_file, 'w') as f:
        f.write(content)

    return True


def extract_section(content: str, section_name: str, max_lines: int = 20) -> str:
    """Extract a section from markdown content."""
    pattern = rf'^## {re.escape(section_name)}\s*\n(.*?)(?=^## |\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        lines = match.group(1).strip().split('\n')[:max_lines]
        text = '\n'.join(lines)
        # Skip if it's just placeholder text
        if text.startswith('*') and text.endswith('*') and len(text) < 100:
            return ''
        return text
    return ''


def get_last_session_date():
    """Get the most recent session date from .index.json."""
    index_file = get_memory_dir() / '.index.json'
    data = read_json_file(index_file)
    if not data or 'sessions' not in data:
        return None

    try:
        dates = sorted(data['sessions'].keys(), reverse=True)
        if not dates:
            return None
        return datetime.strptime(dates[0], '%Y-%m-%d')
    except (ValueError, AttributeError):
        return None


def load_memory_context() -> dict:
    """Load session continuity context from CDF daily logs only.

    Does NOT parse native auto-memory — Claude loads that itself.
    """
    context = {
        'recent_activity': '',
        'open_todos': [],
        'yesterday_summary': '',
        'session_gap_days': 0
    }

    # Load today's TODOs and activity
    today = datetime.now().strftime('%Y-%m-%d')
    today_file = get_daily_dir() / f'{today}.md'
    if today_file.exists():
        with open(today_file) as f:
            content = f.read()

        # Extract unchecked TODOs
        todos = re.findall(r'^- \[ \] (.+)$', content, re.MULTILINE)
        context['open_todos'] = [t for t in todos if not t.startswith('*')]

        # Extract today's activity (last 10 entries)
        activity = extract_section(content, 'Activity Log', 10)
        if activity:
            context['recent_activity'] = activity

    # Load yesterday's summary
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday_file = get_daily_dir() / f'{yesterday}.md'
    if yesterday_file.exists():
        with open(yesterday_file) as f:
            content = f.read()

        summary = extract_section(content, 'Session Summary', 10)
        if summary and '*Session in progress...*' not in summary:
            context['yesterday_summary'] = summary

    # Detect session staleness
    last_session = get_last_session_date()
    if last_session:
        gap = (datetime.now() - last_session).days
        context['session_gap_days'] = gap

    return context


def generate_context_rule(context: dict) -> str:
    """Generate the memory context rule file content.

    Outputs only session continuity info: gap notice, yesterday summary,
    today's activity, and open TODOs.
    """
    parts = []

    parts.append("# Project Memory Context")
    parts.append("")
    parts.append("*Auto-loaded from `.claude/memory/` - Progressive disclosure of project context.*")
    parts.append("")

    # Session gap notice
    if context.get('session_gap_days', 0) > 3:
        parts.append(f"> Note: {context['session_gap_days']} days since last session. Review MEMORY.md for full context.")
        parts.append("")

    # Open TODOs (critical context)
    if context['open_todos']:
        parts.append("## Open TODOs")
        for todo in context['open_todos'][:5]:
            parts.append(f"- [ ] {todo}")
        parts.append("")

    # Yesterday's summary
    if context['yesterday_summary']:
        parts.append("## Yesterday's Summary")
        parts.append(context['yesterday_summary'])
        parts.append("")

    # Today's recent activity
    if context['recent_activity']:
        parts.append("## Recent Activity (Today)")
        parts.append(context['recent_activity'])
        parts.append("")

    # Footer
    parts.append("---")
    parts.append("*Daily logs: `.claude/memory/daily/` | Semantic memory: Claude auto-memory*")

    return '\n'.join(parts)


def inject_memory_context():
    """Generate memory context rule file for Claude to auto-load."""
    context = load_memory_context()

    rules_dir = get_rules_dir()
    rules_dir.mkdir(parents=True, exist_ok=True)

    rule_content = generate_context_rule(context)
    rule_file = rules_dir / 'memory-context.md'

    with open(rule_file, 'w') as f:
        f.write(rule_content)

    return True


def main():
    """Main entry point."""
    try:
        # Initialize structure
        init_memory_structure()

        # Initialize today's log
        daily_created = init_daily_log()
        if daily_created:
            print_info(f"Daily log created for {datetime.now().strftime('%Y-%m-%d')}")

        # Inject memory context into rules (session continuity only)
        context_injected = inject_memory_context()
        if context_injected:
            print_info("Memory context loaded -> .claude/rules/memory-context.md")

    except Exception as e:
        print_warning(f"Memory init warning: {e}")


if __name__ == '__main__':
    main()
