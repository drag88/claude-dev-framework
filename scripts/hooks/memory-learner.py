#!/usr/bin/env python3
"""
Stop hook: Extract learnings from today's daily log and store in learnings.json.
Detects correction patterns (repeated edits), related file patterns (same-dir edits),
and extracts explicit decisions and issues from dedicated sections.
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict
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


def parse_activity_log(content: str) -> list:
    """Extract activity entries from the Activity Log section.

    Returns list of dicts: {timestamp, type, path, detail}
    """
    activities = []

    # Isolate Activity Log section
    if '## Activity Log' not in content:
        return activities

    activity_section = content.split('## Activity Log')[-1]

    # Match entries like: - `HH:MM` - edited: `path/file`
    # or: - `HH:MM:SS` - created/updated: `path/file`
    pattern = r'-\s+`([^`]+)`\s+-\s+([\w/]+)(?::\s+`([^`]+)`)?(?:\s*-?\s*(.*))?'

    for line in activity_section.split('\n'):
        line = line.strip()
        if not line.startswith('- `'):
            continue

        match = re.match(pattern, line)
        if match:
            timestamp, action_type, path, detail = match.groups()
            activities.append({
                'timestamp': timestamp,
                'type': action_type.strip(),
                'path': path or '',
                'detail': (detail or '').strip()
            })

    return activities


def detect_corrections(activities: list) -> list:
    """Files edited 3+ times suggest correction patterns."""
    learnings = []

    # Count edits per file
    edit_counts = Counter()
    for act in activities:
        if act['type'] in ('edited', 'created/updated', 'updated'):
            if act['path']:
                edit_counts[act['path']] += 1

    for filepath, count in edit_counts.items():
        if count >= 3:
            learnings.append({
                'type': 'correction',
                'description': f"File '{filepath}' was edited {count} times in one session, suggesting iterative corrections",
                'confidence': 0.6,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'files': [filepath],
                'source': 'activity-log'
            })

    return learnings


def detect_related_patterns(activities: list) -> list:
    """3+ files in the same directory suggest related component patterns."""
    learnings = []

    # Group edited files by directory
    dir_files = defaultdict(set)
    for act in activities:
        if act['type'] in ('edited', 'created/updated', 'updated', 'created'):
            if act['path']:
                parent = str(Path(act['path']).parent)
                if parent and parent != '.':
                    dir_files[parent].add(act['path'])

    for directory, files in dir_files.items():
        if len(files) >= 3:
            learnings.append({
                'type': 'pattern',
                'description': f"Multiple related files ({len(files)}) edited in '{directory}', indicating tightly coupled components",
                'confidence': 0.5,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'files': sorted(files),
                'source': 'activity-log'
            })

    return learnings


def _is_placeholder(text: str) -> bool:
    """Check if section content is placeholder text (wrapped in *)."""
    stripped = text.strip()
    # Placeholder lines start and end with *
    lines = [l.strip() for l in stripped.split('\n') if l.strip()]
    return all(l.startswith('*') and l.endswith('*') for l in lines) if lines else True


def _extract_section(content: str, section_name: str) -> str:
    """Extract content of a named ## section."""
    pattern = rf'## {re.escape(section_name)}\s*\n(.*?)(?=\n## |\Z)'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else ''


def extract_decisions(content: str) -> list:
    """Read 'Decisions Made' section and extract as learnings."""
    learnings = []
    section = _extract_section(content, 'Decisions Made')

    if not section or _is_placeholder(section):
        return learnings

    # Each non-empty line that isn't a table header/separator is a decision
    for line in section.split('\n'):
        line = line.strip()
        if not line or line.startswith('|') or line.startswith('---'):
            continue
        # Strip leading bullet/dash
        line = re.sub(r'^[-*]\s+', '', line)
        if line:
            learnings.append({
                'type': 'decision',
                'description': line,
                'confidence': 0.9,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'files': [],
                'source': 'decisions-section'
            })

    return learnings


def extract_issues(content: str) -> list:
    """Read 'Issues Encountered' section and extract as learnings."""
    learnings = []
    section = _extract_section(content, 'Issues Encountered')

    if not section or _is_placeholder(section):
        return learnings

    for line in section.split('\n'):
        line = line.strip()
        if not line or line.startswith('|') or line.startswith('---'):
            continue
        line = re.sub(r'^[-*]\s+', '', line)
        if line:
            learnings.append({
                'type': 'issue',
                'description': line,
                'confidence': 0.8,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'files': [],
                'source': 'issues-section'
            })

    return learnings


def save_learnings(new_learnings: list):
    """Load existing learnings.json, append new, cap at 100, save."""
    learnings_path = get_memory_dir() / 'learnings.json'

    # Load existing
    data = {'learnings': [], 'last_updated': ''}
    if learnings_path.exists():
        try:
            with open(learnings_path) as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError):
            data = {'learnings': [], 'last_updated': ''}

    # Append new learnings
    data['learnings'].extend(new_learnings)

    # Cap at 100 entries — prune oldest first
    if len(data['learnings']) > 100:
        data['learnings'] = data['learnings'][-100:]

    data['last_updated'] = datetime.now().isoformat()

    # Ensure directory exists and save
    learnings_path.parent.mkdir(parents=True, exist_ok=True)
    with open(learnings_path, 'w') as f:
        json.dump(data, f, indent=2)


def main():
    """Orchestrate: read daily log, run all extractors, save if any learnings found."""
    try:
        memory_dir = get_memory_dir()
        if not memory_dir.exists():
            return

        log_path = get_daily_log_path()
        if not log_path.exists():
            return

        with open(log_path) as f:
            content = f.read()

        # Parse activity log
        activities = parse_activity_log(content)

        # Run all extractors
        all_learnings = []
        all_learnings.extend(detect_corrections(activities))
        all_learnings.extend(detect_related_patterns(activities))
        all_learnings.extend(extract_decisions(content))
        all_learnings.extend(extract_issues(content))

        # Save if any learnings found
        if all_learnings:
            save_learnings(all_learnings)
            print_info(f"Extracted {len(all_learnings)} learning(s) from today's session")

    except Exception:
        # Silent failure — don't disrupt session end
        pass


if __name__ == '__main__':
    main()
