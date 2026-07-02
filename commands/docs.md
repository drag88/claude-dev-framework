---
description: "Strategic planning with task breakdown, or documentation generation"
argument-hint: "Describe what you need planned (e.g., 'refactor auth system', 'implement payments')"
---

# /cdf:docs - Strategic Planning & Documentation

> Create strategic plans with task breakdown, or generate documentation at various scopes.

## Default Behavior

**When invoked without a subcommand, `/cdf:docs` defaults to the `plan` subcommand.**

```bash
# These are equivalent:
/cdf:docs "refactor authentication system"
/cdf:docs plan "refactor authentication system"
```

If no arguments provided, ask the user what they want to plan or document.

## Quick Start

```bash
# Strategic planning (DEFAULT) - describe what needs planning
/cdf:docs "refactor authentication system"
/cdf:docs "implement payment gateway"

# Explicit subcommands
/cdf:docs plan "migrate to microservices"    # Strategic planning
/cdf:docs update                              # Update dev docs before context limit
/cdf:docs src/api --scope component --type api  # Component docs
```

## When to Use

Use `/cdf:docs` when:
- **Planning complex features** with structured task breakdown (default behavior)
- Preserving session context before context compaction (`update`)
- Generating inline documentation or API references (`--scope component`)
- Creating project documentation or knowledge bases (`--scope project`)

**Don't use this command for**: Project rules generation (use `/cdf:rules` instead).

## Scopes

### Component Scope (`--scope component`)

Generate focused documentation for specific components, functions, or APIs.

```bash
/cdf:docs [target] --scope component [--type inline|external|api|guide] [--style brief|detailed]
```

**Behavioral Flow:**
1. **Analyze**: Examine target component structure and interfaces
2. **Identify**: Determine documentation requirements and audience
3. **Generate**: Create appropriate documentation based on type
4. **Format**: Apply consistent structure and patterns
5. **Integrate**: Ensure compatibility with existing documentation

**Examples:**
```bash
# Inline code documentation (JSDoc/docstrings)
/cdf:docs src/auth/login.js --scope component --type inline

# API reference generation
/cdf:docs src/api --scope component --type api --style detailed

# User guide for a module
/cdf:docs payment-module --scope component --type guide
```

### Project Scope (`--scope project`)

Generate comprehensive project documentation and knowledge bases.

```bash
/cdf:docs [target] --scope project [--type docs|api|structure|readme] [--format md|json|yaml]
```

**Behavioral Flow:**
1. **Analyze**: Examine project structure and key components
2. **Organize**: Apply intelligent organization and cross-referencing
3. **Generate**: Create comprehensive documentation with framework patterns
4. **Validate**: Ensure documentation completeness and quality
5. **Maintain**: Update while preserving manual additions

**Examples:**
```bash
# Project structure documentation
/cdf:docs project-root --scope project --type structure

# API documentation for entire project
/cdf:docs src/api --scope project --type api --format json

# Knowledge base creation
/cdf:docs . --scope project --type docs
```

### Planning Scope (`plan` subcommand)

Create strategic plans with structured task breakdown for complex features.

```bash
/cdf:docs plan [task-description] [--strategy systematic|agile] [--detail brief|full]
```

**Delegation**: The `plan` subcommand delegates to the `compound-engineering:ce-plan` host skill. The compound-engineering plugin is required; if it is not installed, stop and tell the user to install the compound-engineering plugin for their host (install commands are in the README) rather than creating a replacement planning flow.

**CDF constraint**: Plan documentation lands in `docs/plans/`.

**Examples:**
```bash
# Plan a major refactor
/cdf:docs plan "refactor authentication system" --strategy systematic

# Plan new feature implementation
/cdf:docs plan "implement microservices" --detail full
```

### Update Subcommand (`update`)

Update development documentation before context compaction or session end.

```bash
/cdf:docs update [--focus context|tasks|all] [--summarize]
```

**Behavioral Flow:**
1. **Update Active Tasks**: Mark completed, add discovered tasks
2. **Capture Context**: Document decisions, blockers, insights
3. **Create Handoff**: Note exact state for session continuation
4. **Preserve Learning**: Store patterns and solutions

**What Gets Updated:**

1. **Plan Documents** (`docs/plans/`, written by `compound-engineering:ce-plan`):
   - Update the relevant plan's status notes rather than duplicating state elsewhere.

