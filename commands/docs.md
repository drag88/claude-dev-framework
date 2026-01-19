---
description: "Unified documentation generation: component docs, project docs, strategic planning, and session updates"
---

# /cdf:docs - Unified Documentation System

> Generate documentation at any scope: component, project, strategic planning, or session updates.

## Quick Start

```bash
# Component-level documentation (inline, API)
/cdf:docs src/auth --scope component --type api

# Project-level documentation (structure, README)
/cdf:docs . --scope project --type structure

# Strategic planning with task breakdown
/cdf:docs plan "refactor authentication system"

# Update dev docs before context limit
/cdf:docs update
```

## When to Use

Use `/cdf:docs` when:
- Generating inline documentation or API references (component scope)
- Creating project documentation or knowledge bases (project scope)
- Planning complex features with task breakdown (planning scope)
- Preserving session context before context compaction (update)

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

**Behavioral Flow:**
1. **Analyze**: Understand request scope and examine relevant codebase
2. **Plan**: Create structured plan with phases and tasks
3. **Organize**: Generate task management structure in `dev/active/[task-name]/`
4. **Document**: Create plan, context, and tasks files

**Output Structure:**
```
dev/active/[task-name]/
├── [task-name]-plan.md      # Comprehensive strategic plan
├── [task-name]-context.md   # Key files, decisions, dependencies
└── [task-name]-tasks.md     # Checklist format for tracking
```

**Plan Contents:**
- Executive Summary
- Current State Analysis
- Implementation Phases
- Detailed Tasks with acceptance criteria
- Risk Assessment and Mitigation
- Success Metrics
- Timeline Estimates

**Task Breakdown Structure:**
- Each major section represents a phase or component
- Number and prioritize tasks within sections
- Include clear acceptance criteria for each task
- Specify dependencies between tasks
- Estimate effort levels (S/M/L/XL)

**Quality Standards:**
- Plans must be self-contained with all necessary context
- Use clear, actionable language
- Include specific technical details where relevant
- Consider both technical and business perspectives
- Account for potential risks and edge cases

**Context References (check if exists):**
- `PROJECT_KNOWLEDGE.md` - Architecture overview
- `BEST_PRACTICES.md` - Coding standards
- `TROUBLESHOOTING.md` - Common issues to avoid
- `dev/README.md` - Task management guidelines
- `CLAUDE.md` - Project-specific development standards

**Note**: Ideal to use AFTER exiting plan mode when you have a clear vision. Creates persistent task structure that survives context resets.

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

1. **Active Task Documentation** (`dev/active/[task-name]/`):
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

2. **Capture Session Context** (include relevant info about):
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
- Create task management structure for complex planning
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
- `/cdf:session save` - Save session context (different from docs update)
