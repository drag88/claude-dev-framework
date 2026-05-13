#!/usr/bin/env python3
"""
CDF Health Check Script

Validates plugin integrity:
1. hooks.json is valid JSON
2. All scripts referenced in hooks.json exist
3. All skills/*/SKILL.md have valid YAML frontmatter
4. Component counts in docs/marketplace metadata match the actual tree
5. Marketplace plugin version matches plugin.json
6. Deleted commands are not advertised as active commands
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
        "command": [
            r'(\d+)\s+(?:slash\s+)?commands?\b',
            r'Commands\s*\|\s*(\d+)\s*\|',
            r'`commands/`\s*-\s*(\d+)\s+slash command',
        ],
        "agent": [
            r'(\d+)\s+(?:real-expertise\s+)?agent(?:\s+persona)?s?\b',
            r'Agents\s*\|\s*(\d+)\s*\|',
            r'`agents/`\s*-\s*(\d+)\s+(?:real-expertise\s+)?agent',
        ],
        "skill": [
            r'(\d+)\s+(?:auto-invoked\s+)?skills?\b',
            r'Skills\s*\|\s*(\d+)\s*\|',
            r'`skills/`\s*-\s*(\d+)\s+auto-invoked skill',
        ],
        "hook": [
            r'(\d+)\s+(?:lifecycle\s+)?hooks?\b',
            r'Hooks\s*\|\s*(\d+)\s*\|',
        ],
        "template": [
            r'(\d+)\s+rule generation templates?\b',
            r'Rule Templates\s*\|\s*(\d+)\s*\|',
            r'`rules-templates/`\s*-\s*(\d+)\s+rule generation template',
        ],
    }

    for component, component_patterns in patterns.items():
        for pattern in component_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if not match:
                continue
            for group in match.groups():
                if group is not None:
                    counts[component] = int(group)
                    break
            break

    return counts


def get_actual_counts(project_root: Path) -> dict:
    """Count actual framework components in the repository."""
    hooks_count = 0
    hooks_file = project_root / "hooks" / "hooks.json"
    if hooks_file.exists():
        with open(hooks_file) as f:
            data = json.load(f)
        for hook_groups in data.get("hooks", {}).values():
            for group in hook_groups:
                hooks_count += len(group.get("hooks", []))

    return {
        "command": len([p for p in (project_root / "commands").glob("*.md") if p.name != "README.md"]),
        "agent": len([p for p in (project_root / "agents").glob("*.md") if p.name != "README.md"]),
        "skill": len(list((project_root / "skills").glob("*/SKILL.md"))),
        "hook": hooks_count,
        "template": len(list((project_root / "rules-templates").glob("*.md"))),
    }


def check_count_consistency(project_root: Path) -> list:
    issues = []
    actual_counts = get_actual_counts(project_root)

    files_to_check = {
        "CLAUDE.md": project_root / "CLAUDE.md",
        "CLAUDE.generated.md": project_root / "CLAUDE.generated.md",
        "README.md": project_root / "README.md",
        "marketplace.json": project_root / ".claude-plugin" / "marketplace.json",
        ".claude/rules/architecture.md": project_root / ".claude" / "rules" / "architecture.md",
        ".claude/rules/tech-stack.md": project_root / ".claude" / "rules" / "tech-stack.md",
    }

    for name, path in files_to_check.items():
        if not path.exists():
            continue
        content = path.read_text()
        counts = extract_counts(content)
        for component, documented in counts.items():
            actual = actual_counts[component]
            if documented != actual:
                issues.append(
                    f"Stale {component} count in {name}: documented={documented}, actual={actual}"
                )

    return issues


def check_marketplace_version(project_root: Path) -> list:
    issues = []
    plugin_file = project_root / ".claude-plugin" / "plugin.json"
    marketplace_file = project_root / ".claude-plugin" / "marketplace.json"

    if not plugin_file.exists() or not marketplace_file.exists():
        return issues

    with open(plugin_file) as f:
        plugin = json.load(f)
    with open(marketplace_file) as f:
        marketplace = json.load(f)

    plugin_version = plugin.get("version")
    marketplace_plugins = marketplace.get("plugins", [])
    if not marketplace_plugins:
        issues.append(".claude-plugin/marketplace.json has no plugins")
        return issues

    marketplace_version = marketplace_plugins[0].get("version")
    if plugin_version != marketplace_version:
        issues.append(
            f"Marketplace version mismatch: plugin.json={plugin_version}, marketplace.json={marketplace_version}"
        )

    return issues


def check_removed_command_refs(project_root: Path) -> list:
    """Fail when deleted commands are still shown as runnable examples or table rows."""
    issues = []
    bad_patterns = [
        re.compile(r'/cdf:workflow\s+"'),
        re.compile(r'/cdf:flow\s+"'),
        re.compile(r'\|\s*`/cdf:workflow`\s*\|'),
        re.compile(r'\|\s*`/cdf:flow`\s*\|'),
        re.compile(r'/cdf:retro\b'),
        re.compile(r'/cdf:product-review\b'),
        re.compile(r'All 22 Commands'),
    ]

    scan_paths = [
        project_root / "README.md",
        project_root / "CLAUDE.md",
        project_root / "CLAUDE.generated.md",
    ]
    for dirname in ["commands", "docs", ".claude/rules"]:
        root = project_root / dirname
        if root.exists():
            scan_paths.extend(root.rglob("*.md"))

    for path in scan_paths:
        if not path.exists():
            continue
        rel = path.relative_to(project_root)
        if rel.name == "CHANGELOG.md":
            continue

        for line_no, line in enumerate(path.read_text(errors="ignore").splitlines(), start=1):
            if any(pattern.search(line) for pattern in bad_patterns):
                issues.append(f"Removed command advertised in {rel}:{line_no}: {line.strip()}")

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

    # 4. Check marketplace version alignment
    all_issues.extend(check_marketplace_version(project_root))

    # 5. Check removed command references
    all_issues.extend(check_removed_command_refs(project_root))

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
