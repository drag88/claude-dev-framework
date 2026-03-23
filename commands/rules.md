---
description: "Project rules management: generate .claude/rules/ and CLAUDE.md documentation"
---

# /cdf:rules - Project Rules Management

> Generate and manage project rules in `.claude/rules/` and `CLAUDE.md`.

## Quick Start

```bash
# Generate full rules from codebase analysis (now project-type aware)
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

5. **Generate Files** — ALL of the following are REQUIRED:

**Output Files (all must be generated):**

#### `architecture.md` (matklad-inspired)
```markdown
# Architecture

## Bird's Eye View
[1-2 sentences: what problem this solves and how]

## Codemap
[Coarse-grained modules/directories, what each does, key types/files to know about]
- `src/module_a/` - [what it does]. Key type: `WidgetManager`. Depends on `module_b`.
- `src/module_b/` - [what it does]. Entry point: `main.rs`.

## Cross-Cutting Concerns
[Logging, error handling, auth, config patterns that span modules]

## Architectural Invariants
[Things that must NOT happen - constraints, absences, hard rules]
- Module A never directly accesses the database
- All external API calls go through the client wrapper

## [Project-Type Sections]
[Detected automatically — e.g., Data Flow for ML, Component Hierarchy for Frontend]
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

**Project-Type-Specific Files** (generated only when detected):

| Project Type | Additional Files | Architecture Sections |
|-------------|-----------------|----------------------|
| ML/Data Science | `experiment-tracking.md`, `data-contracts.md` | Data Flow, Environment Matrix |
| Frontend | `component-conventions.md`, `accessibility.md` | Component Hierarchy, Route Structure |
| Backend API | `api-conventions.md`, `database-rules.md` | Request Lifecycle, DB Schema |
| Data Engineering | `pipeline-conventions.md`, `data-quality.md` | Pipeline DAG, Data Lineage |
| Mobile | `platform-rules.md`, `navigation.md` | Screen Flow, Native Bridge |
| CLI/Library | `public-api.md`, `versioning.md` | API Surface Map |
| Monorepo | `workspace-map.md`, `change-impact.md` | Package Dependency Graph |
| Infrastructure | `iac-conventions.md`, `security-baseline.md` | Infra Topology, Module Tree |

#### `.claude/rules/workflow.md` (REQUIRED)
MUST generate at `.claude/rules/workflow.md`. Use `rules-templates/workflow-template.md` as the source template. Customize only the "Project-Specific Spawn Patterns" section based on the detected project type — replace the placeholder block with 2-3 concrete subagent patterns relevant to this project's domain and tech stack. If project type is undetected, use the generic patterns. Keep all other sections verbatim from the template.

**Path-Specific Rules** (Optional):
```markdown
---
paths: src/api/**/*.py
---

# API Route Rules
- All endpoints must include input validation
- Use standard error response format
```

6. **Verify** all files were created:
   - `.claude/rules/architecture.md`
   - `.claude/rules/tech-stack.md`
   - `.claude/rules/patterns.md`
   - `.claude/rules/commands.md`
   - `.claude/rules/workflow.md`
   - Any project-type-specific files

**Auto-Chain**: After generating rules, automatically runs `/cdf:rules claudemd`.

### claudemd - Generate CLAUDE.md from Rules

Generate a concise `CLAUDE.generated.md` file from existing `.claude/rules/`.

```bash
/cdf:rules claudemd
```

**Prerequisites**: `.claude/rules/` must exist. If not, run `/cdf:rules generate` first.

**Core Principle** (from code.claude.com/docs/en/best-practices): For every line in the generated file, ask: *"Would removing this cause Claude to make mistakes?"* If not, cut it. Target < 200 lines — first 200 lines are prioritized. Content that already lives in `.claude/rules/` loads automatically and MUST NOT be duplicated in CLAUDE.md.

**Behavioral Flow:**
1. **Verify**: Check for `.claude/rules/` with at least one `.md` file
2. **Read rule files** and extract:
   - From `architecture.md`: Project name, description, key directories
   - From `tech-stack.md`: Language, framework, key libraries
   - From `commands.md`: Setup, test, lint, run commands
   - From `patterns.md`: Critical coding patterns/rules
   - From project-type-specific rules (if they exist): 2-3 non-obvious gotchas
3. **Check what `.claude/rules/` already covers** — do NOT repeat it
4. **Synthesize**: Generate concise `CLAUDE.generated.md` using the Output Template
5. **Output**: Write to project root as `CLAUDE.generated.md`

**What Goes Where:**

