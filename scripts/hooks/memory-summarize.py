#!/usr/bin/env python3
"""
Stop hook: Summarize session activity and update memory files.
Runs when the Claude Code session ends.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from utils import get_project_root, print_info, print_warning


def get_memory_dir() -> Path:
    """Get the memory directory path."""
    return get_project_root() / '.claude' / 'memory'


def get_daily_log_path() -> Path:
    """Get today's daily log path."""
    today = datetime.now().strftime('%Y-%m-%d')
    return get_memory_dir() / 'daily' / f'{today}.md'


def update_session_end_timestamp():
    """Add session end timestamp to daily log."""
    log_path = get_daily_log_path()
    
    if not log_path.exists():
        return
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    entry = f"- `{timestamp}` - Session ended\n"
    
    with open(log_path, 'a') as f:
        f.write(entry)


def count_activity_entries(log_path: Path) -> int:
    """Count the number of activity entries in the log."""
    if not log_path.exists():
        return 0
    
    with open(log_path) as f:
        content = f.read()
    
    # Count lines starting with "- `" in Activity Log section
    activity_section = content.split('## Activity Log')[-1] if '## Activity Log' in content else ''
    entries = [line for line in activity_section.split('\n') if line.strip().startswith('- `')]
    
    return len(entries)


def extract_files_changed(log_path: Path) -> list:
    """Extract list of files changed from the activity log."""
    if not log_path.exists():
        return []
    
    with open(log_path) as f:
        content = f.read()
    
    # Find all file paths in backticks after "edited:" or "created/updated:"
    pattern = r'(?:edited|created/updated): `([^`]+)`'
    matches = re.findall(pattern, content)
    
    return list(set(matches))  # Unique files


def update_memory_md_timestamp():
    """Update the 'Last updated' timestamp in MEMORY.md."""
    memory_file = get_memory_dir() / 'MEMORY.md'
    
    if not memory_file.exists():
        return
    
    with open(memory_file) as f:
        content = f.read()
    
    # Update last updated timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if '*Last updated:' in content:
        content = re.sub(
            r'\*Last updated: [^*]+\*',
            f'*Last updated: {timestamp}*',
            content
        )
    else:
        content += f"\n---\n*Last updated: {timestamp}*\n"
    
    with open(memory_file, 'w') as f:
        f.write(content)


def generate_session_stats() -> dict:
    """Generate statistics about the session."""
    log_path = get_daily_log_path()
    
    stats = {
        'activity_count': count_activity_entries(log_path),
        'files_changed': extract_files_changed(log_path),
        'ended_at': datetime.now().isoformat()
    }
    
    return stats


def save_session_index(stats: dict):
    """Save session statistics to index file."""
    index_file = get_memory_dir() / '.index.json'
    
    # Load existing index
    index = {}
    if index_file.exists():
        try:
            with open(index_file) as f:
                index = json.load(f)
        except:
            index = {}
    
    # Update with today's session
    today = datetime.now().strftime('%Y-%m-%d')
    
    if 'sessions' not in index:
        index['sessions'] = {}
    
    if today not in index['sessions']:
        index['sessions'][today] = []
    
    index['sessions'][today].append(stats)
    index['last_updated'] = datetime.now().isoformat()
    
    # Save index
    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)


def main():
    """Main entry point."""
    try:
        memory_dir = get_memory_dir()
        
        # Only proceed if memory is initialized
        if not memory_dir.exists():
            return
        
        # Update session end timestamp
        update_session_end_timestamp()
        
        # Generate and save stats
        stats = generate_session_stats()
        save_session_index(stats)
        
        # Update MEMORY.md timestamp
        update_memory_md_timestamp()
        
        # Print summary
        if stats['activity_count'] > 0:
            print_info(f"📊 Session logged: {stats['activity_count']} activities, {len(stats['files_changed'])} files changed")
        
    except Exception as e:
        # Don't fail session end on errors
        print_warning(f"Memory summarize warning: {e}")


if __name__ == '__main__':
    main()
