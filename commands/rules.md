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

**Deep Analysis with Sub-Agents**

Quality rules require deep understanding of the entire codebase. Use sub-agents in parallel to cover ground efficiently:

- Spawn multiple Explore agents in parallel to analyze different parts of the codebase
- Use the codebase-navigator agent to trace dependencies and understand component relationships
- For architectural pattern identification, spawn an Explore agent with a focused brief (system design used to be a separate stub agent; the role is now handled by `/cdf:task` plus the Role line in CLAUDE.md)
- Take the time to investigate properly. Surface-level observations produce surface-level rules.

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

#### `.claude/rules/workflow.md` (required)
Generate at `.claude/rules/workflow.md` using `rules-templates/workflow-template.md` as the source. Customize only the "Project-Specific Spawn Patterns" section based on the detected project type — replace the placeholder block with 2-3 concrete subagent patterns relevant to this project's domain and tech stack. If project type is undetected, use the generic patterns. Keep all other sections verbatim from the template.

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

**Core Principle** (from code.claude.com/docs/en/best-practices): For every line in the generated file, ask: *"Would removing this cause Claude to make mistakes?"* If not, cut it. Target under 200 lines — the first 200 lines are prioritized. Content that lives in `.claude/rules/` (auto-loaded) does not get duplicated in CLAUDE.md — duplication causes 4.7 to pick one source arbitrarily when they conflict.

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

## Role
You are a [senior/staff] [language/discipline] engineer working on [project], a [one-clause description]. You ship to production and care about correctness, observability, and code quality.
[One sentence. Anchors tone and scope. Derive from architecture.md and tech-stack.md.]

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
See `@.claude/rules/workflow.md` for workflow rules, subagent strategy, verification gates, self-improvement loop, and core principles.

## Tool and subagent policy

Spawn multiple subagents in the same turn when fanning out across items, reading multiple files, or running independent investigations. Skip fan-out for single-file edits or trivial reads. For multi-agent debate or implementation work, use TeamCreate + named teammates rather than ad-hoc subagents.

<use_parallel_tool_calls>
For maximum efficiency, whenever you perform multiple independent operations,
invoke all relevant tools simultaneously rather than sequentially.
</use_parallel_tool_calls>

## CDF tools available

This project uses CDF (Claude Dev Framework). Reach for these instead of generic approaches:

- **Debugging bugs**: `/cdf:troubleshoot` — root-cause methodology, adds regression test
- **Pre-PR quality check**: `/cdf:verify --mode pre-pr` — types + lint + tests + security in one pass
- **Tests**: `/cdf:test` (coverage-aware), `/cdf:tdd` for RED-GREEN-REFACTOR
- **Multi-file investigation**: `/cdf:task` with codebase-navigator agent (returns summary, not raw dumps)
- **Library research / evaluation**: `/cdf:task` with library-researcher agent (evidence-backed, GitHub permalinks)
- **Refactoring**: `/cdf:improve` — systematic with safety checks
- **Code / security / perf analysis**: `/cdf:analyze` — multi-domain audit
- **Commit / ship**: `/cdf:git`, `/cdf:ship` — conventional commits, no AI attribution

Real-expertise agents (invoke via the Task tool): codebase-navigator, library-researcher, deep-research-agent, quality-engineer, refactoring-expert, e2e-specialist, tdd-guide, requirements-analyst, socratic-mentor, business-research-strategist, business-panel-experts, media-interpreter.

Skills auto-trigger from context (coding-standards, backend-patterns, frontend-patterns, tdd-workflow, e2e-patterns, frontend-design, failure-recovery, visual-explainer). Do not invoke manually.

For role-based work (backend, frontend, devops, security, perf, system design, docs) where no specific CDF tool fits, invoke `/cdf:task` directly — Opus 4.7 plays the role from the `## Role` line above plus `xhigh` effort.

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
- [e.g., "All API handlers use the `@validate_input` decorator. Reason: centralized request schema enforcement."]
- [e.g., "Database migrations require running `make migrate-check` before commit. Reason: catches missing reverse migrations."]
- [e.g., "Component tests use `renderWithProviders()` not bare `render()`. Reason: tests need theme + router context."]
[If no project-type rules exist, omit this section entirely. Each gotcha includes the why so 4.7 generalizes correctly.]

## Imports
@README.md
[Add other top-level docs the model should always have at hand. Skip if README is the only one.]

