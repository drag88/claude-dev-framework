# Rules Generator Skill

Auto-generate `.claude/rules/` documentation for any codebase.

## When to Activate

- No `.claude/rules/` directory exists in the current project
- User asks about codebase structure or architecture
- User asks "what does this project do"
- Starting work on an unfamiliar codebase
- User explicitly asks to generate rules

## Actions

1. **Explore codebase** using the Explore agent to understand:
   - Directory structure and key files
   - Tech stack (languages, frameworks, libraries)
   - Architectural patterns and conventions
   - Build/test/run commands

2. **Generate `.claude/rules/` files**:
   - `architecture.md` - Directory structure, key files, component relationships, data flow
   - `tech-stack.md` - Languages, frameworks, libraries with purposes
   - `patterns.md` - Architectural patterns, code conventions, error handling
   - `commands.md` - Setup, build, test, lint, run commands

3. **Confirm completion** with summary of generated files

## File Format

Each rule file supports YAML frontmatter for path-specific rules:

```markdown
---
paths: src/api/**/*.py
---
# API Route Rules
- All endpoints must include input validation
- Use standard error response format
```

## Related Commands

- `/regenerate-rules` - Manually refresh all rules
- `/dev-docs` - Create task documentation structure
