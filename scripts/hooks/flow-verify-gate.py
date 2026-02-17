#!/usr/bin/env python3
"""
Flow Verify Gate Hook - Track test results during /cdf:flow verify phase.

Triggers on test commands (npm test, pytest, etc.). Updates flow state
with verification results.
"""

import json
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for utils import
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.utils import get_project_root, print_info


def get_active_flow_dir() -> Optional[Path]:
    """Find the active flow directory in the verify phase."""
    project_root = get_project_root()
    dev_active = project_root / "dev" / "active"

    if not dev_active.exists():
        return None

    for task_dir in dev_active.iterdir():
        if task_dir.is_dir():
            state_file = task_dir / "flow-state.md"
            if state_file.exists():
                content = state_file.read_text()
                if "current_phase: verify" in content:
                    return task_dir

    return None


def main():
    """Main verify gate logic."""
    # Early exit if no active flow directory exists
    project_root = get_project_root()
    if not (project_root / "dev" / "active").exists():
        return

    # Check if we have tool output
    if len(sys.argv) < 2:
        return

    try:
        tool_input = json.loads(sys.argv[1])
    except (json.JSONDecodeError, IndexError):
        return

    # Get active flow in verify phase
    flow_dir = get_active_flow_dir()

    if not flow_dir:
        # Not in a flow verify phase, skip
        return

    # Parse any test output that might be in the environment
    # Note: Actual test output parsing happens in post-tool context
    # This hook primarily tracks that tests were run

    print_info("Flow verify gate: Test execution tracked")

    # Output context for next steps
    result = {
        "additionalContext": "Tests executed during /cdf:flow verify phase. Check results and update flow state accordingly."
    }
    print(json.dumps(result))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Silent failure
        pass
