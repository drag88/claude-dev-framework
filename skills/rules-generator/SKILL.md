---
name: generating-rules
description: "Auto-generates .claude/rules/ documentation for any codebase"
---

# Rules Generator Skill

Auto-generate `.claude/rules/` documentation for any codebase.

## When to Activate

- No `.claude/rules/` directory exists in the current project
- User asks about codebase structure or architecture
- User asks "what does this project do"
- Starting work on an unfamiliar codebase
- User explicitly asks to generate rules

## Actions

0. **Load rulebook**: Read `rules-templates/claudemd-4-7-rulebook.md` (vendored into CDF) as the authoritative reference for rule framing (positive imperatives, explicit scope, why-statements, neutral tone). Falls back to the embedded principles in this file only if the rulebook is missing.

1. **Explore codebase** using the Explore agent to understand:
   - Directory structure and key files
   - Tech stack (languages, frameworks, libraries)
   - Architectural patterns and conventions
   - Build/test/run commands

2. **Generate `.claude/rules/` files** with YAML frontmatter on every file:
   - `architecture.md` — Directory structure, key files, component relationships, data flow. Frontmatter: `description:` only (loads broadly).
   - `tech-stack.md` — Languages, frameworks, libraries with purposes. Frontmatter: `description:` only.
   - `patterns.md` — Architectural patterns, code conventions, error handling. Frontmatter: `description:` + `paths:` scoped to source dirs (e.g. `["src/**", "lib/**"]`).
   - `commands.md` — Setup, build, test, lint, run commands. Frontmatter: `description:` only.
   - Project-type files (`api-conventions.md`, `component-conventions.md`, etc.) — Always include `paths:` scoped to the relevant directory glob so they only load when matching files are touched.

3. **Frame rules as positive imperatives**, with explicit scope and the why where non-obvious. Example: "Apply to every API route, including admin routes. Reason: centralized auth check." Avoid CAPS, MUST, CRITICAL, "ANY", "ALWAYS".

4. **Confirm completion** with a summary listing each generated file, its line count, and whether it is path-scoped or always-loaded.

## File Format

Every rule file uses YAML frontmatter:

```markdown
---
description: One-line summary of what this file covers
paths: ["src/api/**/*.py", "src/middleware/**"]   # optional — omit to always-load
---
# API Route Rules

- Every endpoint validates input via the `@validate_input` decorator. Reason: centralized request schema enforcement.
- API errors return the standard `{error, code, details}` shape. Reason: client-side error parser depends on it.
```

Rules without `paths:` load every session. Use `paths:` for any topic that only applies when specific files are touched — this saves context across sessions that do not touch those files.

## Related Commands

- `/cdf:rules generate` - Manually refresh all rules
- `/cdf:docs plan` - Create task documentation structure