2. **Session Context** (`dev/active/[task-name]/`, machine-local scratch, gitignored):
   - `[task-name]-context.md`:
     - Current implementation state
     - Key decisions made this session
     - Files modified and why
     - Any blockers or issues discovered
     - Next immediate steps
     - Last Updated timestamp
   - `[task-name]-tasks.md`:
     - Mark completed tasks as ✅
     - Add any new tasks discovered
     - Update in-progress tasks with current status
     - Reorder priorities if needed

3. **Capture Session Context** (include relevant info about):
   - Complex problems solved
   - Architectural decisions made
   - Tricky bugs found and fixed
   - Integration points discovered
   - Testing approaches used
   - Performance optimizations made

3. **Update Memory** (if applicable):
   - Store any new patterns or solutions in project memory/documentation
   - Update entity relationships discovered
   - Add observations about system behavior

4. **Document Unfinished Work**:
   - What was being worked on when context limit approached
   - Exact state of any partially completed features
   - Commands that need to be run on restart
   - Any temporary workarounds that need permanent fixes

5. **Create Handoff Notes** (if switching conversations):
   - Exact file and line being edited
   - The goal of current changes
   - Any uncommitted changes that need attention
   - Test commands to verify work

**Priority**: Focus on capturing information that would be hard to rediscover or reconstruct from code alone.

**Examples:**
```bash
# Comprehensive update before context limit
/cdf:docs update

# Update with summary generation
/cdf:docs update --summarize

# Focus on specific area
/cdf:docs update --focus tasks
```

## MCP Integration

- **Sequential MCP**: Systematic analysis and documentation workflows
- **Context7 MCP**: Framework-specific patterns and standards
- **Persona Coordination**: Architect (structure), Technical Writer (content), Quality Engineer (validation)

## Tool Coordination

| Tool | Purpose |
|------|---------|
| `Read/Grep/Glob` | Project analysis and content extraction |
| `Write` | Documentation creation with cross-referencing |
| `TodoWrite` | Progress tracking for documentation workflows |
| `Task` | Delegation for large-scale documentation |

## Documentation Types

### Component Types (`--type`)
- `inline`: JSDoc/docstring comments in code
- `external`: Separate documentation files
- `api`: API reference with endpoints/schemas
- `guide`: User-focused tutorials and guides

### Project Types (`--type`)
- `docs`: Comprehensive knowledge base
- `api`: Full API documentation
- `structure`: Project structure and navigation
- `readme`: README generation/update

## Output Formats

- `md`: Markdown (default)
- `json`: JSON structure
- `yaml`: YAML format

## Examples

### Full Documentation Workflow
```bash
# 1. Generate project structure docs
/cdf:docs . --scope project --type structure

# 2. Generate API documentation
/cdf:docs src/api --scope component --type api --style detailed

# 3. Create strategic plan for new feature
/cdf:docs plan "add user authentication"

# 4. Update docs before session end
/cdf:docs update --summarize
```

### Component Documentation
```bash
# React component documentation
/cdf:docs src/components/Button --scope component --type external

# Python module documentation
/cdf:docs src/utils --scope component --type inline
```

### Strategic Planning
```bash
# Plan complex refactor
/cdf:docs plan "migrate to microservices architecture" --strategy systematic --detail full

# Plan feature with agile approach
/cdf:docs plan "implement payment gateway" --strategy agile
```

## Boundaries

**Will:**
- Generate documentation at any scope from inline to strategic
- Delegate strategic planning to `compound-engineering:ce-plan`
- Update documentation while preserving manual additions
- Apply framework-specific patterns and standards

**Will Not:**
- Generate project rules (use `/cdf:rules` instead)
- Override existing documentation without permission
- Expose sensitive implementation details
- Bypass established documentation standards

## Related Commands

- `/cdf:rules generate` - Generate project rules in `.claude/rules/`
- `/cdf:rules claudemd` - Generate CLAUDE.md from rules

## Agent Routing

| Documentation Mode | Approach | When to Use |
|-------------------|----------|-------------|
| API documentation | `/cdf:task` with the Role line in CLAUDE.md as a senior writer | Endpoint docs, SDK guides, integration specs |
| Architecture docs | `/cdf:task` with system-design role framing | ADRs, system diagrams, design rationale |
| Quality reports | quality-engineer (real agent, kept) | Coverage reports, test documentation |

## Next Commands
- `/cdf:implement` — Implement features described in documentation
- `/cdf:task` — Execute complex tasks with structured delegation