## Key Directories
- `[dir1]/` - [brief purpose]
- `[dir2]/` - [brief purpose]
[Max 5-7 directories from architecture.md codemap]
```

**Required Template Sections (10):**
1. **Role** - One sentence anchoring tone and scope (4.7 responds well to a clear role)
2. **Overview** - 1-2 sentence description
3. **Quick Start** - 4-5 bash commands (setup, test, lint, run)
4. **Critical Rules** - 4 standard rules
5. **Workflow** - 1-line pointer to `.claude/rules/workflow.md` (workflow content lives there, not duplicated here)
6. **Tool and subagent policy** - Authorize subagent fan-out + parallel calls explicitly (4.7 defaults are conservative)
7. **CDF tools available** - Routing table telling Claude which `/cdf:*` commands and agents to prefer for which tasks. Without this section, Claude does not reliably reach for CDF tools and falls back to generic approaches. Ship the section verbatim from the template.
8. **Plans Format** - `<plans_instruction>` XML block
9. **Commit Messages** - 1-line convention
10. **Key Directories** - Max 5-7 most important directories

**Optional Sections:**
- **Project-Specific Notes** - Only if project-type rules exist. Include 2-3 concrete, verifiable gotchas, each with the why.
- **Imports** - `@README.md` and other always-relevant top-level docs.

**Guidelines (Opus 4.7-aligned):**
- Target 80-120 lines. Never exceed 180 (excluding `<plans_instruction>` block).
- Every line must pass: "Would removing this cause Claude to make mistakes?"
- Progressive disclosure: point to `.claude/rules/` for details. Workflow content lives in `workflow.md`, not duplicated in CLAUDE.md.
- **No code style** — let linters handle formatting.
- **No content duplicated from `.claude/rules/`** — those files load automatically (path-scoped ones load when matching files are touched).
- Make instructions **concrete and verifiable**: "Run `npm test` and paste the output" beats "test your changes." 4.7 self-filters vague checks.
- **Frame rules as positive imperatives**, not prohibitions. "Use X" beats "Never Y." 4.7 wastes tokens on "don't" rules and may pattern-match into them.
- **State scope explicitly** on every rule. "Apply to every component, including third-party wrappers" beats "apply to components." 4.7 will not silently generalize.
- **Tone down forceful language**. Avoid CAPS, MUST, CRITICAL, "ANY", "ALWAYS". Use neutral imperatives. Forceful negatives cause overcompliance and hostile reading on 4.7.
- **Provide the why** behind non-obvious constraints. "Use Helvetica because react-pdf has no Unicode font" beats a bare "use Helvetica."

**Pre-generation step (Step 0):**
Read `rules-templates/claudemd-4-7-rulebook.md` (vendored into CDF). It is the authoritative rulebook for 4.7 CLAUDE.md generation. The Guidelines above become a fallback baseline only if the rulebook file is missing (which should never happen on a clean CDF install). The point is to generate a correct file by construction rather than auditing a possibly-wrong one after the fact. To update the rulebook, replace `rules-templates/claudemd-4-7-rulebook.md` with the latest version from your prompt47 skill (`~/.claude/skills/prompt47/references/claudemd-4-7.md`) and commit. The vendored copy makes the dependency travel with CDF rather than depending on a separately-installed user-global skill.

**Final pass before writing:**
Walk the audit checklist from the rulebook (17 questions if using prompt47 reference). Fix every "no" before writing the file. Report which rulebook was used in the completion message.

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

## Role
You are a senior Python engineer working on TaskFlow API, a FastAPI-based task management service with PostgreSQL and Redis. You ship to production and care about correctness, observability, and code quality.

## Overview
FastAPI-based task management API with PostgreSQL storage and Redis caching.

## Quick Start
```bash
uv sync                                 # Install dependencies
uv run pytest                           # Run tests
uv run ruff check .                     # Lint
uv run uvicorn app.main:app --reload    # Start dev server
```

## Critical Rules
1. **Read before edit** - understand code before changes
2. **DRY** - search with `rg` before writing similar code
3. **No backwards compat** - delete deprecated code immediately
4. **Tests required** - no feature complete without tests

## Workflow
See `@.claude/rules/workflow.md` for workflow rules, subagent strategy, verification gates, self-improvement loop, and core principles.

## Tool and subagent policy

Spawn multiple subagents in the same turn when fanning out across items, reading multiple files, or running independent investigations. Skip fan-out for single-file edits or trivial reads. For multi-agent debate or implementation work, use TeamCreate + named teammates rather than ad-hoc subagents.

<use_parallel_tool_calls>
For maximum efficiency, whenever you perform multiple independent operations,
invoke all relevant tools simultaneously rather than sequentially.
</use_parallel_tool_calls>

## CDF tools available

This project uses CDF (Claude Dev Framework). Reach for these instead of generic approaches:

- **Debugging bugs**: `/cdf:troubleshoot` — root-cause methodology, adds regression test
- **Pre-PR quality check**: `/cdf:verify --mode pre-pr` — types + lint + tests + security in one pass
- **Tests**: `/cdf:test` (coverage-aware), `/cdf:tdd` for RED-GREEN-REFACTOR
- **Multi-file investigation**: `/cdf:task` with codebase-navigator agent (returns summary, not raw dumps)
- **Library research / evaluation**: `/cdf:task` with library-researcher agent (evidence-backed, GitHub permalinks)
- **Refactoring**: `/cdf:improve` — systematic with safety checks
- **Code / security / perf analysis**: `/cdf:analyze` — multi-domain audit
- **Commit / ship**: `/cdf:git`, `/cdf:ship` — conventional commits, no AI attribution

Real-expertise agents (invoke via the Task tool): codebase-navigator, library-researcher, deep-research-agent, quality-engineer, refactoring-expert, e2e-specialist, tdd-guide, requirements-analyst, socratic-mentor, business-research-strategist, business-panel-experts, media-interpreter.

Skills auto-trigger from context (coding-standards, backend-patterns, frontend-patterns, tdd-workflow, e2e-patterns, frontend-design, failure-recovery, visual-explainer). Do not invoke manually.

For role-based work (backend, frontend, devops, security, perf, system design, docs) where no specific CDF tool fits, invoke `/cdf:task` directly — Opus 4.7 plays the role from the `## Role` line above plus `xhigh` effort.

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
- All API handlers use the `@validate_input` decorator. Reason: centralized request schema enforcement.
- Database migrations require running `make migrate-check` before commit. Reason: catches missing reverse migrations.

## Imports
@README.md

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
