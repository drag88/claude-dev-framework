---
description: Generate CLAUDE.md file from project rules
---

Generate a concise `CLAUDE.generated.md` file by synthesizing `.claude/rules/` documentation.

## Prerequisites

`.claude/rules/` must exist with generated rules. If not, run `/regenerate-rules` first.

## Behavioral Flow

### 1. Verify Rules Exist

Check for `.claude/rules/` directory with at least one `.md` file:
- `architecture.md`
- `tech-stack.md`
- `patterns.md`
- `commands.md`

If missing, inform user: "No project rules found. Run `/regenerate-rules` first."

### 2. Read Rule Files

Read each available rule file and extract:
- **From architecture.md**: Project name, description, key directories, component relationships
- **From tech-stack.md**: Language, framework, key libraries
- **From commands.md**: Setup, test, lint, run commands
- **From patterns.md**: Critical coding patterns/rules

### 3. Generate CLAUDE.generated.md

Create file at project root using this template:

```markdown
# [Project Name]

## Overview
[1-2 sentence description extracted from architecture.md or inferred from codebase]

## Quick Start

```bash
[cd command if needed]
[install/setup command]
[test command]
[lint command]
[run command]
```

## Critical Rules

1. **Read before edit** - understand code before making changes
2. **DRY** - search with `rg` before writing similar code
3. **No backwards compat** - delete deprecated code immediately
4. **Tests required** - no feature is complete without tests

<plans_instruction>
## Plans Format

At end of plans, provide concise unresolved questions:
```
Unresolved Questions:
- [Question]?
```

Requirements:
- Make questions EXTREMELY concise
- Sacrifice grammar for concision
</plans_instruction>

## Commit Messages

Do NOT include Claude attribution in commits:
```
# BAD - Don't include this:
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Project Rules

Auto-generated rules in `.claude/rules/` - Claude loads these automatically.
Run `/regenerate-rules` to refresh after major changes.

## Key Directories

- `[dir1]/` - [brief purpose]
- `[dir2]/` - [brief purpose]
[etc. - max 5-7 key directories]
```

### 4. Guidelines for Generation

- **Keep it concise**: Target < 100 lines, never exceed 150
- **WHY/WHAT/HOW**: Purpose → Stack/Structure → Commands
- **Progressive disclosure**: Point to `.claude/rules/` for details
- **No code style**: Let linters handle formatting rules
- **Quick Start first**: Most used commands at the top
- **Key dirs only**: Don't list every subdirectory

### 5. Output Location

Always write to `CLAUDE.generated.md` (not `CLAUDE.md`) to preserve manual edits.

Inform user:
- File created at `CLAUDE.generated.md`
- Review and rename to `CLAUDE.md` if satisfied
- Or merge changes into existing `CLAUDE.md`

## Example Output

For a Python FastAPI project:

```markdown
# Uplyft Minerva Taxonomist

## Overview
Product taxonomy classifier using Cohere v4 embeddings + MongoDB Atlas vector search.

## Quick Start

```bash
cd smart_classifier
uv sync
uv run pytest
uv run ruff check . --fix
uv run python -m src.api.app
```

## Critical Rules

1. **Read before edit** - understand code before changes
2. **DRY** - search with `rg` before writing similar code
3. **No backwards compat** - delete deprecated code immediately
4. **Tests required** - no feature complete without tests

<plans_instruction>
## Plans Format

At end of plans, provide concise unresolved questions:
```
Unresolved Questions:
- [Question]?
```
</plans_instruction>

## Commit Messages

Do NOT include Claude attribution in commits.

## Project Rules

Auto-generated rules in `.claude/rules/` - Claude loads automatically.
Run `/regenerate-rules` to refresh after major changes.

## Key Directories

- `smart_classifier/src/` - Python ML classifier (FastAPI)
- `smart_classifier/tests/` - Test suite
- `data/` - Shopify taxonomy data
- `dev/` - Ruby ETL system
```
