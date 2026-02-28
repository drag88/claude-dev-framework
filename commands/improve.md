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

## Triggers
- Code quality enhancement and refactoring requests
- Performance optimization and bottleneck resolution needs
- Maintainability improvements and technical debt reduction
- Best practices application and coding standards enforcement

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
2. **Plan**: Choose improvement approach and activate relevant personas for expertise
3. **Execute**: Apply systematic improvements with domain-specific best practices
4. **Validate**: Ensure improvements preserve functionality and meet quality standards
5. **Document**: Generate improvement summary and recommendations for future work

Key behaviors:
- Multi-persona coordination (architect, performance, quality, security) based on improvement type
- Framework-specific optimization via Context7 integration for best practices
- Systematic analysis via Sequential MCP for complex multi-component improvements
- Safe refactoring with comprehensive validation and rollback capabilities

## MCP Integration
- **Sequential MCP**: Auto-activated for complex multi-step improvement analysis and planning
- **Context7 MCP**: Framework-specific best practices and optimization patterns
- **Persona Coordination**: Architect (structure), Performance (speed), Quality (maintainability), Security (safety)

## Tool Coordination
- **Read/Grep/Glob**: Code analysis and improvement opportunity identification
- **Edit/MultiEdit**: Safe code modification and systematic refactoring
- **TodoWrite**: Progress tracking for complex multi-file improvement operations
- **Task**: Delegation for large-scale improvement workflows requiring systematic coordination

## Key Patterns
- **Quality Improvement**: Code analysis → technical debt identification → refactoring application
- **Performance Optimization**: Profiling analysis → bottleneck identification → optimization implementation
- **Maintainability Enhancement**: Structure analysis → complexity reduction → documentation improvement
- **Security Hardening**: Vulnerability analysis → security pattern application → validation verification

## Examples

### Code Quality Enhancement
```
/cdf:improve src/ --type quality --safe
# Systematic quality analysis with safe refactoring application
# Improves code structure, reduces technical debt, enhances readability
```

### Performance Optimization
```
/cdf:improve api-endpoints --type performance --interactive
# Performance persona analyzes bottlenecks and optimization opportunities
# Interactive guidance for complex performance improvement decisions
```

### Maintainability Improvements
```
/cdf:improve legacy-modules --type maintainability --preview
# Architect persona analyzes structure and suggests maintainability improvements
# Preview mode shows changes before application for review
```

### Security Hardening
```
/cdf:improve auth-service --type security --validate
# Security persona identifies vulnerabilities and applies security patterns
# Comprehensive validation ensures security improvements are effective
```

## Boundaries

**Will:**
- Apply systematic improvements with domain-specific expertise and validation
- Provide comprehensive analysis with multi-persona coordination and best practices
- Execute safe refactoring with rollback capabilities and quality preservation

**Will Not:**
- Apply risky improvements without proper analysis and user confirmation
- Make architectural changes without understanding full system impact
- Override established coding standards or project-specific conventions

## Agent Routing

| Improvement Type | Primary Agent | When to Use |
|-----------------|---------------|-------------|
| Refactoring | refactoring-expert | Dead code, duplication, pattern consolidation |
| Performance | performance-engineer | Query optimization, caching, bundle size |
| Security | security-engineer | Vulnerability fixes, auth hardening |
| Code quality | quality-engineer | Test coverage, naming, documentation |

## Next Commands
- `/cdf:verify` — Pre-PR quality check after improvements
- `/cdf:analyze` — Re-analyze to confirm improvements
- `/cdf:test` — Run tests to verify no regressions
