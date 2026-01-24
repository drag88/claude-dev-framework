#!/usr/bin/env python3
"""
Cross-platform utility functions for CDF hook scripts.
"""

import json
import os
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


def get_plugin_root() -> Path:
    """Get the CDF plugin root directory."""
    env_root = os.environ.get('CLAUDE_PLUGIN_ROOT')
    if env_root:
        return Path(env_root)

    # Fallback: assume we're in scripts/lib
    return Path(__file__).parent.parent.parent


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


def detect_package_manager() -> str:
    """Detect which package manager is used in the project."""
    root = get_project_root()

    # Check for lock files
    if (root / 'pnpm-lock.yaml').exists():
        return 'pnpm'
    elif (root / 'yarn.lock').exists():
        return 'yarn'
    elif (root / 'bun.lockb').exists():
        return 'bun'
    elif (root / 'package-lock.json').exists():
        return 'npm'

    # Default to npm if package.json exists
    if (root / 'package.json').exists():
        return 'npm'

    return 'npm'


def print_warning(message: str) -> None:
    """Print a warning message to stderr."""
    print(f"⚠️  Warning: {message}", file=sys.stderr)


def print_error(message: str) -> None:
    """Print an error message to stderr."""
    print(f"❌ Error: {message}", file=sys.stderr)


def print_info(message: str) -> None:
    """Print an info message to stderr."""
    print(f"ℹ️  {message}", file=sys.stderr)


def print_success(message: str) -> None:
    """Print a success message to stderr."""
    print(f"✅ {message}", file=sys.stderr)


def is_ci_environment() -> bool:
    """Check if running in a CI environment."""
    ci_vars = ['CI', 'GITHUB_ACTIONS', 'GITLAB_CI', 'CIRCLECI', 'JENKINS_URL']
    return any(os.environ.get(var) for var in ci_vars)


def get_file_extension(path: str) -> str:
    """Get the file extension from a path."""
    return Path(path).suffix.lower()


def is_typescript_file(path: str) -> bool:
    """Check if a file is TypeScript."""
    return get_file_extension(path) in ['.ts', '.tsx']


def is_javascript_file(path: str) -> bool:
    """Check if a file is JavaScript."""
    return get_file_extension(path) in ['.js', '.jsx', '.mjs', '.cjs']


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
