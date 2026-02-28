#!/usr/bin/env python3
"""
Flow Checkpoint Hook - Auto-checkpoint during /cdf:flow execution.

Triggers on Edit/Write/MultiEdit tools. Creates checkpoints every 20 tool calls
to enable workflow recovery.
"""

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add parent directory to path for utils import
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.utils import get_project_root, print_info, print_warning


def get_active_flow_dir() -> Optional[Path]:
    """Find the active flow directory."""
    project_root = get_project_root()
    dev_active = project_root / "dev" / "active"

    if not dev_active.exists():
        return None

    # Find directories with flow-state.md
    for task_dir in dev_active.iterdir():
        if task_dir.is_dir():
            state_file = task_dir / "flow-state.md"
            if state_file.exists():
                # Check if flow is in_progress
                content = state_file.read_text()
                if "status: in_progress" in content or "current_phase:" in content:
                    return task_dir

    return None


def parse_flow_state(state_file: Path) -> dict:
    """Parse flow-state.md YAML frontmatter."""
    content = state_file.read_text()

    # Extract YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()

            # Simple YAML parsing for key fields
            state = {}
            for line in frontmatter.split("\n"):
                if ":" in line and not line.strip().startswith("-"):
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    if value and not value.startswith("{"):
                        state[key] = value

            return state

    return {}


def update_tool_call_count(state_file: Path) -> int:
    """Update tool call count in flow-state.md."""
    content = state_file.read_text()

    # Find and increment tool_calls
    match = re.search(r'tool_calls:\s*(\d+)', content)

    if match:
        current_count = int(match.group(1))
        new_count = current_count + 1
        content = re.sub(r'tool_calls:\s*\d+', f'tool_calls: {new_count}', content)
    else:
        # Add tool_calls after current_phase if it exists
        if "current_phase:" in content:
            content = re.sub(
                r'(current_phase:\s*\w+)',
                f'\\1\ntool_calls: 1',
                content
            )
        new_count = 1

    # Update last_updated timestamp
    now = datetime.now().isoformat()
    if "last_updated:" in content:
        content = re.sub(r'last_updated:\s*[\w\-:.]+', f'last_updated: {now}', content)

    state_file.write_text(content)
    return new_count


def create_checkpoint(flow_dir: Path, tool_calls: int) -> None:
    """Create a checkpoint file."""
    checkpoints_dir = flow_dir / "checkpoints"
    checkpoints_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    checkpoint_file = checkpoints_dir / f"checkpoint-{tool_calls}-{timestamp}.md"

    # Read current state for checkpoint
    state_file = flow_dir / "flow-state.md"
    plan_file = flow_dir / "flow-plan.md"
    tasks_file = flow_dir / "flow-tasks.md"

    checkpoint_content = f"""---
checkpoint_at: {tool_calls} tool calls
timestamp: {datetime.now().isoformat()}
---

# Checkpoint at {tool_calls} Tool Calls

## State Snapshot
"""

    if state_file.exists():
        checkpoint_content += f"\n### flow-state.md\n```yaml\n{state_file.read_text()[:1000]}...\n```\n"

    if tasks_file.exists():
        # Extract just the checkbox progress
        tasks_content = tasks_file.read_text()
        # Count completed vs total
        completed = tasks_content.count("[x]")
        total = completed + tasks_content.count("[ ]")
        checkpoint_content += f"\n### Tasks Progress\n- Completed: {completed}/{total}\n"

    checkpoint_file.write_text(checkpoint_content)
    print_info(f"Checkpoint created at {tool_calls} tool calls")


def main():
    """Main checkpoint logic."""
    # Get active flow directory
    flow_dir = get_active_flow_dir()

    if not flow_dir:
        # No active flow, skip silently
        return

    state_file = flow_dir / "flow-state.md"

    if not state_file.exists():
        return

    # Update tool call count
    tool_calls = update_tool_call_count(state_file)

    # Create checkpoint every 20 tool calls
    if tool_calls > 0 and tool_calls % 20 == 0:
        create_checkpoint(flow_dir, tool_calls)

    # Warn at 50+ tool calls (approaching context limits)
    if tool_calls == 50:
        print_warning("50 tool calls reached. Consider checkpointing with 'pause' if task is complex.")
    elif tool_calls == 75:
        print_warning("75 tool calls. Context limit approaching. Auto-checkpoint recommended.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Silent failure - don't interrupt tool execution
        pass
