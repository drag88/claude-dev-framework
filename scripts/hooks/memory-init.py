#!/usr/bin/env python3
"""
SessionStart hook: Initialize project memory structure and load context.
Creates .claude/memory/ directory and files if they don't exist.
"""

import json
import os
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


def load_recent_context() -> str:
    """Load relevant context from recent memory."""
    context_parts = []
    
    # Load MEMORY.md summary (first 50 lines or until first ---)
    memory_file = get_memory_dir() / 'MEMORY.md'
    if memory_file.exists():
        with open(memory_file) as f:
            lines = f.readlines()
            summary_lines = []
            for line in lines[:50]:
                if line.strip() == '---':
                    break
                summary_lines.append(line)
            if summary_lines:
                context_parts.append("## From MEMORY.md\n" + ''.join(summary_lines))
    
    # Load today's log if exists
    today = datetime.now().strftime('%Y-%m-%d')
    today_file = get_daily_dir() / f'{today}.md'
    if today_file.exists():
        with open(today_file) as f:
            content = f.read()
            # Extract TODO section if present
            if '## TODO' in content:
                todo_section = content.split('## TODO')[1].split('##')[0]
                if todo_section.strip():
                    context_parts.append(f"## Today's TODOs\n{todo_section.strip()}")
    
    # Load yesterday's summary
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    yesterday_file = get_daily_dir() / f'{yesterday}.md'
    if yesterday_file.exists():
        with open(yesterday_file) as f:
            content = f.read()
            # Extract summary section
            if '## Session Summary' in content:
                summary = content.split('## Session Summary')[1].split('##')[0]
                if summary.strip() and '*Session in progress*' not in summary:
                    context_parts.append(f"## Yesterday's Summary\n{summary.strip()}")
    
    return '\n\n'.join(context_parts) if context_parts else ''


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
        
        # Load and output context (for Claude to pick up)
        context = load_recent_context()
        if context:
            print_info("📚 Memory context loaded")
            # Output context summary to stdout for potential use
            # print(f"\n--- PROJECT MEMORY CONTEXT ---\n{context}\n--- END CONTEXT ---\n")
        
    except Exception as e:
        print_warning(f"Memory init warning: {e}")


if __name__ == '__main__':
    main()
