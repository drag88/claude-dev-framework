---
name: help
description: "List all available CDF commands and their functionality"
category: utility
complexity: low
mcp-servers: []
personas: []
---

# /cdf:help - Command Reference Documentation

> Complete reference for all Claude Dev Framework (CDF) commands.

## Quick Start

```bash
# Show this help
/cdf:help

# Most common commands
/cdf:implement "add user authentication"   # Implement features
/cdf:analyze src/ --focus security         # Analyze code
/cdf:test --coverage                       # Run tests
/cdf:rules generate                        # Generate project rules
```

## Commands

| Command | Category | Description |
|---------|----------|-------------|
| `/cdf:analyze` | utility | Code analysis across quality, security, performance, architecture |
| `/cdf:brainstorm` | orchestration | Interactive requirements discovery through Socratic dialogue |
| `/cdf:build` | utility | Build, compile, and package projects with error handling |
| `/cdf:cleanup` | workflow | Clean up code, remove dead code, optimize structure |
| `/cdf:design` | utility | Design system architecture, APIs, and component interfaces |
| `/cdf:docs` | utility | **Unified documentation**: component, project, planning, updates |
| `/cdf:estimate` | special | Development estimates for tasks, features, or projects |
| `/cdf:explain` | workflow | Clear explanations of code, concepts, and system behavior |
| `/cdf:git` | utility | Git operations with intelligent commit messages |
| `/cdf:help` | meta | List all available commands and their functionality |
| `/cdf:implement` | workflow | Feature implementation with persona activation and MCP |
| `/cdf:improve` | workflow | Systematic improvements to code quality and performance |
| `/cdf:panel` | analysis | **Expert panels**: business strategy and spec review |
| `/cdf:research` | command | Deep web research with adaptive depth |
| `/cdf:rules` | utility | **Project rules**: generate .claude/rules/ and CLAUDE.md |
| `/cdf:select-tool` | special | Intelligent MCP tool selection based on complexity |
| `/cdf:session` | session | **Session lifecycle**: load, save, reflect on progress |
| `/cdf:spawn` | orchestration | Meta-system task orchestration with breakdown |
| `/cdf:task` | orchestration | Execute complex tasks with workflow management |
| `/cdf:test` | utility | Execute tests with coverage and quality reporting |
| `/cdf:troubleshoot` | utility | Diagnose and resolve issues in code, builds, deployments |
| `/cdf:workflow` | orchestration | Generate implementation workflows from PRDs |

## Consolidated Commands

These commands combine related functionality:

### /cdf:session (replaces: load, save, reflect)
```bash
/cdf:session load [checkpoint]           # Load project context
/cdf:session save [--checkpoint]         # Save session state
/cdf:session reflect [--type completion] # Validate task completion
/cdf:session list                        # List checkpoints
```

### /cdf:panel (replaces: business-panel, spec-panel)
```bash
/cdf:panel [doc] --type business         # Business thought leaders
/cdf:panel [doc] --type spec             # Software engineering experts
/cdf:panel [doc] --mode socratic         # Learning mode
```

### /cdf:docs (replaces: document, index, dev-docs, dev-docs-update)
```bash
/cdf:docs [target] --scope component     # Component docs
/cdf:docs [target] --scope project       # Project docs
/cdf:docs plan "task name"               # Strategic planning
/cdf:docs update                         # Update before context limit
```

### /cdf:rules (replaces: regenerate-rules, generate-claude-md)
```bash
/cdf:rules generate                      # Analyze codebase, create rules
/cdf:rules claudemd                      # Generate CLAUDE.md from rules
/cdf:rules status                        # Check if rules need refresh
```

## Command Categories

### Orchestration (Complex Multi-Step)
- `/cdf:brainstorm` - Ideation and requirements discovery
- `/cdf:workflow` - PRD to implementation workflow
- `/cdf:spawn` - Task decomposition
- `/cdf:task` - Task execution

**When to use which:**
| Scenario | Command |
|----------|---------|
| Have an idea, need requirements | `/cdf:brainstorm` |
| Have a PRD/spec, need workflow | `/cdf:workflow` |
| Have complex task, need breakdown | `/cdf:spawn` |
| Have defined task, ready to execute | `/cdf:task` |

### Utility (Single Purpose)
- `/cdf:analyze` - Code quality/security analysis
- `/cdf:build` - Build and package
- `/cdf:design` - Architecture and API design
- `/cdf:docs` - All documentation
- `/cdf:git` - Git operations
- `/cdf:rules` - Project rules management
- `/cdf:test` - Testing and QA
- `/cdf:troubleshoot` - Issue diagnosis

### Workflow (Code Changes)
- `/cdf:cleanup` - Remove dead code
- `/cdf:explain` - Understand code
- `/cdf:implement` - Build features
- `/cdf:improve` - Enhance quality

### Analysis
- `/cdf:panel` - Expert panel discussions
- `/cdf:research` - Deep web research

### Session
- `/cdf:session` - Load/save/reflect

## CDF Framework Flags

Use these flags with any `/cdf:` command to customize behavior.

### MCP Server Flags

| Flag | Purpose |
|------|---------|
| `--c7` / `--context7` | Framework documentation lookup |
| `--seq` / `--sequential` | Structured multi-step reasoning |
| `--magic` | Modern UI generation |
| `--morph` / `--morphllm` | Bulk code transformations |
| `--serena` | Session persistence and memory |
| `--play` / `--playwright` | Browser automation and testing |
| `--all-mcp` | Enable all MCP servers |
| `--no-mcp` | Disable all MCP servers |

### Analysis Depth Flags

| Flag | Depth | Tokens |
|------|-------|--------|
| `--think` | Standard | ~4K |
| `--think-hard` | Deep | ~10K |
| `--ultrathink` | Maximum | ~32K |

### Execution Control Flags

| Flag | Purpose |
|------|---------|
| `--delegate [auto\|files\|folders]` | Sub-agent parallel processing |
| `--concurrency [n]` | Max concurrent operations (1-15) |
| `--loop` | Iterative improvement cycles |
| `--iterations [n]` | Set improvement count (1-10) |
| `--validate` | Pre-execution risk assessment |
| `--safe-mode` | Maximum validation |

### Output Flags

| Flag | Purpose |
|------|---------|
| `--uc` / `--ultracompressed` | Token reduction (30-50%) |
| `--scope [file\|module\|project\|system]` | Analysis boundary |
| `--focus [performance\|security\|quality\|architecture]` | Domain focus |

### Flag Priority

1. **Safety First**: `--safe-mode` > `--validate` > optimization
2. **Explicit Override**: User flags > auto-detection
3. **Depth**: `--ultrathink` > `--think-hard` > `--think`
4. **MCP Control**: `--no-mcp` overrides individual MCP flags

## Usage Examples

```bash
# Deep analysis with framework context
/cdf:analyze --think-hard --context7 src/

# Implement with validation
/cdf:implement --validate "Add user dashboard"

# Token-efficient task management
/cdf:task --token-efficient --delegate auto "Refactor auth"

# Safe production build
/cdf:build --safe-mode --validate --focus security

# Expert panel review
/cdf:panel @spec.yml --type spec --mode critique

# Session management
/cdf:session load && [do work] && /cdf:session save --checkpoint
```

## Boundaries

**Will:**
- Display comprehensive command reference
- Explain command categories and usage
- Show available flags and their effects

**Will Not:**
- Execute commands or create files
- Activate implementation modes
- Start projects or tasks

---

**Note:** Commands are 18 total after consolidation (was 30). Run `/cdf:help` for the latest reference.
