#!/usr/bin/env python3
"""
SessionStart hook: Inject session context from git history and Claude's auto-memory.

Generates additionalContext by reading recent git activity and the project's
native auto-memory file. No files written — pure context injection.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from utils import get_project_root, get_native_auto_memory_path


SUBPROCESS_TIMEOUT = 10  # seconds per git command


def run_git(args: list[str], cwd: Path) -> str:
    """Run a git command and return stdout, or empty string on failure."""
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=SUBPROCESS_TIMEOUT,
        )
        return result.stdout.strip() if result.returncode == 0 else ''
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ''


def get_git_context(project_root: Path) -> str:
    """Gather recent git context."""
    sections = []

    # Current branch
    branch = run_git(['branch', '--show-current'], project_root)
    if branch:
        sections.append(f"Branch: {branch}")

    # Uncommitted changes
    status = run_git(['status', '--short'], project_root)
    if status:
        lines = status.splitlines()
        sections.append(f"Uncommitted changes ({len(lines)} files):\n{status}")
    else:
        sections.append("Working tree clean")

    # Recent commits
    log = run_git(['log', '--oneline', '-20', '--no-decorate'], project_root)
    if log:
        sections.append(f"Recent commits:\n{log}")

    # What changed recently (diff stat of last 5 commits)
    diff_stat = run_git(['diff', '--stat', 'HEAD~5', 'HEAD'], project_root)
    if diff_stat:
        sections.append(f"Recent committed changes:\n{diff_stat}")

    # Uncommitted diff stat (staged + unstaged combined)
    uncommitted_stat = run_git(['diff', '--stat', 'HEAD'], project_root)
    if uncommitted_stat:
        sections.append(f"Uncommitted change scope:\n{uncommitted_stat}")

    return '\n\n'.join(sections)


def get_memory_context() -> str:
    """Read Claude's native auto-memory for semantic context."""
    memory_path = get_native_auto_memory_path()

    if not memory_path.exists():
        return ''

    try:
        content = memory_path.read_text()
        # Truncate to ~2000 chars to avoid bloating context
        if len(content) > 2000:
            content = content[:2000] + '\n\n[... truncated]'
        return content
    except OSError:
        return ''


def build_context() -> str:
    """Build the full session context string."""
    project_root = get_project_root()
    parts = ['## Session Context (auto-generated)\n']

    # Git context
    git_ctx = get_git_context(project_root)
    if git_ctx:
        parts.append(f'### Git State\n{git_ctx}')

    # Auto-memory context
    memory_ctx = get_memory_context()
    if memory_ctx:
        parts.append(f'### Project Memory\n{memory_ctx}')

    return '\n\n'.join(parts)


def main():
    context = build_context()
    if context:
        print(json.dumps({'additionalContext': context}))
    else:
        print(json.dumps({}))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        from datetime import datetime
        log_dir = Path.home() / '.cdf-logs'
        log_dir.mkdir(exist_ok=True)
        with open(log_dir / 'hook-errors.log', 'a') as f:
            f.write(f"{datetime.now().isoformat()} [session-context.py] {e}\n")
