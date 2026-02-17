#!/usr/bin/env python3
"""
Stop hook: Summarize session activity and update memory files.
Runs when the Claude Code session ends.
"""

import json
import os
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from utils import get_project_root, print_info, print_warning, write_json_file


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


def fill_session_summary(log_path: Path):
    """Fill the Session Summary section with actual data."""
    if not log_path.exists():
        return

    with open(log_path) as f:
        content = f.read()

    if '*Session in progress...*' not in content:
        return  # Already filled

    # Count activities
    activity_count = count_activity_entries(log_path)
    files = extract_files_changed(log_path)
    file_count = len(files)

    # Count unique directories
    dirs = set()
    for f in files:
        parent = str(Path(f).parent)
        if parent != '.':
            dirs.add(parent)
    dir_count = len(dirs) if dirs else 0

    # Build summary
    summary_lines = []
    summary_lines.append(f"Edited {file_count} files across {dir_count} directories. {activity_count} total activities.")

    # Find most-edited files (count occurrences, not just unique)
    if files:
        # Re-extract with duplicates to count edits per file
        pattern = r'(?:edited|created/updated): `([^`]+)`'
        all_matches = re.findall(pattern, content)
        file_counts = Counter(all_matches)
        top_files = file_counts.most_common(5)
        if top_files:
            summary_lines.append("")
            summary_lines.append("Most-edited files:")
            for fpath, count in top_files:
                # Make path relative if possible
                try:
                    rel = str(Path(fpath).relative_to(get_project_root()))
                except ValueError:
                    rel = fpath
                summary_lines.append(f"- `{rel}` ({count} edits)")

    summary_text = '\n'.join(summary_lines)
    content = content.replace('*Session in progress...*', summary_text)

    with open(log_path, 'w') as f:
        f.write(content)


def fill_changes_table(log_path: Path):
    """Fill the Changes Made table from Activity Log entries."""
    if not log_path.exists():
        return

    with open(log_path) as f:
        content = f.read()

    # Check for placeholder table
    if '| - | - | - |' not in content:
        return  # Already filled

    # Parse activity log for file changes
    pattern = r'- `[^`]+` - (edited|created/updated): `([^`]+)`(?:\s*\|\s*(.*))?'
    matches = re.findall(pattern, content)

    if not matches:
        return  # No file changes to record

    # Build table rows, deduplicating by file (keep last action)
    seen = {}
    for action, fpath, reason in matches:
        # Make path relative
        try:
            rel = str(Path(fpath).relative_to(get_project_root()))
        except ValueError:
            rel = fpath
        action_type = 'edited' if action == 'edited' else 'created'
        reason_text = reason.strip().strip('"') if reason else '-'
        seen[rel] = (action_type, reason_text)

    # Build rows, cap at 20
    rows = []
    for fpath, (action_type, reason_text) in list(seen.items())[:20]:
        rows.append(f"| `{fpath}` | {action_type} | {reason_text} |")

    if rows:
        table_content = '\n'.join(rows)
        content = content.replace('| - | - | - |', table_content)

        with open(log_path, 'w') as f:
            f.write(content)


def parse_activity_log(content: str) -> list:
    """Extract activity entries from the Activity Log section.

    Returns list of dicts: {timestamp, type, path, detail}
    """
    activities = []

    if '## Activity Log' not in content:
        return activities

    activity_section = content.split('## Activity Log')[-1]

    # Match entries like: - `HH:MM` - edited: `path/file`
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

    for line in section.split('\n'):
        line = line.strip()
        if not line or line.startswith('|') or line.startswith('---'):
            continue
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

    data = {'learnings': [], 'last_updated': ''}
    if learnings_path.exists():
        try:
            with open(learnings_path) as f:
                data = json.load(f)
        except (json.JSONDecodeError, KeyError):
            data = {'learnings': [], 'last_updated': ''}

    data['learnings'].extend(new_learnings)

    if len(data['learnings']) > 100:
        data['learnings'] = data['learnings'][-100:]

    data['last_updated'] = datetime.now().isoformat()

    learnings_path.parent.mkdir(parents=True, exist_ok=True)
    with open(learnings_path, 'w') as f:
        json.dump(data, f, indent=2)


