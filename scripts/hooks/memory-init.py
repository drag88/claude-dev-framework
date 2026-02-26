#!/usr/bin/env python3
"""
SessionStart hook: Initialize project memory structure and inject context.
Creates .claude/memory/ directory and loads relevant context via progressive disclosure.
Bridges with Claude's native auto-memory (~/.claude/projects/<project>/memory/).
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from utils import get_project_root, read_json_file, print_info, print_warning


def get_memory_dir() -> Path:
    """Get the memory directory path."""
    return get_project_root() / '.claude' / 'memory'


def get_daily_dir() -> Path:
    """Get the daily logs directory path."""
    return get_memory_dir() / 'daily'


def get_decisions_dir() -> Path:
    """Get the decisions directory path."""
    return get_memory_dir() / 'decisions'


def get_rules_dir() -> Path:
    """Get the rules directory path."""
    return get_project_root() / '.claude' / 'rules'


def init_memory_structure():
    """Create memory directory structure if it doesn't exist."""
    memory_dir = get_memory_dir()
    daily_dir = get_daily_dir()
    decisions_dir = get_decisions_dir()
    
    # Create directories
    memory_dir.mkdir(parents=True, exist_ok=True)
    daily_dir.mkdir(exist_ok=True)
    decisions_dir.mkdir(exist_ok=True)
    
    return memory_dir


def get_native_auto_memory_path() -> Path:
    """Resolve the native auto-memory MEMORY.md path.

    Claude's auto-memory lives at ~/.claude/projects/<project-key>/memory/MEMORY.md
    where <project-key> replaces all non-alphanumeric chars (except -) with '-'.
    Example: /Users/foo/my_project -> ~/.claude/projects/-Users-foo-my-project/memory/
    """
    project_root = get_project_root()
    # Convert path to Claude's format: replace all non-alphanumeric chars (except -) with '-'
    project_key = re.sub(r'[^a-zA-Z0-9-]', '-', str(project_root))
    return Path.home() / '.claude' / 'projects' / project_key / 'memory' / 'MEMORY.md'


