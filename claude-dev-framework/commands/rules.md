---
description: "Project rules management: generate .claude/rules/ and CLAUDE.md documentation"
---

# /cdf:rules - Project Rules Management

> Generate and manage project rules in `.claude/rules/` and `CLAUDE.md`.

## Quick Start

```bash
# Generate full rules from codebase analysis
/cdf:rules generate

# Generate CLAUDE.md from existing rules
/cdf:rules claudemd

# Check if rules need refresh
/cdf:rules status
```

## When to Use

Use `/cdf:rules` when:
- Setting up a new project (generate initial rules)
- After major refactors (refresh rules to match new architecture)
- Rules are outdated (regenerate to match current code)
- Need `CLAUDE.md` for quick reference (generate from rules)

**Don't use this command for**: Dev documentation or task planning (use `/cdf:docs plan` instead).

## Subcommands

### generate - Analyze Codebase and Generate Rules

Analyze the codebase and generate comprehensive `.claude/rules/` documentation.

```bash
/cdf:rules generate [--force]
```

**Behavioral Flow:**
1. **Explore**: Analyze project structure using Explore agent
   - Identify key directories and their purposes
   - Find main entry points and configuration files
   - Understand the project's domain

2. **Analyze Tech Stack**
   - Read pyproject.toml, package.json, Gemfile, Cargo.toml, go.mod, etc.
   - Identify frameworks, libraries, and tools
   - Note testing and linting setup

3. **Understand Patterns**
   - Read key source files (main.py, app.py, index.ts, etc.)
   - Identify architectural patterns
   - Note naming conventions and code style

4. **Extract Commands**
   - Find how to run tests, lint, and start the app
   - Document environment setup requirements

5. **Generate Files** in `.claude/rules/`:

**Output Files:**

#### `architecture.md`
```markdown
# Architecture

## Directory Structure
- `src/` - [description]
- `tests/` - [description]

## Key Files
| File | Role |
|------|------|
| `app.py` | [role] |

## Component Relationships
[How different parts interact]

## Data Flow
[How data flows through the system]
```

#### `tech-stack.md`
```markdown
# Tech Stack

## Language
- [Language] [version]

## Framework
- [Framework] - [what it's used for]

## Key Libraries
| Library | Purpose |
|---------|---------|
| [lib] | [purpose] |

## Development Tools
- Testing: [tool]
- Linting: [tool]
```

#### `patterns.md`
```markdown
# Code Patterns

## Architectural Patterns
- [Pattern] - [where/how used]

## Service Initialization
[Code example]

## Error Handling
[Exception hierarchy, patterns]

## Configuration
[How config is managed]

## Testing Patterns
[Test organization, fixtures]
```

#### `commands.md`
```markdown
# Commands

## Setup
```bash
[setup commands]
```

## Test
```bash
[test commands]
```

## Lint
```bash
[lint commands]
```

## Run
```bash
[run commands]
```
```

**Path-Specific Rules** (Optional):
```markdown
---
paths: src/api/**/*.py
---

# API Route Rules
- All endpoints must include input validation
- Use standard error response format
```

**Auto-Chain**: After generating rules, automatically runs `/cdf:rules claudemd`.

### claudemd - Generate CLAUDE.md from Rules

Generate a concise `CLAUDE.generated.md` file from existing `.claude/rules/`.

```bash
/cdf:rules claudemd
```

**Prerequisites**: `.claude/rules/` must exist. If not, run `/cdf:rules generate` first.

**Behavioral Flow:**
1. **Verify**: Check for `.claude/rules/` with at least one `.md` file
2. **Read**: Extract key information from rule files
3. **Synthesize**: Generate concise `CLAUDE.generated.md`
4. **Output**: Write to project root

**What Gets Extracted:**
- From `architecture.md`: Project name, description, key directories
- From `tech-stack.md`: Language, framework, key libraries
- From `commands.md`: Setup, test, lint, run commands
- From `patterns.md`: Critical coding patterns/rules

**Output Template:**
```markdown
# [Project Name]

## Overview
[1-2 sentence description]

## Quick Start
```bash
[install/setup command]
[test command]
[lint command]
[run command]
```

## Critical Rules
1. **Read before edit** - understand code before changes
2. **DRY** - search with `rg` before writing similar code
3. **No backwards compat** - delete deprecated code immediately
4. **Tests required** - no feature complete without tests

## Project Rules
Auto-generated rules in `.claude/rules/` - Claude loads automatically.
Run `/cdf:rules generate` to refresh after major changes.

## Key Directories
- `[dir1]/` - [brief purpose]
- `[dir2]/` - [brief purpose]
```

**Guidelines:**
- Keep < 100 lines, never exceed 150
- WHY/WHAT/HOW: Purpose → Stack/Structure → Commands
- Progressive disclosure: Point to `.claude/rules/` for details
- Quick Start first: Most used commands at top

**Output Location**: Always writes to `CLAUDE.generated.md` (not `CLAUDE.md`) to preserve manual edits.

### status - Check Rules Status

Check if rules exist and whether they may need refresh.

```bash
/cdf:rules status
```

**Output:**
- Lists existing rule files
- Checks for `CLAUDE.md` or `CLAUDE.generated.md`
- Suggests regeneration if rules appear outdated

## Guidelines

- Use concise, technical language
- Focus on information useful for working in the codebase
- Base descriptions on actual code analysis, not README content
- Include specific file paths and code patterns observed
- Keep each file focused and scannable
- Use tables for structured data
- Include code examples for patterns

## Examples

### New Project Setup
```bash
# Generate full rules for a new project
/cdf:rules generate

# Review generated CLAUDE.generated.md
# Rename to CLAUDE.md if satisfied
```

### After Major Refactor
```bash
# Check current status
/cdf:rules status

# Regenerate rules
/cdf:rules generate --force

# Verify CLAUDE.md is updated
```

### Refresh CLAUDE.md Only
```bash
# Rules are current, just need new CLAUDE.md
/cdf:rules claudemd
```

## Boundaries

**Will:**
- Analyze codebase to generate accurate rules
- Create comprehensive `.claude/rules/` documentation
- Generate concise `CLAUDE.generated.md` from rules
- Auto-chain from generate to claudemd

**Will Not:**
- Generate rules without analyzing the actual codebase
- Overwrite `CLAUDE.md` (uses `.generated.md` suffix)
- Include sensitive information in generated files
- Generate rules for empty projects without user input

## Related Commands

- `/cdf:docs plan` - Strategic planning with task breakdown
- `/cdf:docs update` - Update dev documentation
- `/cdf:analyze` - Code quality analysis
