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

**CRITICAL: Deep Analysis with Sub-Agents**

This command requires **extremely thorough analysis**. Use sub-agents liberally to ensure comprehensive understanding:

- **Spawn multiple Explore agents** in parallel to analyze different parts of the codebase
- **Use codebase-navigator agent** to trace dependencies and understand component relationships
- **Spawn system-architect agent** to identify architectural patterns and design decisions
- **Don't rush** - quality rules require deep understanding of the entire codebase

The goal is to produce rules that capture the project's true architecture, patterns, and conventions - not surface-level observations.

**Behavioral Flow:**
1. **Explore** (use Explore sub-agents in parallel):
   - Spawn agent to analyze `src/` or main source directory
   - Spawn agent to analyze `tests/` and testing patterns
   - Spawn agent to analyze config files and build setup
   - Identify key directories and their purposes
   - Find main entry points and configuration files
   - Understand the project's domain

2. **Analyze Tech Stack** (thorough investigation):
   - Read pyproject.toml, package.json, Gemfile, Cargo.toml, go.mod, etc.
   - Identify frameworks, libraries, and tools
   - Note testing and linting setup
   - Understand dependency relationships

3. **Understand Patterns** (spawn codebase-navigator if needed):
   - Read key source files (main.py, app.py, index.ts, etc.)
   - Trace how components interact
   - Identify architectural patterns
   - Note naming conventions and code style
   - Document error handling approaches

4. **Extract Commands**:
   - Find how to run tests, lint, and start the app
   - Document environment setup requirements
   - Note any custom scripts or workflows

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
See `/cdf:git` for commit message rules (conventional format, no Claude attribution).

## CDF Agents

When working in this project, use the appropriate CDF agent for specialized tasks:

| Task Type | Agent | Command |
|-----------|-------|---------|
| System design | system-architect | `/cdf:spawn` |
| API/backend work | backend-architect | `/cdf:spawn` |
| UI development | frontend-architect | `/cdf:spawn` |
| CI/CD setup | devops-architect | `/cdf:spawn` |
| Research topics | deep-research-agent | `/cdf:research` |
| Find code/patterns | codebase-navigator | `/cdf:spawn` |
| Evaluate libraries | library-researcher | `/cdf:spawn` |
| Debug issues | root-cause-analyst | `/cdf:troubleshoot` |
| Write tests | quality-engineer | `/cdf:test` |
| Security audit | security-engineer | `/cdf:analyze` |
| Performance | performance-engineer | `/cdf:analyze` |
| Refactor code | refactoring-expert | `/cdf:improve` |
| Documentation | technical-writer | `/cdf:docs` |
| TDD workflow | tdd-guide | `/cdf:tdd` |
| E2E testing | e2e-specialist | `/cdf:e2e` |

**Auto-activation**: Agents activate automatically via `/cdf:spawn` and `/cdf:task` based on task context.

## Project Rules
Auto-generated rules in `.claude/rules/` - Claude loads automatically.
Run `/cdf:rules generate` to refresh after major changes.

## Key Directories
- `[dir1]/` - [brief purpose]
- `[dir2]/` - [brief purpose]
```

**Required Template Sections:**
1. **Overview** - 1-2 sentence description
2. **Quick Start** - 4-5 bash commands (setup, test, lint, run)
3. **Critical Rules** - 4 standard rules (read before edit, DRY, no backwards compat, tests required)
4. **Plans Format** - Plans instruction block for unresolved questions
5. **Commit Messages** - Pointer to `/cdf:git` command
6. **CDF Agents** - Agent selection guide for specialized tasks
7. **Project Rules** - Pointer to `.claude/rules/`
8. **Key Directories** - Max 5-7 most important directories

**Guidelines:**
- Keep < 100 lines, never exceed 150
- WHY/WHAT/HOW: Purpose → Stack/Structure → Commands
- Progressive disclosure: Point to `.claude/rules/` for details
- Quick Start first: Most used commands at top
- **No code style**: Let linters handle formatting rules - don't include style guides
- **Key dirs only**: Don't list every subdirectory - max 5-7 most important

**Output Location**: Always writes to `CLAUDE.generated.md` (not `CLAUDE.md`) to preserve manual edits.

**Inform User After Generation:**
After generating `CLAUDE.generated.md`, inform the user:
- File created at `CLAUDE.generated.md`
- Review the content and rename to `CLAUDE.md` if satisfied
- Or merge changes into existing `CLAUDE.md`

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

### Example Output (FastAPI Project)

```markdown
# TaskFlow API

## Overview
FastAPI-based task management API with PostgreSQL storage and Redis caching.

## Quick Start
```bash
uv sync                    # Install dependencies
uv run pytest              # Run tests
uv run ruff check .        # Lint
uv run uvicorn app.main:app --reload  # Start dev server
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

Requirements:
- Make questions EXTREMELY concise
- Sacrifice grammar for concision
</plans_instruction>

## Commit Messages
See `/cdf:git` for commit message rules (conventional format, no Claude attribution).

## CDF Agents
[Agent table - see template above]

## Project Rules
Auto-generated rules in `.claude/rules/` - Claude loads automatically.
Run `/cdf:rules generate` to refresh after major changes.

## Key Directories
- `app/` - FastAPI application code
- `app/api/` - API route handlers
- `app/models/` - SQLAlchemy models
- `app/services/` - Business logic
- `tests/` - Test suite
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
