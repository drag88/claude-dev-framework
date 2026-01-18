#!/usr/bin/env python3
"""
Codebase Rules Guide for Claude Code

SessionStart hook that:
- If rules exist: Claude loads them automatically (just confirm they exist)
- If project has code but no rules: instructs Claude to analyze and generate
- If project is empty/new: asks user questions to set up project rules
"""

import json
import os
from pathlib import Path

# Instructions for analyzing existing codebase
GENERATION_INSTRUCTIONS = """No project rules found. Automatically generating...

## IMPORTANT: Generate project rules NOW

Before doing anything else, analyze this codebase and generate `.claude/rules/` documentation.

### Analysis Steps

1. **Explore project structure** using the Explore agent
   - Identify key directories and their purposes
   - Find main entry points and configuration files
   - Understand the project's domain

2. **Analyze tech stack**
   - Read pyproject.toml, package.json, Gemfile, etc.
   - Identify frameworks, libraries, and tools

3. **Understand code patterns**
   - Read key source files
   - Identify architectural patterns

4. **Extract commands**
   - Find how to run tests, lint, and start the app

### Generate these files in `.claude/rules/`:

**`architecture.md`** - Directory structure with descriptions, key files, component relationships, data flow
**`tech-stack.md`** - Languages, frameworks, libraries (with purpose), dev tools
**`patterns.md`** - Architectural patterns, service init, error handling, config, testing patterns
**`commands.md`** - Setup, test, lint, run commands

Use concise technical language. Base on actual code analysis, not README.

For path-specific rules, use YAML frontmatter:
```markdown
---
paths: src/api/**/*.py
---
# API Route Rules
...
```

After generating, confirm completion to user."""

# Instructions for empty/new projects
NEW_PROJECT_INSTRUCTIONS = """This appears to be a new or empty project with no code to analyze.

## Project Setup Required

Ask the user these questions to set up project rules:

1. **Project name**: What is this project called?
2. **Purpose**: What will this project do? (1-2 sentences)
3. **Tech stack**: What language/framework will you use? (e.g., Python + FastAPI, Node + Express, etc.)
4. **Project type**: What kind of project? (API, CLI, library, web app, etc.)

After getting answers, generate `.claude/rules/` with starter templates:

**`architecture.md`**:
```markdown
# Architecture

## Project Structure
To be defined as code is added.

## Key Components
- [Based on user's description]
```

**`tech-stack.md`**:
```markdown
# Tech Stack

## Language
- [From user input]

## Framework
- [From user input]
```

**`commands.md`**:
```markdown
# Commands

## Setup
`[appropriate for tech stack]`

## Test
`[appropriate for tech stack]`

## Run
`[appropriate for tech stack]`
```

**`patterns.md`**: Create minimal placeholder noting "To be updated when code is added."

Confirm setup complete and ready for development."""


# Files/dirs that indicate a project has code
CODE_INDICATORS = [
    # Config files
    "pyproject.toml", "package.json", "Cargo.toml", "go.mod", "Gemfile",
    "setup.py", "requirements.txt", "composer.json", "pom.xml", "build.gradle",
    # Source directories
    "src", "lib", "app", "main.py", "index.js", "index.ts", "main.go", "main.rs",
]


def get_project_dir() -> Path:
    """Get the project directory from environment or current directory."""
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))


def has_code(project_dir: Path) -> bool:
    """Check if project has any code or config files."""
    for indicator in CODE_INDICATORS:
        if (project_dir / indicator).exists():
            return True

    # Also check for any source files in immediate subdirs
    source_extensions = {".py", ".js", ".ts", ".go", ".rs", ".rb", ".java", ".kt", ".swift"}
    try:
        for item in project_dir.iterdir():
            if item.is_file() and item.suffix in source_extensions:
                return True
            if item.is_dir() and not item.name.startswith("."):
                for subitem in item.iterdir():
                    if subitem.is_file() and subitem.suffix in source_extensions:
                        return True
    except PermissionError:
        pass

    return False


def check_rules_exist(project_dir: Path) -> dict:
    """Check project state and return appropriate guidance."""
    rules_dir = project_dir / ".claude" / "rules"

    # Check if any .md files exist in rules directory
    has_rules = False
    rule_files = []
    if rules_dir.exists():
        for f in rules_dir.rglob("*.md"):
            has_rules = True
            rule_files.append(f.relative_to(rules_dir))

    if has_rules:
        # Rules exist - Claude loads them automatically
        files_list = "\n".join(f"- {f}" for f in sorted(rule_files)[:10])
        if len(rule_files) > 10:
            files_list += f"\n- ... and {len(rule_files) - 10} more"

        # Check if CLAUDE.md exists
        has_claude_md = (project_dir / "CLAUDE.md").exists()
        has_claude_generated = (project_dir / "CLAUDE.generated.md").exists()

        claude_md_note = ""
        if not has_claude_md and not has_claude_generated:
            claude_md_note = "\n\nNo CLAUDE.md found. Run /cdf:rules claudemd to create one from your rules."

        return {
            "additionalContext": f"""Project rules loaded from .claude/rules/:
{files_list}

These rules are automatically applied. Run /cdf:rules generate to refresh after major changes.{claude_md_note}"""
        }
    elif has_code(project_dir):
        # Has code but no rules - trigger automatic generation
        return {"additionalContext": GENERATION_INSTRUCTIONS}
    else:
        # Empty/new project - ask user questions
        return {"additionalContext": NEW_PROJECT_INSTRUCTIONS}


def main() -> None:
    """Main entry point."""
    project_dir = get_project_dir()
    result = check_rules_exist(project_dir)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
