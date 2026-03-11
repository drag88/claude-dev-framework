#!/usr/bin/env python3
"""
CDF Health Check Script

Validates plugin integrity:
1. hooks.json is valid JSON
2. All scripts referenced in hooks.json exist
3. All skills/*/SKILL.md have valid YAML frontmatter
4. Component counts are consistent across CLAUDE.md, README.md, plugin.json, marketplace.json
"""

import json
import re
import sys
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def check_hooks_json(project_root: Path) -> list:
    issues = []
    hooks_file = project_root / "hooks" / "hooks.json"

    if not hooks_file.exists():
        issues.append("hooks/hooks.json does not exist")
        return issues

    try:
        with open(hooks_file) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        issues.append(f"hooks/hooks.json is invalid JSON: {e}")
        return issues

    if "hooks" not in data:
        issues.append("hooks/hooks.json missing top-level 'hooks' key")
        return issues

    # Check that all referenced scripts exist
    script_pattern = re.compile(r'\$CLAUDE_PLUGIN_ROOT/([^\s"]+)')
    for event, hook_groups in data["hooks"].items():
        for group in hook_groups:
            for hook in group.get("hooks", []):
                command = hook.get("command", "")
                matches = script_pattern.findall(command)
                for script_path in matches:
                    full_path = project_root / script_path
                    if not full_path.exists():
                        issues.append(f"Missing script: {script_path} (referenced in {event} hook)")

    return issues


def check_skills(project_root: Path) -> list:
    issues = []
    skills_dir = project_root / "skills"

    if not skills_dir.exists():
        issues.append("skills/ directory does not exist")
        return issues

    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            issues.append(f"skills/{skill_dir.name}/ missing SKILL.md")
            continue

        content = skill_file.read_text()
        if not content.startswith("---"):
            issues.append(f"skills/{skill_dir.name}/SKILL.md missing YAML frontmatter (does not start with ---)")

    return issues


def extract_counts(text: str) -> dict:
    """Extract component counts from text using common patterns."""
    counts = {}

    # Specific patterns to avoid matching prose like "spawn 3-5 agents"
    patterns = {
        "command": r'(\d+)\s+(?:slash\s+)?commands?\b',
        "agent": r'(\d+)\s+agent\s+personas?\b',
        "skill": r'(\d+)\s+(?:auto-invoked\s+)?skills?\b',
        "hook": r'(\d+)\s+(?:lifecycle\s+)?hooks?\b',
    }

    for component, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            counts[component] = int(match.group(1))

    return counts


def check_count_consistency(project_root: Path) -> list:
    issues = []
    all_counts = {}

    files_to_check = {
        "CLAUDE.md": project_root / "CLAUDE.md",
        "README.md": project_root / "README.md",
        "plugin.json": project_root / ".claude-plugin" / "plugin.json",
        "marketplace.json": project_root / ".claude-plugin" / "marketplace.json",
    }

    for name, path in files_to_check.items():
        if not path.exists():
            continue
        content = path.read_text()
        counts = extract_counts(content)
        if counts:
            all_counts[name] = counts

    if len(all_counts) < 2:
        return issues  # Not enough files to compare

    # Compare counts across files
    components = set()
    for counts in all_counts.values():
        components.update(counts.keys())

    for component in sorted(components):
        values = {}
        for fname, counts in all_counts.items():
            if component in counts:
                values[fname] = counts[component]

        unique_values = set(values.values())
        if len(unique_values) > 1:
            detail = ", ".join(f"{f}={v}" for f, v in sorted(values.items()))
            issues.append(f"Inconsistent {component} count: {detail}")

    return issues


def main():
    project_root = get_project_root()
    all_issues = []

    # 1. Validate hooks.json
    all_issues.extend(check_hooks_json(project_root))

    # 2. Check skills
    all_issues.extend(check_skills(project_root))

    # 3. Check count consistency
    all_issues.extend(check_count_consistency(project_root))

    if all_issues:
        print(f"Health check FAILED - {len(all_issues)} issue(s):\n")
        for issue in all_issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("Health check PASSED - all checks OK")
        sys.exit(0)


if __name__ == "__main__":
    main()
