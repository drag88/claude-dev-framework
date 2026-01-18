---
name: spawn
description: "Meta-system task orchestration with intelligent breakdown and delegation"
category: special
complexity: high
mcp-servers: []
personas: []
---

# /cdf:spawn - Meta-System Task Orchestration

> Break down complex operations into coordinated subtask hierarchies.

## Quick Start

```bash
# Break down a complex feature
/cdf:spawn "implement user authentication system"

# Deep decomposition with adaptive strategy
/cdf:spawn "migrate monolith to microservices" --strategy adaptive --depth deep

# Parallel infrastructure setup
/cdf:spawn "establish CI/CD pipeline with security scanning" --strategy parallel
```

## When to Use

Use `/cdf:spawn` when:
- Complex task needs breaking down into subtasks
- Operation spans multiple technical domains
- Need hierarchical task management (Epic → Story → Task)
- Coordinating parallel and sequential work streams

**Don't use this command for**: Executing already-defined tasks (use `/cdf:task`), exploring unclear ideas (use `/cdf:brainstorm`), generating workflows from PRDs (use `/cdf:workflow`).

| Scenario | Command |
|----------|---------|
| Have an idea, need requirements | `/cdf:brainstorm` |
| Have a PRD/spec, need workflow | `/cdf:workflow` |
| Have complex task, need breakdown | `/cdf:spawn` |
| Have defined task, ready to execute | `/cdf:task` |

## Triggers
- Complex multi-domain operations requiring intelligent task breakdown
- Large-scale system operations spanning multiple technical areas
- Operations requiring parallel coordination and dependency management
- Meta-level orchestration beyond standard command capabilities

## Usage
```
/cdf:spawn [complex-task] [--strategy sequential|parallel|adaptive] [--depth normal|deep]
```

## Behavioral Flow
1. **Analyze**: Parse complex operation requirements and assess scope across domains
2. **Decompose**: Break down operation into coordinated subtask hierarchies
3. **Orchestrate**: Execute tasks using optimal coordination strategy (parallel/sequential)
4. **Monitor**: Track progress across task hierarchies with dependency management
5. **Integrate**: Aggregate results and provide comprehensive orchestration summary

Key behaviors:
- Meta-system task decomposition with Epic → Story → Task → Subtask breakdown
- Intelligent coordination strategy selection based on operation characteristics
- Cross-domain operation management with parallel and sequential execution patterns
- Advanced dependency analysis and resource optimization across task hierarchies
## MCP Integration
- **Native Orchestration**: Meta-system command uses native coordination without MCP dependencies
- **Progressive Integration**: Coordination with systematic execution for progressive enhancement
- **Framework Integration**: Advanced integration with CDF orchestration layers

## Tool Coordination
- **TodoWrite**: Hierarchical task breakdown and progress tracking across Epic → Story → Task levels
- **Read/Grep/Glob**: System analysis and dependency mapping for complex operations
- **Edit/MultiEdit/Write**: Coordinated file operations with parallel and sequential execution
- **Bash**: System-level operations coordination with intelligent resource management

## Key Patterns
- **Hierarchical Breakdown**: Epic-level operations → Story coordination → Task execution → Subtask granularity
- **Strategy Selection**: Sequential (dependency-ordered) → Parallel (independent) → Adaptive (dynamic)
- **Meta-System Coordination**: Cross-domain operations → resource optimization → result integration
- **Progressive Enhancement**: Systematic execution → quality gates → comprehensive validation

## Examples

### Complex Feature Implementation
```
/cdf:spawn "implement user authentication system"
# Breakdown: Database design → Backend API → Frontend UI → Testing
# Coordinates across multiple domains with dependency management
```

### Large-Scale System Operation
```
/cdf:spawn "migrate legacy monolith to microservices" --strategy adaptive --depth deep
# Enterprise-scale operation with sophisticated orchestration
# Adaptive coordination based on operation characteristics
```

### Cross-Domain Infrastructure
```
/cdf:spawn "establish CI/CD pipeline with security scanning"
# System-wide infrastructure operation spanning DevOps, Security, Quality domains
# Parallel execution of independent components with validation gates
```

## Delegation Format

When delegating to subagents via the Task tool, use this 7-section structure for clarity and completeness:

```markdown
### 1. TASK
[Atomic, specific goal - one action only]

### 2. EXPECTED OUTCOME
[Concrete deliverables with measurable success criteria]

### 3. REQUIRED SKILLS
[Which CDF skill/agent to invoke, e.g., "codebase-navigator", "library-researcher"]

### 4. REQUIRED TOOLS
[Explicit tool whitelist, e.g., "Read, Grep, Glob" - no tools outside this list]

### 5. MUST DO
- [Exhaustive list of requirements]
- [Each requirement on its own line]
- [Be specific and actionable]

### 6. MUST NOT DO
- [Forbidden actions]
- [Scope boundaries]
- [Quality constraints]

### 7. CONTEXT
- File paths: [Relevant paths]
- Patterns: [Naming conventions, code patterns]
- Constraints: [Time, scope, dependencies]
```

### Example Delegation

```markdown
### 1. TASK
Find all usages of the deprecated `getUserById` function

### 2. EXPECTED OUTCOME
List of file paths with line numbers where `getUserById` is called

### 3. REQUIRED SKILLS
codebase-navigator

### 4. REQUIRED TOOLS
Grep, Glob, Read

### 5. MUST DO
- Search entire src/ directory
- Include test files
- Report exact line numbers
- Note if any usages are in type definitions

### 6. MUST NOT DO
- Modify any files
- Search node_modules
- Include the function definition itself

### 7. CONTEXT
- File paths: src/, tests/
- Patterns: Function may be imported as alias
- Constraints: Focus on .ts and .tsx files only
```

## Boundaries

**Will:**
- Decompose complex multi-domain operations into coordinated task hierarchies
- Provide intelligent orchestration with parallel and sequential coordination strategies
- Execute meta-system operations beyond standard command capabilities

**Will Not:**
- Replace domain-specific commands for simple operations
- Override user coordination preferences or execution strategies
- Execute operations without proper dependency analysis and validation