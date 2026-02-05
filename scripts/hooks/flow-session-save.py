#!/usr/bin/env python3
"""
Flow Session Save Hook - Persist flow state on session end.

Triggers on Stop event. Saves complete flow state and creates
resume instructions for next session.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for utils import
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.utils import get_project_root, print_info, print_warning


def get_all_active_flows() -> list[Path]:
    """Find all active flow directories."""
    project_root = get_project_root()
    dev_active = project_root / "dev" / "active"

    if not dev_active.exists():
        return []

    flows = []
    for task_dir in dev_active.iterdir():
        if task_dir.is_dir():
            state_file = task_dir / "flow-state.md"
            if state_file.exists():
                content = state_file.read_text()
                # Check if flow has incomplete phases
                if "status: pending" in content or "status: in_progress" in content:
                    flows.append(task_dir)

    return flows


def get_incomplete_tasks(flow_dir: Path) -> list[str]:
    """Extract incomplete tasks from flow-tasks.md."""
    tasks_file = flow_dir / "flow-tasks.md"

    if not tasks_file.exists():
        return []

    content = tasks_file.read_text()
    incomplete = []

    for line in content.split("\n"):
        if "[ ]" in line:
            # Extract task text
            task = line.replace("- [ ]", "").strip()
            if task:
                incomplete.append(task)

    return incomplete[:5]  # Limit to top 5


def get_current_phase(flow_dir: Path) -> str:
    """Get current phase from flow state."""
    state_file = flow_dir / "flow-state.md"

    if not state_file.exists():
        return "unknown"

    content = state_file.read_text()

    import re
    match = re.search(r'current_phase:\s*(\w+)', content)
    if match:
        return match.group(1)

    return "unknown"


def update_flow_state_on_stop(flow_dir: Path) -> None:
    """Update flow state with session end info."""
    state_file = flow_dir / "flow-state.md"

    if not state_file.exists():
        return

    content = state_file.read_text()
    now = datetime.now().isoformat()

    import re

    # Update last_updated
    content = re.sub(r'last_updated:\s*[\w\-:.]+', f'last_updated: {now}', content)

    # Add session_ended if not present
    if "session_ended:" not in content:
        # Add after last_updated
        content = re.sub(
            r'(last_updated:\s*[\w\-:.]+)',
            f'\\1\nsession_ended: {now}',
            content
        )
    else:
        content = re.sub(r'session_ended:\s*[\w\-:.]+', f'session_ended: {now}', content)

    state_file.write_text(content)


def create_resume_instructions(flow_dir: Path) -> None:
    """Create/update resume instructions in flow state."""
    state_file = flow_dir / "flow-state.md"

    if not state_file.exists():
        return

    content = state_file.read_text()
    current_phase = get_current_phase(flow_dir)
    incomplete_tasks = get_incomplete_tasks(flow_dir)

    # Build resume section
    resume_section = f"""
## Quick Resume

To continue this flow, run:
```bash
/cdf:flow --resume
```

**Current State:**
- Phase: {current_phase}
- Incomplete Tasks: {len(incomplete_tasks)}

**Next Steps:**
"""

    if incomplete_tasks:
        for task in incomplete_tasks:
            resume_section += f"1. {task}\n"
    else:
        resume_section += "1. Check flow-tasks.md for remaining work\n"

    # Update or append resume section
    if "## Quick Resume" in content:
        import re
        content = re.sub(
            r'## Quick Resume.*?(?=\n## |\Z)',
            resume_section,
            content,
            flags=re.DOTALL
        )
    else:
        content += "\n" + resume_section

    state_file.write_text(content)


def main():
    """Main session save logic."""
    flows = get_all_active_flows()

    if not flows:
        return

    for flow_dir in flows:
        task_name = flow_dir.name
        current_phase = get_current_phase(flow_dir)

        # Update flow state
        update_flow_state_on_stop(flow_dir)

        # Create resume instructions
        create_resume_instructions(flow_dir)

        print_info(f"Flow '{task_name}' saved (phase: {current_phase})")
        print_info(f"Resume with: /cdf:flow --resume")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Silent failure - don't block session end
        pass
