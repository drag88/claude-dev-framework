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


def check_component_counts(files, project_root):
    """Validate actual component counts match plugin.json and CLAUDE.md."""
    component_dirs = {
        'commands/': 'commands',
        'agents/': 'agents',
        'skills/': 'skills',
    }

    touches_components = any(
        any(f.startswith(d) for d in component_dirs)
        for f in files
    )

    if not touches_components:
        return None

    plugin_json_path = project_root / '.claude-plugin' / 'plugin.json'
    claude_md_path = project_root / 'CLAUDE.md'

    if not plugin_json_path.exists():
        return None

    # Count actual components
    commands_dir = project_root / 'commands'
    agents_dir = project_root / 'agents'
    skills_dir = project_root / 'skills'

    actual_commands = len([f for f in commands_dir.glob('*.md') if f.name != 'README.md']) if commands_dir.exists() else 0
    actual_agents = len([f for f in agents_dir.glob('*.md') if f.name != 'README.md']) if agents_dir.exists() else 0
    actual_skills = len(list(skills_dir.glob('*/SKILL.md'))) if skills_dir.exists() else 0

    # Count hooks from hooks.json
    hooks_json_path = project_root / 'hooks' / 'hooks.json'
    actual_hooks = 0
    if hooks_json_path.exists():
        try:
            with open(hooks_json_path) as f:
                hooks_data = json.load(f)
            for entries in hooks_data.get('hooks', {}).values():
                for entry in entries:
                    actual_hooks += len(entry.get('hooks', []))
        except (json.JSONDecodeError, Exception):
            pass

    # Check plugin.json description
    mismatches = []
    try:
        with open(plugin_json_path) as f:
            desc = json.load(f).get('description', '')
        if f'{actual_commands} commands' not in desc:
            mismatches.append(f'plugin.json command count (actual: {actual_commands})')
        if f'{actual_agents} agent' not in desc:
            mismatches.append(f'plugin.json agent count (actual: {actual_agents})')
        if f'{actual_skills} skills' not in desc:
            mismatches.append(f'plugin.json skill count (actual: {actual_skills})')
        if f'{actual_hooks} lifecycle' not in desc:
            mismatches.append(f'plugin.json hook count (actual: {actual_hooks})')
    except (json.JSONDecodeError, Exception):
        pass

    # Check CLAUDE.md counts
    if claude_md_path.exists():
        try:
            claude_md = claude_md_path.read_text()
            if f'{actual_commands} slash command' not in claude_md:
                mismatches.append(f'CLAUDE.md command count (actual: {actual_commands})')
            if f'{actual_skills} auto-invoked' not in claude_md:
                mismatches.append(f'CLAUDE.md skill count (actual: {actual_skills})')
        except Exception:
            pass

    if not mismatches:
        return None

    return "Component count mismatches found: " + "; ".join(mismatches) + ". Update plugin.json and CLAUDE.md before pushing."


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

    warnings = []
    for check in [check_changelog, check_version, check_docs, check_component_counts]:
        result = check(files, project_root)
        if result:
            warnings.append(result)

    if not warnings:
        return

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
