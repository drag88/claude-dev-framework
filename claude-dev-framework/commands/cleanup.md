---
description: "Systematically clean up code, remove dead code, and optimize project structure"
---

# /cdf:cleanup - Code and Project Cleanup

> Remove dead code, optimize imports, and clean up project structure.

## Quick Start

```bash
# Safe cleanup of source directory
/cdf:cleanup src/ --type code --safe

# Preview import optimization
/cdf:cleanup --type imports --preview

# Comprehensive cleanup with guidance
/cdf:cleanup --type all --interactive

# Aggressive cleanup (use with caution)
/cdf:cleanup components/ --aggressive
```

## When to Use

Use `/cdf:cleanup` when:
- Removing unused code, imports, or files
- Cleaning up after refactoring or feature removal
- Reducing codebase size and complexity
- Organizing project structure

**Don't use this command for**: Enhancing code quality or performance (use `/cdf:improve`), fixing bugs (use `/cdf:troubleshoot`).

| Goal | Command |
|------|---------|
| Remove waste (dead code, unused imports) | `/cdf:cleanup` |
| Enhance quality (refactor, optimize) | `/cdf:improve` |

## Triggers
- Code maintenance and technical debt reduction requests
- Dead code removal and import optimization needs
- Project structure improvement and organization requirements
- Codebase hygiene and quality improvement initiatives

## Usage
```
/cdf:cleanup [target] [--type code|imports|files|all] [--safe|--aggressive] [--interactive]
```

## Behavioral Flow
1. **Analyze**: Assess cleanup opportunities and safety considerations across target scope
2. **Plan**: Choose cleanup approach and activate relevant personas for domain expertise
3. **Execute**: Apply systematic cleanup with intelligent dead code detection and removal
4. **Validate**: Ensure no functionality loss through testing and safety verification
5. **Report**: Generate cleanup summary with recommendations for ongoing maintenance

Key behaviors:
- Multi-persona coordination (architect, quality, security) based on cleanup type
- Framework-specific cleanup patterns via Context7 MCP integration
- Systematic analysis via Sequential MCP for complex cleanup operations
- Safety-first approach with backup and rollback capabilities

## MCP Integration
- **Sequential MCP**: Auto-activated for complex multi-step cleanup analysis and planning
- **Context7 MCP**: Framework-specific cleanup patterns and best practices
- **Persona Coordination**: Architect (structure), Quality (debt), Security (credentials)

## Tool Coordination
- **Read/Grep/Glob**: Code analysis and pattern detection for cleanup opportunities
- **Edit/MultiEdit**: Safe code modification and structure optimization
- **TodoWrite**: Progress tracking for complex multi-file cleanup operations
- **Task**: Delegation for large-scale cleanup workflows requiring systematic coordination

## Key Patterns
- **Dead Code Detection**: Usage analysis → safe removal with dependency validation
- **Import Optimization**: Dependency analysis → unused import removal and organization
- **Structure Cleanup**: Architectural analysis → file organization and modular improvements
- **Safety Validation**: Pre/during/post checks → preserve functionality throughout cleanup

## Examples

### Safe Code Cleanup
```
/cdf:cleanup src/ --type code --safe
# Conservative cleanup with automatic safety validation
# Removes dead code while preserving all functionality
```

### Import Optimization
```
/cdf:cleanup --type imports --preview
# Analyzes and shows unused import cleanup without execution
# Framework-aware optimization via Context7 patterns
```

### Comprehensive Project Cleanup
```
/cdf:cleanup --type all --interactive
# Multi-domain cleanup with user guidance for complex decisions
# Activates all personas for comprehensive analysis
```

### Framework-Specific Cleanup
```
/cdf:cleanup components/ --aggressive
# Thorough cleanup with Context7 framework patterns
# Sequential analysis for complex dependency management
```

## Boundaries

**Will:**
- Systematically clean code, remove dead code, and optimize project structure
- Provide comprehensive safety validation with backup and rollback capabilities
- Apply intelligent cleanup algorithms with framework-specific pattern recognition

**Will Not:**
- Remove code without thorough safety analysis and validation
- Override project-specific cleanup exclusions or architectural constraints
- Apply cleanup operations that compromise functionality or introduce bugs