def extract_and_save_learnings(log_path: Path):
    """Extract learnings from daily log and save to learnings.json."""
    if not log_path.exists():
        return

    with open(log_path) as f:
        content = f.read()

    activities = parse_activity_log(content)

    all_learnings = []
    all_learnings.extend(detect_corrections(activities))
    all_learnings.extend(detect_related_patterns(activities))
    all_learnings.extend(extract_decisions(content))
    all_learnings.extend(extract_issues(content))

    if all_learnings:
        save_learnings(all_learnings)
        print_info(f"Extracted {len(all_learnings)} learning(s) from today's session")


def propagate_learnings_to_memory():
    """Propagate high-confidence learnings from learnings.json to MEMORY.md."""
    memory_dir = get_memory_dir()
    learnings_file = memory_dir / 'learnings.json'
    memory_file = memory_dir / 'MEMORY.md'

    if not learnings_file.exists() or not memory_file.exists():
        return

    try:
        with open(learnings_file) as f:
            data = json.load(f)
    except (json.JSONDecodeError, KeyError):
        return

    learnings = data.get('learnings', [])
    if not learnings:
        return

    with open(memory_file) as f:
        memory_content = f.read()

    # Map learning types to MEMORY.md sections
    section_map = {
        'decision': '## Key Decisions',
        'issue': '## Known Issues & Workarounds',
        'pattern': '## Patterns & Conventions',
        'correction': '## Patterns & Conventions',
    }

    # Placeholder text to replace when first entry is added
    placeholders = {
        '## Key Decisions': '*No decisions recorded yet.*',
        '## Known Issues & Workarounds': '*No known issues documented yet.*',
        '## Patterns & Conventions': '*Project-specific patterns will be documented here.*',
    }

    modified = False

    for learning in learnings:
        confidence = learning.get('confidence', 0)
        if confidence <= 0.7:
            continue

        learning_type = learning.get('type', '')
        description = learning.get('description', '')
        date = learning.get('date', datetime.now().strftime('%Y-%m-%d'))

        if not description or learning_type not in section_map:
            continue

        section_header = section_map[learning_type]

        # Deduplicate: skip if description substring already in MEMORY.md
        if description in memory_content:
            continue

        entry = f"- [{date}] {description}"

        # Find section and append entry
        if section_header in memory_content:
            # Check if placeholder needs replacing
            placeholder = placeholders.get(section_header, '')
            if placeholder and placeholder in memory_content:
                memory_content = memory_content.replace(placeholder, entry)
            else:
                # Append after last line in section (before next ## or ---)
                # Find position after section header
                section_start = memory_content.index(section_header) + len(section_header)
                # Find next section or end marker
                rest = memory_content[section_start:]
                next_section = re.search(r'\n## |\n---', rest)
                if next_section:
                    insert_pos = section_start + next_section.start()
                else:
                    insert_pos = len(memory_content)

                memory_content = memory_content[:insert_pos] + '\n' + entry + memory_content[insert_pos:]

            modified = True

    if modified:
        with open(memory_file, 'w') as f:
            f.write(memory_content)
        print_info("Propagated learnings to MEMORY.md")


