# AGENTS.md Template

> Template for generating root `AGENTS.md` — cross-tool AI agent compatibility file.

# AGENTS.md

## Project Overview

[1-2 sentence elevator pitch from README or package description]

**Tech Stack**: [language] + [framework] + [database] + [key libraries]
**Status**: [active development / stable / maintenance]

## Development Setup

```bash
# Install dependencies
[detect: npm install / pip install -e . / cargo build / go mod download]

# Run tests
[detect: npm test / pytest / cargo test / go test ./...]

# Lint and format
[detect: npm run lint / ruff check . / cargo clippy]

# Start development server
[detect: npm run dev / python manage.py runserver / cargo run]
```

## Architecture

[Condensed codemap — key directories and their roles]

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `[src/]` | [Core application logic] | [entry point] |
| `[tests/]` | [Test suite] | [test config] |
| `[config/]` | [Configuration] | [main config file] |

### Key Relationships
- `[module A]` depends on `[module B]` for [reason]
- `[module C]` is the entry point, orchestrating [what]
- `[module D]` is standalone and can be modified independently

## Coding Standards

- [Key pattern 1 — e.g., "All API handlers follow request→validate→process→respond"]
- [Key pattern 2 — e.g., "Error handling uses Result types, never bare exceptions"]
- [Key pattern 3 — e.g., "Database access only through repository layer"]
- [Key pattern 4 — e.g., "All public functions have docstrings"]

## Testing Requirements

- **Framework**: [pytest / jest / cargo test]
- **Coverage threshold**: [detect from config, default 80%]
- **Test naming**: [test_should_... / it('should ...') / descriptive]
- **Required for**: [all new features / bug fixes / API changes]

## Agent-Specific Guidelines

### File Safety
- **Never modify**: [lock files, migrations, generated code, CI config]
- **Never commit**: [.env files, credentials, large binaries]
- **Caution**: [public API surface, database schema, auth logic]

### After Every Change
1. Run [test command]
2. Run [lint command]
3. Verify no regressions in [critical path]

### Multi-Agent Safety
These files should not be edited concurrently:
- [lock files, migration files, generated indices]
- [shared config files that multiple features touch]

## Domain Knowledge

| Domain | Why It Matters | Key Files |
|--------|---------------|-----------|
| [detected domain 1] | [context for AI agents] | [relevant paths] |
| [detected domain 2] | [context for AI agents] | [relevant paths] |

## Common Tasks

| Task | Command | Notes |
|------|---------|-------|
| Add a new feature | [workflow] | [key files to touch] |
| Fix a bug | [workflow] | [where to add tests] |
| Update dependencies | [command] | [check for breaking changes] |
