# Solutions Directory

Institutional knowledge captured from solved problems.

## Directory Structure

```
docs/solutions/
├── build-errors/       # Compilation, bundler, dependency issues
├── test-failures/      # Flaky tests, assertion failures, test env
├── runtime-errors/     # Exceptions, crashes, unexpected behavior
├── performance-issues/ # Slow queries, memory leaks, bottlenecks
├── database-issues/    # Migrations, deadlocks, data integrity
├── security-issues/    # Vulnerabilities, auth problems
├── ui-bugs/           # Layout, interaction, accessibility
└── integration-issues/ # API failures, external dependencies
```

## Document Format

Each solution uses YAML frontmatter for searchability:

```yaml
---
title: "Problem Title"
date: 2024-01-15
category: runtime-errors
tags: [auth, oauth, async]
module: src/auth
symptom: "Error message or behavior"
severity: high
time_to_fix: 2h
---
```

## Searching Solutions

```bash
# By symptom
grep -r "TokenExpiredError" docs/solutions/

# By tag
grep -l "tags:.*oauth" docs/solutions/**/*.md

# By module
grep -l "module: src/auth" docs/solutions/**/*.md

# By severity
grep -l "severity: high" docs/solutions/**/*.md
```

## Creating Solutions

Solutions are created by:
1. `/cdf:flow` - Knowledge capture during workflow
2. Auto-memory hooks (`memory-summarize.py`) - Session-end pattern extraction
3. Manual creation following the template

## Template

```markdown
---
title: "Problem Title"
date: YYYY-MM-DD
category: [category]
tags: [relevant, tags]
module: src/affected/module
symptom: "How the problem manifested"
severity: low|medium|high|critical
time_to_fix: Xh
---

# Problem Title

## Symptom
Brief description of how the problem manifested.

## Root Cause
Analysis of why the problem occurred.

## Solution
What was done to fix it, with code examples if relevant.

## Prevention
How to avoid this problem in the future.

## Related
- Links to related solutions
- External references
```
