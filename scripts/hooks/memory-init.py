#!/usr/bin/env python3
"""
SessionStart hook: Initialize project memory structure and inject context.
Creates .claude/memory/ directory and loads relevant context via progressive disclosure.
"""

import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from utils import get_project_root, print_info, print_warning


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


def get_project_name() -> str:
    """Get the project name from directory or package.json."""
    project_root = get_project_root()
    
    # Try package.json
    package_json = project_root / 'package.json'
    if package_json.exists():
        try:
            with open(package_json) as f:
                data = json.load(f)
                if 'name' in data:
                    return data['name']
        except:
            pass
    
    # Try pyproject.toml
    pyproject = project_root / 'pyproject.toml'
    if pyproject.exists():
        try:
            with open(pyproject) as f:
                for line in f:
                    if line.startswith('name'):
                        return line.split('=')[1].strip().strip('"\'')
        except:
            pass
    
    # Fall back to directory name
    return project_root.name


def init_memory_md():
    """Create MEMORY.md if it doesn't exist."""
    memory_file = get_memory_dir() / 'MEMORY.md'
    
    if memory_file.exists():
        return False
    
    project_name = get_project_name()
    project_root = get_project_root()
    
    # Detect project type
    project_type = "Unknown"
    if (project_root / 'package.json').exists():
        project_type = "Node.js/JavaScript"
    elif (project_root / 'pyproject.toml').exists() or (project_root / 'setup.py').exists():
        project_type = "Python"
    elif (project_root / 'Cargo.toml').exists():
        project_type = "Rust"
    elif (project_root / 'go.mod').exists():
        project_type = "Go"
    
    content = f"""# Project Memory

## Project Overview

**Name**: {project_name}
**Type**: {project_type}
**Root**: {project_root}

[Add project description here]

## Key Decisions

*No decisions recorded yet.*

## Architecture Notes

*Architecture documentation will be added as the project evolves.*

## Patterns & Conventions

*Project-specific patterns will be documented here.*

## Known Issues & Workarounds

*No known issues documented yet.*

## Important Context

*Domain knowledge and business rules will be captured here.*

---
*Memory initialized: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open(memory_file, 'w') as f:
        f.write(content)
    
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


def load_memory_context() -> dict:
    """Load relevant memory context with progressive disclosure."""
    context = {
        'project_overview': '',
        'key_decisions': '',
        'known_issues': '',
        'recent_activity': '',
        'open_todos': [],
        'yesterday_summary': ''
    }
    
    # Load from MEMORY.md
    memory_file = get_memory_dir() / 'MEMORY.md'
    if memory_file.exists():
        with open(memory_file) as f:
            content = f.read()
        
        context['project_overview'] = extract_section(content, 'Project Overview', 10)
        context['key_decisions'] = extract_section(content, 'Key Decisions', 15)
        context['known_issues'] = extract_section(content, 'Known Issues & Workarounds', 10)
    
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
        if summary and '*Session in progress*' not in summary:
            context['yesterday_summary'] = summary
    
    return context


def generate_context_rule(context: dict) -> str:
    """Generate the memory context rule file content."""
    parts = []
    
    parts.append("# Project Memory Context")
    parts.append("")
    parts.append("*Auto-loaded from `.claude/memory/` - Progressive disclosure of project context.*")
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
    
    # Level 3: Background context (condensed)
    if context['key_decisions']:
        parts.append("## 📋 Key Decisions")
        parts.append(context['key_decisions'])
        parts.append("")
    
    # Footer with pointer to full memory
    parts.append("---")
    parts.append("*Full memory: `.claude/memory/MEMORY.md` | Daily logs: `.claude/memory/daily/`*")
    
    return '\n'.join(parts)


def inject_memory_context():
    """Generate memory context rule file for Claude to auto-load."""
    context = load_memory_context()
    
    # Check if there's any meaningful content
    has_content = (
        context['open_todos'] or
        context['known_issues'] or
        context['yesterday_summary'] or
        context['recent_activity'] or
        context['key_decisions']
    )
    
    if not has_content:
        return False
    
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
        
        # Initialize MEMORY.md
        memory_created = init_memory_md()
        if memory_created:
            print_info("📝 Project memory initialized")
        
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
