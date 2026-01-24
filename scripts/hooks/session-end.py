#!/usr/bin/env python3
"""
Stop hook: Perform cleanup and save session state.
Runs when the Claude Code session ends.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from utils import get_project_root, write_json_file, print_info


def get_session_summary() -> dict:
    """Gather session summary information."""
    return {
        'ended_at': datetime.now().isoformat(),
        'project_root': str(get_project_root()),
        'cwd': os.getcwd()
    }


def save_session_state():
    """Save session state for potential recovery."""
    state_dir = get_project_root() / '.claude' / 'sessions'
    state_dir.mkdir(parents=True, exist_ok=True)

    session_id = os.environ.get('CLAUDE_SESSION_ID', 'unknown')
    state_file = state_dir / f'session-{session_id}.json'

    summary = get_session_summary()

    if write_json_file(state_file, summary):
        print_info(f"Session state saved")


def main():
    """Main entry point."""
    try:
        save_session_state()
    except Exception as e:
        # Don't fail session end on errors
        pass


if __name__ == '__main__':
    main()
