---
description: "Apply systematic improvements to code quality, performance, and maintainability"
---

# /cdf:improve - Code Improvement

> Enhance code quality, performance, and maintainability through systematic improvements.

## Quick Start

```bash
# Safe quality improvements
/cdf:improve src/ --type quality --safe

# Interactive performance optimization
/cdf:improve api-endpoints --type performance --interactive

# Preview maintainability improvements
/cdf:improve legacy-modules --type maintainability --preview

# Security hardening
/cdf:improve auth-service --type security --validate
```

## When to Use

Use `/cdf:improve` when:
- Refactoring code for better quality or readability
- Optimizing performance in slow areas
- Enhancing maintainability of complex code
- Applying security best practices

**Don't use this command for**: Analyzing code without changes (use `/cdf:analyze`).

## Usage
```
/cdf:improve [target] [--type quality|performance|maintainability|style|cleanup] [--safe] [--interactive]
```

### Cleanup Mode (`--type cleanup`)

When `--type cleanup` is specified, the command operates in cleanup mode (formerly `/cdf:cleanup`):

- **Dead code detection**: Usage analysis and safe removal with dependency validation
- **Import optimization**: Unused import removal and organization
- **Structure cleanup**: File organization and modular improvements
- **Safety validation**: Pre/during/post checks to preserve functionality

```bash
# Safe cleanup of source directory
/cdf:improve src/ --type cleanup --safe

# Preview import cleanup without execution
/cdf:improve --type cleanup --interactive

# Aggressive cleanup (use with caution)
/cdf:improve components/ --type cleanup
```

## Behavioral Flow
1. **Analyze**: Examine codebase for improvement opportunities and quality issues
2. **Plan**: Choose an improvement approach that fits the existing codebase
3. **Execute**: Apply systematic improvements with domain-specific best practices
4. **Validate**: Ensure improvements preserve functionality and meet quality standards
5. **Document**: Generate improvement summary and recommendations for future work

Key behaviors:
- Use judgement on conventions already in the repo; delegate via `/cdf:task` with role framing only when multi-file fan-out is warranted.
- Safe refactoring with comprehensive validation and rollback capabilities

## Examples

```
/cdf:improve src/ --type quality --safe
```

## Boundaries

**Will:**
- Apply systematic improvements with domain-specific expertise and validation
- Execute safe refactoring with rollback capabilities and quality preservation

**Will Not:**
- Apply risky improvements without proper analysis and user confirmation
- Make architectural changes without understanding full system impact
- Override established coding standards or project-specific conventions

## Agent Routing

| Improvement Type | Approach | When to Use |
|-----------------|----------|-------------|
| Refactoring | refactoring-expert | Dead code, duplication, pattern consolidation |
| Performance | `/cdf:task` with performance-focused role framing | Query optimization, caching, bundle size |
| Security | `/cdf:task` with security-focused role framing | Vulnerability fixes, auth hardening |
| Code quality | quality-engineer | Test coverage, naming, documentation |

## Next Commands
- `/cdf:verify` — Pre-PR quality check after improvements
- `/cdf:analyze` — Re-analyze to confirm improvements
- `/cdf:test` — Run tests to verify no regressions
