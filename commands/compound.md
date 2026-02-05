---
description: "Capture institutional knowledge from solved problems for future sessions"
argument-hint: "[problem-description] [--category auto|build|test|runtime|performance|database|security|integration]"
---

# /cdf:compound - Knowledge Capture

> Transform solved problems into searchable institutional knowledge that compounds over time.

## Philosophy

**Each solved problem should make future problems easier.** This command extracts patterns, documents decisions, and creates reusable knowledge from your work.

## Quick Start

```bash
# Auto-detect category from context
/cdf:compound "fixed OAuth token refresh race condition"

# Specify category explicitly
/cdf:compound "resolved N+1 query in user listing" --category performance

# Capture from current session (after /cdf:flow or implementation)
/cdf:compound
```

## When to Use

Use `/cdf:compound` when:
- You've solved a non-trivial problem
- A bug fix involved debugging that others might repeat
- You discovered a gotcha or edge case
- You want to preserve architectural decisions
- After completing `/cdf:flow` or any significant implementation

**Don't use this command for**: Trivial fixes, simple typos, or well-documented patterns.

## Behavioral Flow

1. **Analyze**: Examine recent changes, commits, or specified problem
2. **Extract**: Identify root cause, solution approach, and patterns
3. **Classify**: Determine appropriate category
4. **Document**: Create structured solution document
5. **Index**: Update project knowledge index

## Output Structure

Creates documents in `docs/solutions/[category]/`:

```
docs/solutions/
├── build-errors/
│   └── 2024-01-15-webpack-module-resolution.md
├── test-failures/
│   └── 2024-01-14-flaky-async-test.md
├── runtime-errors/
│   └── 2024-01-15-oauth-token-refresh.md
├── performance-issues/
│   └── 2024-01-13-n-plus-one-query.md
├── database-issues/
│   └── 2024-01-12-migration-deadlock.md
├── security-issues/
│   └── 2024-01-11-xss-in-comments.md
├── ui-bugs/
│   └── 2024-01-10-modal-focus-trap.md
└── integration-issues/
    └── 2024-01-09-api-timeout-handling.md
```

## Document Template

```markdown
---
title: "OAuth Token Refresh Race Condition"
date: 2024-01-15
category: runtime-errors
tags: [auth, oauth, race-condition, async]
module: src/auth
symptom: "TokenExpiredError on concurrent requests"
severity: high
time_to_fix: 2h
---

# OAuth Token Refresh Race Condition

## Symptom
Brief description of how the problem manifested.

## Root Cause
Analysis of why the problem occurred.

## Solution
What was done to fix it, with code examples.

## Prevention
How to avoid this problem in the future.

## Related
- Links to related solutions
- External references
```

## Categories

| Category | Symptoms |
|----------|----------|
| `build-errors` | Compilation failures, bundler issues, dependency conflicts |
| `test-failures` | Flaky tests, assertion failures, test environment issues |
| `runtime-errors` | Exceptions, crashes, unexpected behavior |
| `performance-issues` | Slow queries, memory leaks, render bottlenecks |
| `database-issues` | Migrations, deadlocks, data integrity |
| `security-issues` | Vulnerabilities, auth problems, data exposure |
| `ui-bugs` | Layout issues, interaction problems, accessibility |
| `integration-issues` | API failures, service communication, external dependencies |

## Arguments

| Argument | Description |
|----------|-------------|
| `[problem-description]` | Brief description of what was solved |
| `--category` | Override auto-detection: `build`, `test`, `runtime`, etc. |
| `--from-flow` | Extract from active flow state (auto if in flow) |
| `--severity` | Set severity: `low`, `medium`, `high`, `critical` |

## Auto-Detection

When no description provided, analyze:
1. Recent git commits in current branch
2. Active flow state (`dev/active/*/flow-state.md`)
3. Recent file modifications
4. Test results and error logs

## YAML Frontmatter Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `title` | Searchable title | "OAuth Token Refresh Race Condition" |
| `date` | When documented | 2024-01-15 |
| `category` | Solution category | runtime-errors |
| `tags` | Searchable keywords | [auth, oauth, async] |
| `module` | Affected code area | src/auth |
| `symptom` | How problem appeared | "TokenExpiredError on concurrent requests" |
| `severity` | Impact level | high |
| `time_to_fix` | Effort required | 2h |

## Searching Solutions

Solutions are searchable via tags, symptoms, and modules:

```bash
# Search by symptom (grep in docs/solutions/)
grep -r "TokenExpiredError" docs/solutions/

# Search by tag
grep -l "tags:.*oauth" docs/solutions/**/*.md

# Search by module
grep -l "module: src/auth" docs/solutions/**/*.md
```

Future: Integrate with `/cdf:research` to auto-surface relevant solutions.

## Integration with /cdf:flow

When used as final phase of `/cdf:flow`:
1. Automatically extracts from flow context
2. Uses flow-plan.md for problem description
3. Uses flow-context.md for decisions
4. Creates flow-compound.md in active directory
5. Copies to `docs/solutions/` for persistence

## Examples

### After Fixing a Bug
```bash
/cdf:compound "Fixed race condition where multiple API calls could trigger simultaneous token refresh"
# Creates: docs/solutions/runtime-errors/2024-01-15-token-refresh-race-condition.md
```

### After Performance Optimization
```bash
/cdf:compound "Resolved N+1 query in user listing by eager loading associations" --category performance
# Creates: docs/solutions/performance-issues/2024-01-15-user-listing-eager-load.md
```

### After Completing a Flow
```bash
/cdf:compound --from-flow
# Extracts context from dev/active/[current-task]/
# Summarizes decisions, patterns, and learnings
```

## MCP Integration

- **Sequential MCP**: Structured analysis of problem and solution
- **Context7 MCP**: Check if solution matches known patterns

## Tool Coordination

| Tool | Purpose |
|------|---------|
| `Read` | Analyze recent changes and flow state |
| `Grep` | Search for related code patterns |
| `Write` | Create solution document |
| `Bash` | Check git history for context |

## Boundaries

**Will:**
- Extract knowledge from solved problems
- Create searchable, structured documentation
- Identify patterns and prevention strategies
- Link related solutions

**Will Not:**
- Document trivial fixes
- Expose sensitive information (credentials, keys)
- Override existing solutions (creates new version)
- Auto-commit solution documents

## Related Commands

- `/cdf:flow` - Unified workflow that ends with compound
- `/cdf:learn` - Extract patterns mid-session
- `/cdf:docs` - General documentation
- `/cdf:research` - Search for existing solutions