def migrate_memory_to_native():
    """One-time migration: copy Key Decisions from in-project MEMORY.md to native auto-memory.

    Only runs if:
    - Native auto-memory MEMORY.md does NOT exist
    - In-project .claude/memory/MEMORY.md exists and has Key Decisions content
    """
    native_path = get_native_auto_memory_path()
    if native_path.exists():
        return False

    old_memory = get_memory_dir() / 'MEMORY.md'
    if not old_memory.exists():
        return False

    with open(old_memory) as f:
        content = f.read()

    # Check if there's actual Key Decisions content (not just placeholder)
    decisions = extract_section(content, 'Key Decisions', 50)
    if not decisions:
        return False

    # Create the native auto-memory directory and write migrated content
    native_path.parent.mkdir(parents=True, exist_ok=True)

    migrated = f"""# Project Memory (migrated from in-project .claude/memory/)

## Key Decisions

{decisions}

---
*Migrated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    with open(native_path, 'w') as f:
        f.write(migrated)

    print_info("Migrated Key Decisions from in-project MEMORY.md to native auto-memory")
    return True


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

## Decisions Made

*No decisions recorded yet today.*

## Issues Encountered

*No issues recorded yet today.*

## TODO / Follow-up

- [ ] *Add follow-up items as they arise*

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


def load_recent_learnings(max_count: int = 5) -> list:
    """Load the most recent learnings from learnings.json.

    Returns up to max_count learnings sorted by date descending.
    Returns empty list if file doesn't exist or is malformed.
    """
    learnings_file = get_memory_dir() / 'learnings.json'
    data = read_json_file(learnings_file)
    if not data or 'learnings' not in data or not isinstance(data['learnings'], list):
        return []

    try:
        # Sort by date descending, take most recent
        sorted_learnings = sorted(
            data['learnings'],
            key=lambda x: x.get('date', ''),
            reverse=True
        )
        return sorted_learnings[:max_count]
    except (TypeError, KeyError):
        return []


def get_last_session_date():
    """Get the most recent session date from .index.json.

    Returns datetime or None if unavailable.
    """
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
    """Load relevant memory context with progressive disclosure."""
    context = {
        'key_decisions': '',
        'known_issues': '',
        'lessons_learned': '',
        'recent_activity': '',
        'open_todos': [],
        'yesterday_summary': '',
        'recent_learnings': [],
        'session_gap_days': 0
    }
    
    # Load from native auto-memory MEMORY.md (~/.claude/projects/<project>/memory/)
    native_memory = get_native_auto_memory_path()
    if native_memory.exists():
        with open(native_memory) as f:
            content = f.read()

        context['key_decisions'] = extract_section(content, 'Key Decisions', 15)
        context['known_issues'] = extract_section(content, 'Known Issues & Workarounds', 10)
        context['lessons_learned'] = extract_section(content, 'Lessons Learned', 15)
    
    # Load today's TODOs
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

    # Load recent learnings
    context['recent_learnings'] = load_recent_learnings()

    # Detect session staleness
    last_session = get_last_session_date()
    if last_session:
        gap = (datetime.now() - last_session).days
        context['session_gap_days'] = gap

        # For stale sessions (>1 day), force-load Key Decisions and Known Issues
        # even if they contain placeholder text
        if gap > 1:
            native_memory = get_native_auto_memory_path()
            if native_memory.exists():
                with open(native_memory) as f:
                    content = f.read()

                # Re-extract without placeholder filtering
                for section_name, key in [('Key Decisions', 'key_decisions'), ('Known Issues & Workarounds', 'known_issues'), ('Lessons Learned', 'lessons_learned')]:
                    pattern = rf'^## {re.escape(section_name)}\s*\n(.*?)(?=^## |\Z)'
                    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
                    if match:
                        text = '\n'.join(match.group(1).strip().split('\n')[:20])
                        if text:
                            context[key] = text

    return context


def generate_context_rule(context: dict) -> str:
    """Generate the memory context rule file content."""
    parts = []
    
    parts.append("# Project Memory Context")
    parts.append("")
    parts.append("> **Action**: Save key decisions and insights to your auto-memory during this session.")
    parts.append("")
    parts.append("*Auto-loaded from `.claude/memory/` - Progressive disclosure of project context.*")
    parts.append("")

    # Session gap notice
    if context.get('session_gap_days', 0) > 3:
        parts.append(f"> Note: {context['session_gap_days']} days since last session. Review MEMORY.md for full context.")
        parts.append("")

    # Level 1: Critical context (always show)
    if context['open_todos']:
        parts.append("## 🎯 Open TODOs")
        for todo in context['open_todos'][:5]:  # Max 5 TODOs
            parts.append(f"- [ ] {todo}")
        parts.append("")
    
    if context['known_issues']:
        parts.append("## ⚠️ Known Issues")
        parts.append(context['known_issues'])
        parts.append("")
    
    # Level 2: Recent context
    if context['yesterday_summary']:
        parts.append("## 📅 Yesterday's Summary")
        parts.append(context['yesterday_summary'])
        parts.append("")
    
    if context['recent_activity']:
        parts.append("## 🕐 Recent Activity (Today)")
        parts.append(context['recent_activity'])
        parts.append("")
    
    # Level 2.5: Recent learnings
    if context.get('recent_learnings'):
        parts.append("## 💡 Recent Learnings")
        for l in context['recent_learnings']:
            ltype = l.get('type', 'general')
            desc = l.get('description', '')
            conf = l.get('confidence', 'medium')
            parts.append(f"- [{ltype}] {desc} (confidence: {conf})")
        parts.append("")

    # Level 3: Background context (condensed)
    if context['key_decisions']:
        parts.append("## 📋 Key Decisions")
        parts.append(context['key_decisions'])
        parts.append("")

    if context.get('lessons_learned'):
        parts.append("## 📖 Lessons Learned")
        parts.append(context['lessons_learned'])
        parts.append("")
    
    # Footer with pointer to full memory
    parts.append("---")
    parts.append("*Auto-memory: `~/.claude/projects/<project>/memory/` | Daily logs: `.claude/memory/daily/`*")
    
    return '\n'.join(parts)


def inject_memory_context():
    """Generate memory context rule file for Claude to auto-load."""
    context = load_memory_context()
    
    # Always generate the rule file — the auto-memory directive should always be present
    # Generate and write the context rule
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
        memory_dir = init_memory_structure()

        # One-time migration from in-project MEMORY.md to native auto-memory
        migrated = migrate_memory_to_native()

        # Initialize today's log
        daily_created = init_daily_log()
        if daily_created:
            print_info(f"📅 Daily log created for {datetime.now().strftime('%Y-%m-%d')}")
        
        # Inject memory context into rules (progressive disclosure)
        context_injected = inject_memory_context()
        if context_injected:
            print_info("🧠 Memory context loaded → .claude/rules/memory-context.md")
        
    except Exception as e:
        print_warning(f"Memory init warning: {e}")


if __name__ == '__main__':
    main()
