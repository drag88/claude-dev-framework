---
description: "Execute complex tasks with intelligent workflow management and delegation"
---

# /cdf:task - Enhanced Task Management

> Execute defined tasks with intelligent coordination and multi-agent delegation.

## Quick Start

```bash
# Execute a complex feature task
/cdf:task create "enterprise authentication system" --strategy systematic

# Parallel execution with delegation
/cdf:task execute "feature backlog" --strategy agile --delegate --parallel

# Enterprise-scale task execution
/cdf:task execute "microservices platform" --strategy enterprise
```

## When to Use

Use `/cdf:task` when:
- You have a clearly defined task ready for execution
- Task requires multi-agent coordination
- Need intelligent MCP routing and persona activation
- Executing pre-planned work items

**Don't use this command for**: Breaking down complex tasks (use `/cdf:spawn`), exploring unclear ideas (use `/cdf:brainstorm`), creating workflows from specs (use `/cdf:workflow`).

| Scenario | Command |
|----------|---------|
| Have an idea, need requirements | `/cdf:brainstorm` |
| Have a PRD/spec, need workflow | `/cdf:workflow` |
| Have complex task, need breakdown | `/cdf:spawn` |
| Have defined task, ready to execute | `/cdf:task` |

## Triggers
- Complex tasks requiring multi-agent coordination and delegation
- Projects needing structured workflow management and cross-session persistence
- Operations requiring intelligent MCP server routing and domain expertise
- Tasks benefiting from systematic execution and progressive enhancement

## Usage
```
/cdf:task [action] [target] [--strategy systematic|agile|enterprise] [--parallel] [--delegate]
```

## Behavioral Flow
1. **Analyze**: Parse task requirements and determine optimal execution strategy
2. **Delegate**: Route to appropriate MCP servers and activate relevant personas
3. **Coordinate**: Execute tasks with intelligent workflow management and parallel processing
4. **Validate**: Apply quality gates and comprehensive task completion verification
5. **Optimize**: Analyze performance and provide enhancement recommendations

Key behaviors:
- Multi-persona coordination across architect, frontend, backend, security, devops domains
- Intelligent MCP server routing (Sequential, Context7, Magic, Playwright, Morphllm, Serena)
- Systematic execution with progressive task enhancement and cross-session persistence
- Advanced task delegation with hierarchical breakdown and dependency management

## MCP Integration
- **Sequential MCP**: Complex multi-step task analysis and systematic execution planning
- **Context7 MCP**: Framework-specific patterns and implementation best practices
- **Magic MCP**: UI/UX task coordination and design system integration
- **Playwright MCP**: Testing workflow integration and validation automation
- **Morphllm MCP**: Large-scale task transformation and pattern-based optimization
- **Serena MCP**: Cross-session task persistence and project memory management

## Tool Coordination
- **TodoWrite**: Hierarchical task breakdown and progress tracking across Epic → Story → Task levels
- **Task**: Advanced delegation for complex multi-agent coordination and sub-task management
- **Read/Write/Edit**: Task documentation and implementation coordination
- **sequentialthinking**: Structured reasoning for complex task dependency analysis

## Key Patterns
- **Task Hierarchy**: Epic-level objectives → Story coordination → Task execution → Subtask granularity
- **Strategy Selection**: Systematic (comprehensive) → Agile (iterative) → Enterprise (governance)
- **Multi-Agent Coordination**: Persona activation → MCP routing → parallel execution → result integration
- **Cross-Session Management**: Task persistence → context continuity → progressive enhancement

## Examples

### Complex Feature Development
```
/cdf:task create "enterprise authentication system" --strategy systematic --parallel
# Comprehensive task breakdown with multi-domain coordination
# Activates architect, security, backend, frontend personas
```

### Agile Sprint Coordination
```
/cdf:task execute "feature backlog" --strategy agile --delegate
# Iterative task execution with intelligent delegation
# Cross-session persistence for sprint continuity
```

### Multi-Domain Integration
```
/cdf:task execute "microservices platform" --strategy enterprise --parallel
# Enterprise-scale coordination with compliance validation
# Parallel execution across multiple technical domains
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
Implement input validation for the user registration form

### 2. EXPECTED OUTCOME
- Validation functions for email, password, username fields
- Error messages displayed inline
- Form prevents submission until valid

### 3. REQUIRED SKILLS
frontend-architect

### 4. REQUIRED TOOLS
Read, Edit, Write, Grep

### 5. MUST DO
- Use existing validation utility in src/utils/validators.ts
- Follow project's error message conventions
- Add unit tests for each validator
- Ensure accessibility (aria-invalid, aria-describedby)

### 6. MUST NOT DO
- Change the form layout or styling
- Add new dependencies
- Modify backend validation logic

### 7. CONTEXT
- File paths: src/components/RegisterForm.tsx, src/utils/validators.ts
- Patterns: Project uses Zod for schema validation
- Constraints: Must work with existing form state management
```

## Boundaries

**Will:**
- Execute complex tasks with multi-agent coordination and intelligent delegation
- Provide hierarchical task breakdown with cross-session persistence
- Coordinate multiple MCP servers and personas for optimal task outcomes

**Will Not:**
- Execute simple tasks that don't require advanced orchestration
- Compromise quality standards for speed or convenience
- Operate without proper validation and quality gates