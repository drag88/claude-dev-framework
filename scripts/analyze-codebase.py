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
from typing import Dict, List, Set

# Project type detection signatures
PROJECT_TYPE_SIGNATURES: Dict[str, Dict[str, list]] = {
    "ml": {
        "files": ["*.ipynb", "mlflow", "wandb"],
        "deps": ["torch", "tensorflow", "sklearn", "scikit-learn", "mlflow", "wandb", "transformers", "keras"],
        "configs": ["mlflow", "dvc.yaml", "dvc.lock"],
    },
    "frontend": {
        "files": ["next.config.*", "vite.config.*", "webpack.config.*", "tsconfig.json"],
        "deps": ["react", "vue", "angular", "svelte", "next", "nuxt"],
        "dirs": ["components", "pages", "app"],
    },
    "backend": {
        "files": ["manage.py", "alembic.ini"],
        "deps": ["fastapi", "flask", "django", "express", "nestjs", "spring"],
        "dirs": ["migrations", "api", "routes"],
    },
    "mobile": {
        "files": ["pubspec.yaml", "Podfile", "build.gradle"],
        "dirs": ["ios", "android", "lib"],
        "deps": ["react-native", "expo", "flutter"],
    },
    "data-eng": {
        "files": ["dbt_project.yml", "profiles.yml"],
        "deps": ["airflow", "dagster", "prefect", "dbt-core", "great-expectations"],
        "dirs": ["models", "macros", "seeds"],
    },
    "cli-library": {
        "deps": ["click", "typer", "argparse", "commander", "yargs"],
        "indicators": ["entry_points", "console_scripts", "bin"],
    },
    "monorepo": {
        "files": ["pnpm-workspace.yaml", "lerna.json", "nx.json", "turbo.json"],
        "dirs": ["packages", "apps"],
    },
    "infra": {
        "files": ["*.tf", "Dockerfile", "docker-compose.yml", "Jenkinsfile", ".github/workflows"],
        "dirs": ["terraform", "k8s", "helm", "ansible"],
    },
}

# Project-type-specific generation instructions
PROJECT_TYPE_INSTRUCTIONS: Dict[str, str] = {
    "ml": """
#### ML/AI Project
- Generate `.claude/rules/experiment-tracking.md` - experiment config patterns, MLflow/W&B conventions, model versioning
- Generate `.claude/rules/data-contracts.md` - input/output schemas, feature definitions, data validation rules
- `architecture.md` must include **Data Flow** section: raw → features → training → serving
- `patterns.md` must include experiment config patterns, notebook conventions, reproducibility requirements""",

    "frontend": """
#### Frontend Project
- Generate `.claude/rules/component-conventions.md` - component structure, props patterns, composition rules
- Generate `.claude/rules/accessibility.md` - a11y requirements, ARIA patterns, keyboard navigation
- `architecture.md` must include **Component Hierarchy** and **Route Structure** sections
- `patterns.md` must include component patterns, state management, styling conventions""",

    "backend": """
#### Backend Project
- Generate `.claude/rules/api-conventions.md` - endpoint naming, request/response schemas, auth patterns
- Generate `.claude/rules/database-rules.md` - migration discipline, query patterns, indexing conventions
- `architecture.md` must include **Request Lifecycle** and **Database Schema Reference** sections
- `patterns.md` must include migration discipline, API versioning, error response format""",

    "data-eng": """
#### Data Engineering Project
- Generate `.claude/rules/pipeline-conventions.md` - DAG patterns, scheduling, idempotency rules
- Generate `.claude/rules/data-quality.md` - testing expectations, freshness checks, schema enforcement
- `architecture.md` must include **Pipeline DAG** and **Data Lineage** sections
- `patterns.md` must include SQL style, CTE patterns, incremental model conventions""",

    "mobile": """
#### Mobile Project
- Generate `.claude/rules/platform-rules.md` - platform-specific patterns, native bridge conventions
- Generate `.claude/rules/navigation.md` - screen flow, deep linking, navigation state management
- `architecture.md` must include **Screen Flow** and **Native Bridge Architecture** sections""",

    "cli-library": """
#### CLI / Library Project
- Generate `.claude/rules/public-api.md` - public API surface, breaking change policy, deprecation process
- Generate `.claude/rules/versioning.md` - semver rules, changelog conventions, release process
- `architecture.md` must include **Public API Surface Map** section""",

    "monorepo": """
#### Monorepo Project
- Generate `.claude/rules/workspace-map.md` - package boundaries, shared dependencies, build order
- Generate `.claude/rules/change-impact.md` - cross-package change rules, CI/CD implications
- `architecture.md` must include **Package Dependency Graph** section""",

    "infra": """
#### Infrastructure Project
- Generate `.claude/rules/iac-conventions.md` - module structure, naming, state management
- Generate `.claude/rules/security-baseline.md` - least-privilege patterns, secret management, network rules
- `architecture.md` must include **Infrastructure Topology** and **Terraform Module Tree** sections""",
}