| Content | In CLAUDE.md? | Why |
|---------|--------------|-----|
| Overview, Quick Start | YES | Essential orientation for every interaction |
| Critical Rules (4 standard) | YES | High-signal, prevents common mistakes |
| Workflow summary (3 lines) | YES | Quick orientation — details in `.claude/rules/workflow.md` |
| Plans Format (`<plans_instruction>`) | YES | XML processing tag — safest in guaranteed-load file |
| Commit message convention | YES | 1-line pointer, high-frequency need |
| Key directories | YES | Orientation for every task |
| Project-specific gotchas | YES | Non-obvious things Claude would get wrong |
| Full workflow (8 subsections) | NO | Already in `.claude/rules/workflow.md`, auto-loads |
| CDF Agents table | NO | Already in `.claude/rules/workflow.md`, auto-loads |
| Memory guidance | NO | Already in `.claude/rules/workflow.md`, auto-loads |
| Architecture details | NO | Already in `.claude/rules/architecture.md`, auto-loads |
| Code patterns | NO | Already in `.claude/rules/patterns.md`, auto-loads |

**Output Template:**
```markdown
# [Project Name]

## Overview
[1-2 sentence description derived from architecture.md]

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

## Workflow
Explore → Plan → Code → Verify. Always explore full scope before piecemeal edits.
Plan mode for 3+ step tasks. Subagents for exploration; agent teams for parallel implementation.
Full workflow, agent routing table, and delegation patterns in `.claude/rules/workflow.md`.

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
Conventional format (`feat:`, `fix:`, `docs:`), no Claude attribution.

## Project-Specific Notes
[2-3 non-obvious gotchas derived from project-type-specific rule files.
Only include if project-type rules exist. Examples:]
- [e.g., "All API handlers must use the `@validate_input` decorator"]
- [e.g., "Database migrations require running `make migrate-check` before commit"]
- [e.g., "Component tests use `renderWithProviders()` not bare `render()`"]
[If no project-type rules exist, omit this section entirely.]

## Key Directories
- `[dir1]/` - [brief purpose]
- `[dir2]/` - [brief purpose]
[Max 5-7 directories from architecture.md codemap]
```

**Required Template Sections (7):**
1. **Overview** - 1-2 sentence description
2. **Quick Start** - 4-5 bash commands (setup, test, lint, run)
3. **Critical Rules** - 4 standard rules
4. **Workflow** - 3-line summary pointing to `.claude/rules/workflow.md`
5. **Plans Format** - `<plans_instruction>` XML block
6. **Commit Messages** - 1-line convention
7. **Key Directories** - Max 5-7 most important directories

**Optional Section:**
- **Project-Specific Notes** - Only if project-type rules exist. Include 2-3 concrete, verifiable gotchas.

**Guidelines:**
- Target 50-70 lines. Never exceed 80 (excluding `<plans_instruction>` block)
- Every line must pass: "Would removing this cause Claude to make mistakes?"
- Progressive disclosure: point to `.claude/rules/` for details
- **No code style** — let linters handle formatting
- **No content from `.claude/rules/`** — it loads automatically
- Make instructions **concrete and verifiable**: "Run `npm test`" not "test your changes"

**Output Location**: Always writes to `CLAUDE.generated.md` (not `CLAUDE.md`) to preserve manual edits.

**Inform User After Generation:**
After generating `CLAUDE.generated.md`, inform the user:
- File created at `CLAUDE.generated.md`
- Review and rename to `CLAUDE.md` if satisfied, or merge into existing `CLAUDE.md`
- Note: full workflow, agents, and memory details live in `.claude/rules/workflow.md`

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

## Workflow

### Explore → Plan → Code → Verify
- Use plan mode for non-trivial tasks (3+ steps or multi-file changes)
- For small fixes (typo, rename, single-file change), skip planning and execute directly
- If something goes sideways, STOP and re-plan — do not push through a broken approach

### Subagent Strategy
- Use subagents for exploration and research to keep main context clean
- One atomic goal per subagent — return summaries, not raw file dumps
- For complex problems, spawn parallel subagents covering different angles
- Main context is for implementation only

### Verification Before Done
- Never mark a task complete without proving it works
- Run tests, check logs, demonstrate correctness
- For visual/UI changes: verify in the browser before confirming to the user
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"

### Self-Improvement Loop
- After ANY correction from the user: capture the pattern in `.claude/rules/`
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these rules until mistake rate drops
- Review rules at session start for relevant project

### Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting it

### Autonomous Bug Fixing
- Given a bug report: identify root cause, fix it, add regression test, verify
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user

### Context Management
- Run /clear between unrelated tasks
- Use /compact when context grows large
- After 2 failed corrections on the same issue, clear context and restart with a better prompt

### Core Principles
- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Only touch what's necessary. No side effects with new bugs.

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

## Memory
- Check auto-memory for prior context at session start
- Save key decisions, debugging insights, and project patterns to auto-memory during work

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
- Detect project type and generate type-specific rules
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
