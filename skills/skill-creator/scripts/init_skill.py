#!/usr/bin/env python3
"""
Initialize a new skill with the standard directory structure and template files.

Usage:
    python init_skill.py <skill-name> --path <output-directory>

Example:
    python init_skill.py pdf-editor --path ./skills
    # Creates: ./skills/pdf-editor/SKILL.md and example directories
"""

import argparse
import os
import sys
from pathlib import Path

SKILL_MD_TEMPLATE = '''---
name: {skill_name}
description: TODO - Describe what this skill does and when it should be used. Use third-person (e.g., "This skill should be used when...").
license: Complete terms in LICENSE.txt
---

# {skill_title}

TODO - Brief description of the skill's purpose (2-3 sentences).

## Overview

TODO - Explain what this skill provides and the problems it solves.

## When to Use This Skill

This skill should be used when:
- TODO - First trigger condition
- TODO - Second trigger condition
- TODO - Third trigger condition

## Workflow

TODO - Describe the step-by-step process for using this skill.

### Step 1: TODO

TODO - Describe the first step.

### Step 2: TODO

TODO - Describe the second step.

## Scripts

The following scripts are available in the `scripts/` directory:

- `example.py` - TODO - Describe what this script does

## References

The following reference materials are available in the `references/` directory:

- `example.md` - TODO - Describe this reference document

## Assets

The following assets are available in the `assets/` directory:

- `example.txt` - TODO - Describe this asset

## Dependencies

TODO - List any required dependencies (pip packages, npm packages, system tools, etc.)

## Examples

### Example 1: TODO

```
TODO - Show an example usage
```
'''

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example script for the {skill_name} skill.

TODO - Replace this with actual functionality.

Usage:
    python example.py <input> [options]
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Example script")
    parser.add_argument("input", help="Input file or value")
    parser.add_argument("--output", "-o", help="Output file (optional)")
    args = parser.parse_args()

    # TODO - Implement actual functionality
    print(f"Processing: {{args.input}}")
    if args.output:
        print(f"Output: {{args.output}}")


if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = '''# Example Reference Document

TODO - Replace this with actual reference content.

## Overview

This document provides reference information for the {skill_name} skill.

## Key Concepts

- **Concept 1**: TODO - Explain this concept
- **Concept 2**: TODO - Explain this concept

## API Reference

TODO - Add API documentation if applicable.

## Schema Reference

TODO - Add schema documentation if applicable.

## Best Practices

- TODO - First best practice
- TODO - Second best practice
'''

EXAMPLE_ASSET = '''# Example Asset

TODO - Replace this file with actual assets (templates, images, etc.)

This is a placeholder asset file for the {skill_name} skill.
'''

LICENSE_TEMPLATE = '''MIT License

Copyright (c) {year} [Author Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


def validate_skill_name(name: str) -> bool:
    """Validate skill name follows conventions (lowercase, hyphenated)."""
    if not name:
        return False
    if not name[0].isalpha():
        return False
    for char in name:
        if not (char.isalnum() or char == '-'):
            return False
    if name != name.lower():
        return False
    return True


def skill_name_to_title(name: str) -> str:
    """Convert skill-name to Skill Name title format."""
    return ' '.join(word.capitalize() for word in name.split('-'))


def create_skill(skill_name: str, output_path: Path) -> None:
    """Create the skill directory structure with template files."""
    skill_dir = output_path / skill_name

    if skill_dir.exists():
        print(f"Error: Directory already exists: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    # Create directories
    directories = [
        skill_dir,
        skill_dir / "scripts",
        skill_dir / "references",
        skill_dir / "assets",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created: {directory}")

    # Get current year for license
    from datetime import datetime
    current_year = datetime.now().year

    # Create files
    skill_title = skill_name_to_title(skill_name)

    files = {
        skill_dir / "SKILL.md": SKILL_MD_TEMPLATE.format(
            skill_name=skill_name,
            skill_title=skill_title
        ),
        skill_dir / "LICENSE.txt": LICENSE_TEMPLATE.format(year=current_year),
        skill_dir / "scripts" / "example.py": EXAMPLE_SCRIPT.format(
            skill_name=skill_name
        ),
        skill_dir / "references" / "example.md": EXAMPLE_REFERENCE.format(
            skill_name=skill_name
        ),
        skill_dir / "assets" / "example.txt": EXAMPLE_ASSET.format(
            skill_name=skill_name
        ),
    }

    for file_path, content in files.items():
        file_path.write_text(content)
        print(f"Created: {file_path}")

    # Make the example script executable
    script_path = skill_dir / "scripts" / "example.py"
    script_path.chmod(script_path.stat().st_mode | 0o111)

    print(f"\nSkill '{skill_name}' initialized successfully!")
    print(f"\nNext steps:")
    print(f"  1. Edit {skill_dir / 'SKILL.md'} to define your skill")
    print(f"  2. Add scripts to {skill_dir / 'scripts/'}")
    print(f"  3. Add references to {skill_dir / 'references/'}")
    print(f"  4. Add assets to {skill_dir / 'assets/'}")
    print(f"  5. Delete any example files you don't need")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new skill with standard directory structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s pdf-editor --path ./skills
  %(prog)s my-skill --path /path/to/output

The script creates:
  <output-path>/<skill-name>/
  ├── SKILL.md              (skill definition template)
  ├── LICENSE.txt           (MIT license template)
  ├── scripts/
  │   └── example.py        (example script)
  ├── references/
  │   └── example.md        (example reference doc)
  └── assets/
      └── example.txt       (example asset)
"""
    )
    parser.add_argument(
        "skill_name",
        help="Name of the skill (lowercase, hyphenated, e.g., 'pdf-editor')"
    )
    parser.add_argument(
        "--path",
        required=True,
        type=Path,
        help="Output directory where the skill folder will be created"
    )

    args = parser.parse_args()

    # Validate skill name
    if not validate_skill_name(args.skill_name):
        print(
            f"Error: Invalid skill name '{args.skill_name}'. "
            "Must be lowercase, start with a letter, and contain only "
            "letters, numbers, and hyphens.",
            file=sys.stderr
        )
        sys.exit(1)

    # Validate output path
    if not args.path.exists():
        print(f"Error: Output path does not exist: {args.path}", file=sys.stderr)
        sys.exit(1)

    if not args.path.is_dir():
        print(f"Error: Output path is not a directory: {args.path}", file=sys.stderr)
        sys.exit(1)

    create_skill(args.skill_name, args.path)


if __name__ == "__main__":
    main()
