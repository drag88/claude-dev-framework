#!/usr/bin/env python3
"""
Flow Verify Gate Hook - Track test results during /cdf:flow verify phase.

Triggers on test commands (npm test, pytest, etc.). Updates flow state
with verification results.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for utils import
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.utils import get_project_root, print_info, print_warning, print_success, print_error


def get_active_flow_dir() -> Path | None:
    """Find the active flow directory."""
    project_root = get_project_root()
    dev_active = project_root / "dev" / "active"

    if not dev_active.exists():
        return None

    for task_dir in dev_active.iterdir():
        if task_dir.is_dir():
            state_file = task_dir / "flow-state.md"
            if state_file.exists():
                content = state_file.read_text()
                # Check if in verify phase
                if "current_phase: verify" in content:
                    return task_dir

    return None


def parse_test_output(tool_output: str) -> dict:
    """Parse test output to extract results."""
    result = {
        "passed": False,
        "tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "coverage": None,
        "errors": []
    }

    # Common test result patterns
    # Jest/Vitest pattern: "Tests: X passed, Y failed, Z total"
    jest_match = re.search(r'Tests:\s*(\d+)\s*passed.*?(\d+)\s*failed.*?(\d+)\s*total', tool_output, re.IGNORECASE)
    if jest_match:
        result["tests_passed"] = int(jest_match.group(1))
        result["tests_failed"] = int(jest_match.group(2))
        result["tests_run"] = int(jest_match.group(3))
        result["passed"] = result["tests_failed"] == 0

    # Pytest pattern: "X passed, Y failed"
    pytest_match = re.search(r'(\d+)\s*passed.*?(\d+)\s*failed', tool_output, re.IGNORECASE)
    if pytest_match:
        result["tests_passed"] = int(pytest_match.group(1))
        result["tests_failed"] = int(pytest_match.group(2))
        result["tests_run"] = result["tests_passed"] + result["tests_failed"]
        result["passed"] = result["tests_failed"] == 0

    # Pytest success pattern: "X passed"
    pytest_success = re.search(r'(\d+)\s*passed(?!.*failed)', tool_output, re.IGNORECASE)
    if pytest_success and not pytest_match:
        result["tests_passed"] = int(pytest_success.group(1))
        result["tests_run"] = result["tests_passed"]
        result["passed"] = True

    # Coverage pattern
    coverage_match = re.search(r'Coverage:\s*(\d+(?:\.\d+)?)\s*%', tool_output, re.IGNORECASE)
    if coverage_match:
        result["coverage"] = float(coverage_match.group(1))

    # Alternative coverage: "All files | XX.XX |"
    alt_coverage = re.search(r'All files\s*\|\s*(\d+(?:\.\d+)?)', tool_output)
    if alt_coverage:
        result["coverage"] = float(alt_coverage.group(1))

    # Check for general success indicators
    if not result["tests_run"]:
        if "PASS" in tool_output and "FAIL" not in tool_output:
            result["passed"] = True
        elif "OK" in tool_output and "FAILED" not in tool_output:
            result["passed"] = True

    # Extract error messages
    error_lines = re.findall(r'(?:Error|FAIL|FAILED):\s*(.+)', tool_output, re.IGNORECASE)
    result["errors"] = error_lines[:5]  # Limit to 5 errors

    return result


def update_flow_state_verify(flow_dir: Path, test_result: dict) -> None:
    """Update flow state with verification results."""
    state_file = flow_dir / "flow-state.md"

    if not state_file.exists():
        return

    content = state_file.read_text()
    now = datetime.now().isoformat()

    # Update last_updated
    content = re.sub(r'last_updated:\s*[\w\-:.]+', f'last_updated: {now}', content)

    # Update verify phase status
    if test_result["passed"]:
        content = re.sub(
            r'verify:\s*\{[^}]*\}',
            f'verify: {{ status: completed, gate_passed: true, tests_passed: {test_result["tests_passed"]}, coverage: {test_result.get("coverage", "null")} }}',
            content
        )
    else:
        content = re.sub(
            r'verify:\s*\{[^}]*\}',
            f'verify: {{ status: in_progress, gate_passed: false, tests_failed: {test_result["tests_failed"]} }}',
            content
        )

    state_file.write_text(content)


def main():
    """Main verify gate logic."""
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
