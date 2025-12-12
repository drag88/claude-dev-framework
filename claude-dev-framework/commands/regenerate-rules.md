---
description: Generate project rules by analyzing codebase
---

Analyze this codebase thoroughly and generate `.claude/rules/` documentation.

## Analysis Steps

1. **Explore project structure** using the Explore agent
   - Identify key directories and their purposes
   - Find main entry points and configuration files
   - Understand the project's domain

2. **Analyze tech stack**
   - Read pyproject.toml, package.json, Gemfile, Cargo.toml, go.mod, etc.
   - Identify frameworks, libraries, and tools
   - Note testing and linting setup

3. **Understand code patterns**
   - Read key source files (main.py, app.py, index.ts, etc.)
   - Identify architectural patterns (async services, dependency injection, etc.)
   - Note naming conventions and code style

4. **Extract commands**
   - Find how to run tests, lint, and start the app
   - Document environment setup requirements

## Output Files

Generate these files in `.claude/rules/`:

### `architecture.md`
```markdown
# Architecture

## Directory Structure
- `src/` - [description]
- `tests/` - [description]
[etc.]

## Key Files
| File | Role |
|------|------|
| `app.py` | [role] |
[etc.]

## Component Relationships
[How different parts interact - can use ASCII diagram]

## Data Flow
[How data flows through the system]
```

### `tech-stack.md`
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
[etc.]

## Development Tools
- Testing: [tool]
- Linting: [tool]
- Type Checking: [tool]
```

### `patterns.md`
```markdown
# Code Patterns

## Architectural Patterns
- [Pattern] - [where/how used]

## Service Initialization
[Code example of how services are initialized]

## Error Handling
[Exception hierarchy, error handling patterns]

## Configuration
[How config is managed - env vars, settings files]

## Testing Patterns
[Test organization, fixtures, mocks]
```

### `commands.md`
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

## Path-Specific Rules (Optional)

For domain-specific rules, create additional files with YAML frontmatter:

### Example: `api-routes.md`
```markdown
---
paths: src/api/**/*.py
---

# API Route Rules

- All endpoints must include input validation
- Use standard error response format
- Include OpenAPI documentation comments
```

## Guidelines

- Use concise, technical language
- Focus on information useful for working in the codebase
- Base descriptions on actual code analysis, not README content
- Include specific file paths and code patterns observed
- Keep each file focused and scannable
- Use tables for structured data
- Include code examples for patterns