def _build_generation_instructions(detected_types: List[str]) -> str:
    """Build generation instructions with project-type-specific sections."""
    types_str = ", ".join(detected_types) if detected_types else "general"

    type_sections = ""
    if detected_types:
        type_sections = "\n\n### Project-Type-Specific Rules\n"
        type_sections += f"\nDetected project type(s): **{types_str}**\n"
        for t in detected_types:
            if t in PROJECT_TYPE_INSTRUCTIONS:
                type_sections += PROJECT_TYPE_INSTRUCTIONS[t]

    return f"""No project rules found. Automatically generating...

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

**`architecture.md`** (matklad-inspired):
- **Bird's Eye View**: 1-2 sentences on what problem this solves
- **Codemap**: Coarse-grained modules, what each does, relationships between them
- **Cross-Cutting Concerns**: Logging, error handling, auth patterns
- **Architectural Invariants**: Constraints that must NOT be violated
- [Project-type-specific sections based on detected type]

**`tech-stack.md`** - Languages, frameworks, libraries (with purpose), dev tools
**`patterns.md`** - Architectural patterns, service init, error handling, config, testing patterns
**`commands.md`** - Setup, test, lint, run commands

**`soul.md`** - MUST generate `.claude/rules/soul.md` capturing the project's personality:
- **Identity**: What this project IS (from README/package.json)
- **Values**: Speed vs correctness, simplicity vs features (from code patterns)
- **Naming Conventions**: Variable/file/DB naming patterns detected from code
- **Boundaries**: Sacred files (migrations, lock files, generated code), never-commit patterns

**Root `AGENTS.md`** - MUST generate `AGENTS.md` at project root (not in .claude/) for cross-tool AI agent compatibility:
- **Project Overview**: 1-2 sentence elevator pitch
- **Development Setup**: Key commands
- **Architecture**: Condensed codemap
- **Coding Standards**: Key patterns
- **Agent Guidelines**: Sacred files, required commands after changes
{type_sections}

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


def _read_project_deps(project_dir: Path) -> Set[str]:
    """Read dependency names from common config files."""
    deps: Set[str] = set()

    # package.json
    pkg_json = project_dir / "package.json"
    if pkg_json.exists():
        try:
            data = json.loads(pkg_json.read_text())
            for key in ("dependencies", "devDependencies"):
                if key in data and isinstance(data[key], dict):
                    deps.update(data[key].keys())
        except (json.JSONDecodeError, OSError):
            pass

    # requirements.txt
    req_txt = project_dir / "requirements.txt"
    if req_txt.exists():
        try:
            for line in req_txt.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith(("#", "-")):
                    # Extract package name before version specifier
                    name = line.split("==")[0].split(">=")[0].split("<=")[0].split("[")[0].strip()
                    if name:
                        deps.add(name.lower())
        except OSError:
            pass

    # pyproject.toml - simple parsing without toml library
    pyproject = project_dir / "pyproject.toml"
    if pyproject.exists():
        try:
            content = pyproject.read_text()
            # Look for dependency strings in common sections
            in_deps = False
            for line in content.splitlines():
                stripped = line.strip()
                if stripped.startswith("[") and "dependencies" in stripped.lower():
                    in_deps = True
                    continue
                elif stripped.startswith("["):
                    in_deps = False
                    continue
                if in_deps and stripped.startswith('"'):
                    name = stripped.strip('"').strip("'").split(">=")[0].split("==")[0].split("[")[0].strip()
                    if name:
                        deps.add(name.lower())
        except OSError:
            pass

    return deps


def detect_project_types(project_dir: Path) -> List[str]:
    """Detect project types based on file signatures, directories, and dependencies."""
    detected: List[str] = []
    deps = _read_project_deps(project_dir)

    for proj_type, signatures in PROJECT_TYPE_SIGNATURES.items():
        matched = False

        # Check files (supports glob patterns)
        for pattern in signatures.get("files", []):
            if "*" in pattern:
                if list(project_dir.glob(pattern)):
                    matched = True
                    break
            elif (project_dir / pattern).exists():
                matched = True
                break

        # Check directories
        if not matched:
            for d in signatures.get("dirs", []):
                if (project_dir / d).is_dir():
                    matched = True
                    break

        # Check config files
        if not matched:
            for cfg in signatures.get("configs", []):
                if (project_dir / cfg).exists():
                    matched = True
                    break

        # Check dependencies
        if not matched:
            for dep in signatures.get("deps", []):
                if dep.lower() in deps:
                    matched = True
                    break

        # Check indicators (search in pyproject.toml/package.json content)
        if not matched:
            for indicator in signatures.get("indicators", []):
                for cfg_file in ["pyproject.toml", "package.json"]:
                    cfg_path = project_dir / cfg_file
                    if cfg_path.exists():
                        try:
                            if indicator in cfg_path.read_text():
                                matched = True
                                break
                        except OSError:
                            pass
                if matched:
                    break

        if matched:
            detected.append(proj_type)

    return detected


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

    detected_types = detect_project_types(project_dir)
    types_note = ""
    if detected_types:
        types_note = f"\nDetected project type(s): {', '.join(detected_types)}"

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

        # Check for missing recommended files
        missing = []
        if not (rules_dir / "soul.md").exists():
            missing.append(".claude/rules/soul.md")
        if not (project_dir / "AGENTS.md").exists():
            missing.append("AGENTS.md (project root)")

        missing_note = ""
        if missing:
            missing_note = f"\n\nRecommended files missing: {', '.join(missing)}. Run /cdf:rules generate to create them."

        return {
            "additionalContext": f"""Project rules loaded from .claude/rules/:
{files_list}
{types_note}
These rules are automatically applied. Run /cdf:rules generate to refresh after major changes.{claude_md_note}{missing_note}"""
        }
    elif has_code(project_dir):
        # Has code but no rules - trigger automatic generation
        return {"additionalContext": _build_generation_instructions(detected_types)}
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
