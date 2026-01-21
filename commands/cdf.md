---
description: "Claude Dev Framework - Development framework with commands, agents, skills, and hooks"
argument-hint: "Optional: subcommand (help, implement, analyze, etc.)"
---

# /cdf - Claude Dev Framework

> Complete development framework for intelligent code analysis, generation, and workflow automation.

## Quick Start

```bash
# Show all commands
/cdf:help

# Common workflows
/cdf:implement "add user authentication"    # Build features
/cdf:analyze src/                           # Code analysis
/cdf:rules generate                         # Generate project rules
/cdf:docs "plan refactor"                   # Strategic planning
```

## Available Commands

### Core Development
| Command | Description |
|---------|-------------|
| `/cdf:implement` | Feature implementation with persona activation |
| `/cdf:build` | Build, compile, and package projects |
| `/cdf:test` | Execute tests with coverage analysis |
| `/cdf:git` | Git operations with intelligent commits |
| `/cdf:cleanup` | Clean up code, remove dead code |
| `/cdf:improve` | Systematic code improvements |

### Analysis & Understanding
| Command | Description |
|---------|-------------|
| `/cdf:analyze` | Code analysis (quality, security, performance) |
| `/cdf:explain` | Clear explanations of code and concepts |
| `/cdf:research` | Deep web research |
| `/cdf:troubleshoot` | Diagnose and resolve issues |

### Planning & Design
| Command | Description |
|---------|-------------|
| `/cdf:brainstorm` | Interactive requirements discovery |
| `/cdf:design` | System architecture and API design |
| `/cdf:estimate` | Development effort estimation |
| `/cdf:workflow` | Generate implementation workflows |

### Orchestration
| Command | Description |
|---------|-------------|
| `/cdf:task` | Execute complex tasks with delegation |
| `/cdf:spawn` | Break down complex tasks |
| `/cdf:panel` | Multi-expert panel discussions |

### Utilities
| Command | Description |
|---------|-------------|
| `/cdf:help` | **Full command reference** |
| `/cdf:docs` | Documentation and planning |
| `/cdf:rules` | Project rules generation |
| `/cdf:session` | Session management |
| `/cdf:setup` | View plugin configuration |

## Features

- **22 Commands** - Comprehensive development operations
- **19 Agents** - Specialized expert personas (`@agent-name`)
- **6 Skills** - Auto-invoked contextual behaviors
- **3 Hooks** - Lifecycle automation

## Default Behavior

When invoked without arguments, `/cdf` displays this overview. For the full command reference with flags and examples, use `/cdf:help`.

## Version

v1.5.0 - [Changelog](https://github.com/drag88/claude-dev-framework)
