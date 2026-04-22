#!/usr/bin/env python3
"""
PreToolUse hook: Verify changelog, version, and documentation are updated before push.
Fires on Bash commands containing 'push'. Injects reminders as additionalContext
so Claude can fix missing items before the push goes through.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from utils import run_command, get_project_root


def get_changed_files():
    """Get files changed between HEAD and origin/main (or upstream)."""
    success, stdout, _ = run_command([
        'git', 'diff', '--name-only', 'origin/main...HEAD'
    ])
    if not success:
        # Fallback: diff against upstream tracking branch
        success, stdout, _ = run_command([
            'git', 'log', '@{u}..HEAD', '--name-only', '--format='
        ])
    if success and stdout:
        return [f for f in stdout.strip().split('\n') if f]
    return []


def has_code_changes(files):
    """Check if any changed files are actual code (not just docs/config)."""
    code_exts = {'.py', '.js', '.ts', '.tsx', '.jsx', '.rb', '.go', '.rs',
                 '.java', '.kt', '.swift', '.c', '.cpp', '.h', '.cs', '.sh'}
    doc_only = {'.md', '.txt', '.rst', '.json', '.yaml', '.yml', '.toml'}

    for f in files:
        ext = Path(f).suffix.lower()
        if ext in code_exts:
            return True
    return False


def check_changelog(files, project_root):
    """Check if CHANGELOG was updated when code changed."""
    changelog_names = ['CHANGELOG.md', 'CHANGES.md', 'HISTORY.md', 'changelog.md']

    # Find if project has a changelog
    existing = None
    for name in changelog_names:
        if (project_root / name).exists():
            existing = name
            break

    if existing is None:
        return None  # No changelog convention — skip

    if existing in files:
        return None  # Already updated

    return f"CHANGELOG ({existing}) not updated. Code changes should be documented."


def check_version(files, project_root):
    """Check if version was bumped when code changed."""
    version_files = ['VERSION', 'version.txt']
    version_in_config = [
        ('package.json', 'version'),
        ('pyproject.toml', 'version'),
        ('setup.cfg', 'version'),
        ('Cargo.toml', 'version'),
    ]

    # Check dedicated version files
    for vf in version_files:
        if (project_root / vf).exists():
            if vf in files:
                return None  # Updated
            return f"VERSION file ({vf}) not bumped. Consider updating the version."

    # Check version in config files
    for cfg, _ in version_in_config:
        if (project_root / cfg).exists() and cfg in files:
            return None  # Config file was touched — assume version handled

    return None  # No version convention detected — skip


def check_docs(files, project_root):
    """Check if README/docs updated when public API or commands change."""
    api_indicators = [
        'commands/', 'agents/', 'skills/', 'hooks/',  # CDF components
        'api/', 'routes/', 'endpoints/',                # API changes
        'src/cli', 'bin/',                              # CLI changes
    ]

    touches_public_surface = any(
        any(indicator in f for indicator in api_indicators)
        for f in files
    )

    if not touches_public_surface:
        return None

    doc_files = {'README.md', 'docs/', 'CLAUDE.md'}
    docs_updated = any(
        any(f.startswith(d) or f == d for d in doc_files)
        for f in files
    )

    if docs_updated:
        return None

    return "Public API/commands changed but documentation not updated. Consider updating README.md or docs/."


def main():
    try:
        hook_data = json.load(sys.stdin)
        command = hook_data.get('tool_input', {}).get('command', '')
    except (json.JSONDecodeError, Exception):
        return

    # Only fire on git push commands
    if 'push' not in command or 'git' not in command:
        return

    project_root = get_project_root()
    files = get_changed_files()

    if not files:
        return

    # For CDF repo, .md files in commands/agents/skills ARE code
    is_cdf = (project_root / '.claude-plugin' / 'plugin.json').exists()
    if not is_cdf and not has_code_changes(files):
        return

    # Run health check first — block on failure
    health_check = project_root / 'scripts' / 'health-check.py'
    if health_check.exists():
        import subprocess
        result = subprocess.run(
            ['python3', str(health_check)],
            capture_output=True, text=True, cwd=str(project_root)
        )
        if result.returncode != 0:
            print(json.dumps({
                "decision": "block",
                "reason": f"Health check failed. Fix before pushing:\n{result.stdout.strip()}"
            }))
            return

    warnings = []
    for check in [check_changelog, check_version, check_docs]:
        result = check(files, project_root)
        if result:
            warnings.append(result)

    if not warnings:
        return

    # Warn on issues (docs, changelog, version) — never block. Gating belongs in CI.
    context = "PRE-PUSH CHECK — the following items may need attention before pushing:\n"
    for i, w in enumerate(warnings, 1):
        context += f"  {i}. {w}\n"
    context += "\nAsk the user if they want to fix these before pushing, or proceed anyway."

    print(json.dumps({"additionalContext": context}))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        from datetime import datetime
        log_dir = Path.home() / '.cdf-logs'
        log_dir.mkdir(exist_ok=True)
        with open(log_dir / 'hook-errors.log', 'a') as f:
            f.write(f"{datetime.now().isoformat()} [pre-push-checks.py] {e}\n")
