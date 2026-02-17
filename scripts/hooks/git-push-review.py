#!/usr/bin/env python3
"""
PreToolUse hook: Remind to review before git push.
Provides a reminder to verify changes before pushing to remote.
"""

import json
import sys
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from utils import print_info, run_command


def get_unpushed_commits() -> int:
    """Count commits that haven't been pushed."""
    success, stdout, _ = run_command([
        'git', 'log', '@{u}..HEAD', '--oneline'
    ])

    if not success:
        # If no upstream, count all commits on current branch
        success, stdout, _ = run_command([
            'git', 'log', 'HEAD', '--oneline', '-n', '20'
        ])

    if success and stdout:
        return len(stdout.strip().split('\n'))
    return 0


def get_current_branch() -> str:
    """Get the current branch name."""
    success, stdout, _ = run_command(['git', 'branch', '--show-current'])
    return stdout.strip() if success else 'unknown'


def main():
    """Main entry point."""
    # Early exit: only run git checks when the bash command involves "push"
    if len(sys.argv) > 1:
        try:
            tool_input = json.loads(sys.argv[1])
            command = tool_input.get('command', '')
        except (json.JSONDecodeError, TypeError):
            command = ''
    else:
        command = ''

    if 'push' not in command:
        return

    branch = get_current_branch()
    commits = get_unpushed_commits()

    # Warn about pushing to main/master
    if branch in ['main', 'master']:
        print_info(f"Pushing directly to {branch} branch")
        print("  Consider using a feature branch and PR instead.", file=sys.stderr)

    # Show commit count
    if commits > 0:
        print_info(f"About to push {commits} commit(s) to {branch}")
        print("  Review checklist:", file=sys.stderr)
        print("  [ ] Tests pass locally", file=sys.stderr)
        print("  [ ] No debugging statements", file=sys.stderr)
        print("  [ ] Commit messages are clear", file=sys.stderr)


if __name__ == '__main__':
    main()
