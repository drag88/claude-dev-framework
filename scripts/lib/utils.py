#!/usr/bin/env python3
"""
Cross-platform utility functions for CDF hook scripts.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any


def get_project_root() -> Path:
    """Get the current project root directory."""
    cwd = Path.cwd()

    # Look for common project markers
    markers = ['.git', 'package.json', 'pyproject.toml', 'Cargo.toml', 'go.mod']

    current = cwd
    while current != current.parent:
        for marker in markers:
            if (current / marker).exists():
                return current
        current = current.parent

    return cwd


def read_json_file(path: Path) -> Optional[Dict[str, Any]]:
    """Read and parse a JSON file."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def write_json_file(path: Path, data: Dict[str, Any]) -> bool:
    """Write data to a JSON file."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False


def run_command(cmd: list, cwd: Optional[Path] = None, timeout: int = 30) -> tuple:
    """
    Run a shell command and return (success, stdout, stderr).
    """
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or get_project_root(),
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return (result.returncode == 0, result.stdout, result.stderr)
    except subprocess.TimeoutExpired:
        return (False, '', 'Command timed out')
    except Exception as e:
        return (False, '', str(e))


def print_warning(message: str) -> None:
    """Print a warning message to stderr."""
    print(f"⚠️  Warning: {message}", file=sys.stderr)


def print_info(message: str) -> None:
    """Print an info message to stderr."""
    print(f"ℹ️  {message}", file=sys.stderr)


def is_test_file(path: str) -> bool:
    """Check if a file is a test file."""
    name = Path(path).name.lower()
    return any([
        '.test.' in name,
        '.spec.' in name,
        name.startswith('test_'),
        '/test/' in path.lower(),
        '/__tests__/' in path.lower()
    ])


def get_memory_dir() -> Path:
    """Get the .claude/memory directory path."""
    return get_project_root() / '.claude' / 'memory'


def get_daily_log_path() -> Path:
    """Get today's daily log path."""
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    return get_memory_dir() / 'daily' / f'{today}.md'


def get_native_auto_memory_path() -> Path:
    """Resolve the native auto-memory MEMORY.md path.

    Claude's auto-memory lives at ~/.claude/projects/<project-key>/memory/MEMORY.md
    where <project-key> replaces all non-alphanumeric chars (except -) with '-'.
    """
    import re
    project_root = str(get_project_root())
    project_key = re.sub(r'[^a-zA-Z0-9-]', '-', project_root)
    return Path.home() / '.claude' / 'projects' / project_key / 'memory' / 'MEMORY.md'
