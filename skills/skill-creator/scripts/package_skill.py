#!/usr/bin/env python3
"""
Validate and package a skill into a distributable zip file.

Usage:
    python package_skill.py <path/to/skill-folder> [output-directory]

Example:
    python package_skill.py ./skills/pdf-editor
    python package_skill.py ./skills/pdf-editor ./dist
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path
from typing import Optional


class ValidationError:
    def __init__(self, message: str, severity: str = "error"):
        self.message = message
        self.severity = severity  # "error" or "warning"

    def __str__(self):
        prefix = "ERROR" if self.severity == "error" else "WARNING"
        return f"{prefix}: {self.message}"


def parse_yaml_frontmatter(content: str) -> tuple[Optional[dict], Optional[str]]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return None, "SKILL.md must start with YAML frontmatter (---)"

    lines = content.split('\n')
    end_index = None
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            end_index = i
            break

    if end_index is None:
        return None, "YAML frontmatter not properly closed (missing closing ---)"

    frontmatter_lines = lines[1:end_index]
    frontmatter = {}

    for line in frontmatter_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            frontmatter[key] = value

    return frontmatter, None


def validate_skill_name(name: str) -> list[ValidationError]:
    """Validate skill name follows conventions."""
    errors = []

    if not name:
        errors.append(ValidationError("Skill name is empty"))
        return errors

    if not name[0].isalpha():
        errors.append(ValidationError(
            f"Skill name '{name}' must start with a letter"
        ))

    if name != name.lower():
        errors.append(ValidationError(
            f"Skill name '{name}' must be lowercase"
        ))

    invalid_chars = [c for c in name if not (c.isalnum() or c == '-')]
    if invalid_chars:
        errors.append(ValidationError(
            f"Skill name '{name}' contains invalid characters: {invalid_chars}. "
            "Only lowercase letters, numbers, and hyphens are allowed."
        ))

    return errors


def validate_description(description: str) -> list[ValidationError]:
    """Validate skill description quality."""
    errors = []

    if not description:
        errors.append(ValidationError("Description is missing"))
        return errors

    if description.startswith("TODO"):
        errors.append(ValidationError(
            "Description contains TODO placeholder - please provide actual description"
        ))

    if len(description) < 20:
        errors.append(ValidationError(
            f"Description is too short ({len(description)} chars). "
            "Please provide a more detailed description (at least 20 characters)."
        ))

    # Check for third-person usage
    if description.lower().startswith("use this") or description.lower().startswith("you "):
        errors.append(ValidationError(
            "Description should use third-person (e.g., 'This skill should be used when...' "
            "instead of 'Use this skill when...')",
            severity="warning"
        ))

    return errors


def validate_skill_md_content(content: str) -> list[ValidationError]:
    """Validate SKILL.md body content."""
    errors = []

    # Check for TODO placeholders in the body
    todo_count = content.count("TODO")
    if todo_count > 0:
        errors.append(ValidationError(
            f"SKILL.md contains {todo_count} TODO placeholder(s) that need to be replaced",
            severity="warning"
        ))

    # Check minimum content length (excluding frontmatter)
    lines = content.split('\n')
    body_start = 0
    in_frontmatter = False
    for i, line in enumerate(lines):
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
            else:
                body_start = i + 1
                break

    body = '\n'.join(lines[body_start:])
    if len(body.strip()) < 100:
        errors.append(ValidationError(
            "SKILL.md body is too short. Please provide more detailed instructions.",
            severity="warning"
        ))

    return errors


def validate_directory_structure(skill_path: Path) -> list[ValidationError]:
    """Validate skill directory structure."""
    errors = []

    # Get actual filenames in directory (case-sensitive)
    actual_files = {f.name for f in skill_path.iterdir() if f.is_file()}

    # Check SKILL.md exists (exact case)
    if "SKILL.md" not in actual_files:
        errors.append(ValidationError(
            f"Required file SKILL.md not found in {skill_path}"
        ))

    # Check for common misspellings (case-sensitive check)
    wrong_names = ["skill.md", "Skill.md", "SKILLS.md"]
    for wrong in wrong_names:
        if wrong in actual_files:
            errors.append(ValidationError(
                f"Found '{wrong}' but the file must be named 'SKILL.md' (exact case)",
                severity="warning"
            ))

    return errors


def validate_skill(skill_path: Path) -> tuple[list[ValidationError], dict]:
    """Validate a skill and return errors and metadata."""
    errors = []
    metadata = {}

    # Check directory structure
    errors.extend(validate_directory_structure(skill_path))

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return errors, metadata

    # Read and parse SKILL.md
    content = skill_md.read_text()

    # Parse frontmatter
    frontmatter, parse_error = parse_yaml_frontmatter(content)
    if parse_error:
        errors.append(ValidationError(parse_error))
        return errors, metadata

    if frontmatter is None:
        errors.append(ValidationError("Failed to parse YAML frontmatter"))
        return errors, metadata

    # Validate required fields
    if 'name' not in frontmatter:
        errors.append(ValidationError("Missing required field 'name' in frontmatter"))
    else:
        metadata['name'] = frontmatter['name']
        errors.extend(validate_skill_name(frontmatter['name']))

        # Check name matches directory name
        if frontmatter['name'] != skill_path.name:
            errors.append(ValidationError(
                f"Skill name '{frontmatter['name']}' in frontmatter doesn't match "
                f"directory name '{skill_path.name}'"
            ))

    if 'description' not in frontmatter:
        errors.append(ValidationError("Missing required field 'description' in frontmatter"))
    else:
        metadata['description'] = frontmatter['description']
        errors.extend(validate_description(frontmatter['description']))

    # Validate SKILL.md content
    errors.extend(validate_skill_md_content(content))

    return errors, metadata


def package_skill(skill_path: Path, output_dir: Path) -> Path:
    """Package a skill into a zip file."""
    skill_name = skill_path.name
    zip_path = output_dir / f"{skill_name}.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in skill_path.rglob('*'):
            if file_path.is_file():
                # Skip common unwanted files
                if file_path.name.startswith('.'):
                    continue
                if file_path.name.endswith('.pyc'):
                    continue
                if '__pycache__' in str(file_path):
                    continue

                arcname = file_path.relative_to(skill_path.parent)
                zipf.write(file_path, arcname)

    return zip_path


def main():
    parser = argparse.ArgumentParser(
        description="Validate and package a skill into a distributable zip file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ./skills/pdf-editor
  %(prog)s ./skills/pdf-editor ./dist

The script will:
  1. Validate the skill (YAML frontmatter, naming, structure)
  2. Report any errors or warnings
  3. If validation passes, create a zip file for distribution
"""
    )
    parser.add_argument(
        "skill_path",
        type=Path,
        help="Path to the skill directory"
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        nargs='?',
        default=None,
        help="Output directory for the zip file (default: same as skill directory)"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate, don't create zip file"
    )

    args = parser.parse_args()

    # Resolve paths
    skill_path = args.skill_path.resolve()
    output_dir = args.output_dir.resolve() if args.output_dir else skill_path.parent

    # Validate paths
    if not skill_path.exists():
        print(f"Error: Skill path does not exist: {skill_path}", file=sys.stderr)
        sys.exit(1)

    if not skill_path.is_dir():
        print(f"Error: Skill path is not a directory: {skill_path}", file=sys.stderr)
        sys.exit(1)

    if not output_dir.exists():
        print(f"Error: Output directory does not exist: {output_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Validating skill: {skill_path.name}")
    print("-" * 50)

    # Validate
    errors, metadata = validate_skill(skill_path)

    # Report results
    warnings = [e for e in errors if e.severity == "warning"]
    hard_errors = [e for e in errors if e.severity == "error"]

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning.message}")

    if hard_errors:
        print("\nErrors:")
        for error in hard_errors:
            print(f"  - {error.message}")
        print(f"\nValidation FAILED with {len(hard_errors)} error(s)")
        sys.exit(1)

    if warnings:
        print(f"\nValidation passed with {len(warnings)} warning(s)")
    else:
        print("\nValidation passed!")

    # Package if not validate-only
    if args.validate_only:
        return

    print("-" * 50)
    print("Packaging skill...")

    zip_path = package_skill(skill_path, output_dir)
    print(f"\nPackage created: {zip_path}")
    print(f"Size: {zip_path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
