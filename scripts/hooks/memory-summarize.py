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
from collections import Counter
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


def get_native_auto_memory_path() -> Path:
    """Get path to native auto-memory MEMORY.md.

    Native auto-memory lives at ~/.claude/projects/<project-key>/memory/MEMORY.md
    where <project-key> replaces all non-alphanumeric chars (except -) with '-'.
    """
    project_root = str(get_project_root())
    project_key = re.sub(r'[^a-zA-Z0-9-]', '-', project_root)
    return Path.home() / '.claude' / 'projects' / project_key / 'memory' / 'MEMORY.md'


def write_session_recap_to_auto_memory(log_path: Path):
    """Write a 2-3 line session recap to native auto-memory MEMORY.md."""
    if not log_path.exists():
        return

    with open(log_path) as f:
        content = f.read()

    activities = parse_activity_log(content)
    if not activities:
        return

    # Count files edited and searches done
    files_edited = set()
    searches = []
    dirs_touched = set()

    for act in activities:
        if act['type'] in ('edited', 'created/updated', 'updated', 'created'):
            if act['path']:
                files_edited.add(act['path'])
                parent = str(Path(act['path']).parent)
                if parent and parent != '.':
                    dirs_touched.add(parent)
        elif act['type'] in ('searched', 'grepped', 'search'):
            if act['detail']:
                searches.append(act['detail'].strip('"').strip("'"))

    # Build recap lines
    today = datetime.now().strftime('%Y-%m-%d')
    parts = []

    if files_edited:
        # Show up to 4 file basenames
        basenames = [Path(f).name for f in sorted(files_edited)]
        if len(basenames) <= 4:
            files_str = ', '.join(basenames)
        else:
            files_str = ', '.join(basenames[:4]) + f', +{len(basenames) - 4} more'
        parts.append(f"Edited {len(files_edited)} files ({files_str}).")

    if searches:
        unique_searches = list(dict.fromkeys(searches))[:3]
        parts.append(f"Researched: {', '.join(unique_searches)}.")

    if dirs_touched:
        sorted_dirs = sorted(dirs_touched)
        if len(sorted_dirs) <= 3:
            dirs_str = ', '.join(sorted_dirs)
        else:
            dirs_str = ', '.join(sorted_dirs[:3]) + f', +{len(sorted_dirs) - 3} more'
        parts.append(f"Key areas: {dirs_str}.")

    if not parts:
        parts.append(f"{len(activities)} activities logged.")

    recap = f"## Session: {today}\n" + ' '.join(parts) + "\n"

    # Write to native auto-memory
    memory_path = get_native_auto_memory_path()
    memory_path.parent.mkdir(parents=True, exist_ok=True)

    if memory_path.exists():
        with open(memory_path) as f:
            existing = f.read()
    else:
        existing = "# Project Memory\n\n*Auto-maintained by CDF hooks.*\n\n"

    existing += '\n' + recap

    # Cap at 200 lines (native auto-memory only loads first 200)
    lines = existing.split('\n')
    if len(lines) > 200:
        lines = lines[:200]
        existing = '\n'.join(lines)

    with open(memory_path, 'w') as f:
        f.write(existing)

    print_info(f"Session recap written to native auto-memory")


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

        # 5. Write session recap to native auto-memory
        write_session_recap_to_auto_memory(log_path)

        # 6. Archive old logs
        archive_old_logs()

        # Print summary
        if stats['activity_count'] > 0:
            print_info(f"Session logged: {stats['activity_count']} activities, {len(stats['files_changed'])} files changed")

    except Exception as e:
        # Don't fail session end on errors
        print_warning(f"Memory summarize warning: {e}")


if __name__ == '__main__':
    main()
