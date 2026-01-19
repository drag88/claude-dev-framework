---
description: "Session lifecycle management: load context, save progress, reflect on work"
---

# /cdf:session - Session Lifecycle Management

> Unified session management: load context, save progress, reflect on work.

## Quick Start

```bash
# Load project context at session start
/cdf:session load

# Save session before ending work
/cdf:session save --checkpoint

# Reflect on task completion
/cdf:session reflect --type completion

# List available checkpoints
/cdf:session list
```

## When to Use

Use `/cdf:session` when:
- Starting work on a project (load context from previous sessions)
- Ending a work session (save discoveries and create checkpoint)
- Validating task completion (reflect on progress)
- Approaching context limits (save before compaction)

**Don't use this command for**: Creating dev documentation structure (use `/cdf:docs plan` instead).

## Subcommands

### load - Project Context Loading

Load project context and restore session state.

```bash
/cdf:session load [target] [--type project|config|deps|checkpoint] [--refresh] [--analyze]
```

**Behavioral Flow:**
1. **Initialize**: Establish Serena MCP connection and session context
2. **Discover**: Analyze project structure and identify context requirements
3. **Load**: Retrieve project memories, checkpoints, and persistence data
4. **Activate**: Establish project context and prepare for development
5. **Validate**: Ensure loaded context integrity and session readiness

**Examples:**
```bash
# Load current project context
/cdf:session load

# Load specific project with analysis
/cdf:session load /path/to/project --type project --analyze

# Restore from checkpoint
/cdf:session load --type checkpoint --checkpoint session_123

# Load with fresh dependency analysis
/cdf:session load --type deps --refresh
```

### save - Session Context Persistence

Save session context and create recovery checkpoints.

```bash
/cdf:session save [--type session|learnings|context|all] [--summarize] [--checkpoint]
```

**Behavioral Flow:**
1. **Analyze**: Examine session progress and identify discoveries worth preserving
2. **Persist**: Save session context using Serena MCP memory management
3. **Checkpoint**: Create recovery points for complex sessions
4. **Validate**: Ensure session data integrity and cross-session compatibility
5. **Prepare**: Ready context for seamless continuation in future sessions

**Examples:**
```bash
# Basic session save
/cdf:session save

# Complete save with checkpoint
/cdf:session save --type all --checkpoint

# Save with summary generation
/cdf:session save --summarize

# Save only new learnings
/cdf:session save --type learnings
```

### reflect - Task Reflection and Validation

Validate task completion and capture insights.

```bash
/cdf:session reflect [--type task|session|completion] [--analyze] [--validate]
```

**Behavioral Flow:**
1. **Analyze**: Examine current task state and session progress
2. **Validate**: Assess task adherence, completion quality, and requirements
3. **Reflect**: Apply deep analysis of collected information
4. **Document**: Update session metadata and capture learning insights
5. **Optimize**: Provide recommendations for improvement

**Examples:**
```bash
# Validate task adherence
/cdf:session reflect --type task --analyze

# Session progress analysis
/cdf:session reflect --type session --validate

# Completion validation
/cdf:session reflect --type completion
```

### list - List Checkpoints

List available checkpoints for restoration.

```bash
/cdf:session list [--filter recent|all]
```

## MCP Integration

- **Serena MCP**: Mandatory for project activation, memory operations, and session management
- **Memory Operations**: Cross-session persistence, checkpoint loading, context restoration
- **Performance Critical**: <200ms for core operations, <1s for checkpoint creation

## Tool Coordination

| Tool | Purpose |
|------|---------|
| `activate_project` | Core project activation and context establishment |
| `list_memories/read_memory` | Memory retrieval and session context loading |
| `write_memory` | Session context persistence and checkpoint creation |
| `think_about_task_adherence` | Task validation against project goals |
| `think_about_collected_information` | Session analysis and completeness assessment |
| `think_about_whether_you_are_done` | Completion criteria evaluation |
| `summarize_changes` | Session summary generation |

## Boundaries

**Will:**
- Load/save project context using Serena MCP integration
- Create automatic checkpoints based on session progress
- Perform comprehensive task reflection and validation
- Preserve discoveries for enhanced project understanding

**Will Not:**
- Operate without proper Serena MCP integration
- Modify project structure without explicit permission
- Override session context without checkpoint preservation
- Bypass session integrity checks

## Related Commands

- `/cdf:docs plan` - Create strategic planning documentation
- `/cdf:docs update` - Update dev docs before context compaction