def cap_memory_md_size(max_bytes: int = 4096):
    """Cap MEMORY.md size by trimming oldest bullet entries from each section."""
    memory_file = get_memory_dir() / 'MEMORY.md'

    if not memory_file.exists():
        return

    with open(memory_file) as f:
        content = f.read()

    if len(content.encode('utf-8')) <= max_bytes:
        return

    # Split into sections, trim oldest bullets (first bullet in each section) iteratively
    lines = content.split('\n')

    # Keep trimming until under limit
    max_iterations = 50  # Safety guard
    iteration = 0
    while len('\n'.join(lines).encode('utf-8')) > max_bytes and iteration < max_iterations:
        iteration += 1
        trimmed = False

        # Find sections with bullet entries, trim the oldest (first) bullet in longest section
        sections = []  # (section_name, first_bullet_line_index)
        current_section = None
        bullet_indices = []

        for i, line in enumerate(lines):
            if line.startswith('## '):
                if current_section and bullet_indices:
                    sections.append((current_section, bullet_indices))
                current_section = line
                bullet_indices = []
            elif line.startswith('- ') and current_section:
                bullet_indices.append(i)

        # Don't forget last section
        if current_section and bullet_indices:
            sections.append((current_section, bullet_indices))

        # Find section with most bullets and remove its oldest (first) entry
        if sections:
            sections.sort(key=lambda x: len(x[1]), reverse=True)
            longest_section, indices = sections[0]
            if len(indices) > 1:  # Keep at least one entry
                lines.pop(indices[0])
                trimmed = True

        if not trimmed:
            break

    with open(memory_file, 'w') as f:
        f.write('\n'.join(lines))

    print_info("Trimmed MEMORY.md to stay under size cap")


def archive_old_logs():
    """Archive daily logs older than 14 days."""
    memory_dir = get_memory_dir()
    daily_dir = memory_dir / 'daily'
    archive_dir = memory_dir / 'archive'

    if not daily_dir.exists():
        return

    threshold_date = datetime.now() - timedelta(days=14)
    archived_count = 0

    for log_file in daily_dir.glob('*.md'):
        # Extract date from filename (YYYY-MM-DD.md)
        try:
            date_str = log_file.stem
            file_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            continue

        if file_date < threshold_date:
            archive_month = file_date.strftime('%Y-%m')
            archive_path = archive_dir / archive_month

            try:
                archive_path.mkdir(parents=True, exist_ok=True)
                shutil.move(str(log_file), str(archive_path / log_file.name))
                archived_count += 1
            except Exception as e:
                print_warning(f"Failed to archive {log_file.name}: {e}")

    if archived_count > 0:
        print_info(f"Archived {archived_count} old daily log(s)")


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


def save_session_state():
    """Save session state to .claude/sessions/ for potential recovery."""
    state_dir = get_project_root() / '.claude' / 'sessions'
    state_dir.mkdir(parents=True, exist_ok=True)

    session_id = os.environ.get('CLAUDE_SESSION_ID', 'unknown')
    state_file = state_dir / f'session-{session_id}.json'

    summary = {
        'ended_at': datetime.now().isoformat(),
        'project_root': str(get_project_root()),
        'cwd': os.getcwd()
    }

    if write_json_file(state_file, summary):
        print_info("Session state saved")


def main():
    """Main entry point."""
    try:
        # 0. Save session state (independent of memory system)
        save_session_state()

        memory_dir = get_memory_dir()

        # Only proceed if memory is initialized
        if not memory_dir.exists():
            return

        log_path = get_daily_log_path()

        # 1. Update session end timestamp
        update_session_end_timestamp()

        # 2. Fill session summary
        fill_session_summary(log_path)

        # 3. Fill changes table
        fill_changes_table(log_path)

        # 4. Generate and save stats
        stats = generate_session_stats()
        save_session_index(stats)

        # 5. Extract learnings from daily log into learnings.json
        extract_and_save_learnings(log_path)

        # 6. Propagate learnings to MEMORY.md
        propagate_learnings_to_memory()

        # 7. Cap MEMORY.md size
        cap_memory_md_size()

        # 8. Archive old logs
        archive_old_logs()

        # 9. Update MEMORY.md timestamp
        update_memory_md_timestamp()

        # Print summary
        if stats['activity_count'] > 0:
            print_info(f"Session logged: {stats['activity_count']} activities, {len(stats['files_changed'])} files changed")

    except Exception as e:
        # Don't fail session end on errors
        print_warning(f"Memory summarize warning: {e}")


if __name__ == '__main__':
    main()
