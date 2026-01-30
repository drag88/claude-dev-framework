# Project Memory Skill

Persistent, project-scoped memory that automatically logs session activity, decisions, and learnings for future context recall.

## When to Activate

- **SessionStart**: Initialize memory structure, load relevant context
- **During Session**: Log significant events (file changes, decisions, discoveries)
- **SessionEnd**: Summarize session to daily log, update long-term memory
- **On Request**: When user asks about past work, decisions, or context

## Memory Structure

Each project gets its own memory in `.claude/memory/`:

```
.claude/memory/
├── MEMORY.md              # Long-term curated knowledge
├── daily/
│   ├── 2026-01-30.md      # Today's session log
│   └── 2026-01-29.md      # Previous days
├── decisions/
│   └── ADR-001-*.md       # Architecture Decision Records
└── .index.json            # Search index metadata
```

## File Formats

### MEMORY.md (Long-term Memory)

```markdown
# Project Memory

## Project Overview
[Auto-generated summary of what this project is]

## Key Decisions
- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

## Architecture Notes
[Important architectural context]

## Patterns & Conventions
[Project-specific patterns discovered]

## Known Issues & Workarounds
[Gotchas and their solutions]

## Important Context
[Domain knowledge, business rules, etc.]

---
*Last updated: [timestamp]*
```

### Daily Log (daily/YYYY-MM-DD.md)

```markdown
# [Date] Session Log

## Session Summary
[Brief overview of what was accomplished]

## Changes Made
| File | Change | Reason |
|------|--------|--------|
| path/to/file | Description | Why |

## Decisions Made
- **[Decision]**: [Rationale]

## Issues Encountered
- [Issue]: [Resolution]

## TODO / Follow-up
- [ ] [Item needing attention]

## Raw Activity
[Timestamped log of significant actions]
```

### Architecture Decision Record (decisions/ADR-NNN-*.md)

```markdown
# ADR-NNN: [Title]

**Date**: [Date]
**Status**: [Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the issue we're addressing?]

## Decision
[What did we decide to do?]

## Consequences
[What are the results of this decision?]

## Alternatives Considered
[What other options were evaluated?]
```

## Actions

### On Session Start

1. **Initialize Structure**
   - Create `.claude/memory/` if missing
   - Create MEMORY.md with project overview if missing
   - Create daily/ directory if missing

2. **Load Context**
   - Read MEMORY.md for long-term context
   - Read today's daily log if exists
   - Read yesterday's log for continuity

3. **Inject Context**
   - Provide summary of recent activity
   - Highlight any open TODOs or follow-ups
   - Surface relevant decisions

### During Session

1. **Log Significant Events**
   - File creates/edits with purpose
   - Important decisions and rationale
   - Problems encountered and solutions
   - External integrations or dependencies added

2. **Track Decisions**
   - When architectural choices are made
   - When trade-offs are evaluated
   - When patterns are established

3. **Note Issues**
   - Bugs encountered
   - Workarounds applied
   - Technical debt incurred

### On Session End

1. **Summarize Session**
   - Generate session summary
   - Compile changes made
   - List decisions with rationale

2. **Update Daily Log**
   - Append or create daily log entry
   - Include all tracked events
   - Add follow-up items

3. **Update Long-term Memory**
   - Extract patterns worth remembering
   - Update key decisions if new ones made
   - Add any new known issues/workarounds

## Memory Recall

### Automatic Recall
At session start, automatically surface:
- Recent activity summary (last 2-3 days)
- Open TODOs or follow-ups
- Relevant context based on current directory/files

### On-Demand Recall
When user asks about past work:
1. Search daily logs for relevant entries
2. Check MEMORY.md for high-level context
3. Search decisions/ for architectural context

### Search Patterns
- "What did we do yesterday?" → Read daily/[yesterday].md
- "Why did we choose X?" → Search decisions/ and MEMORY.md
- "What's the status of Y?" → Search daily logs for Y
- "Any issues with Z?" → Check known issues in MEMORY.md

## Integration with Other Skills

### With context-saver
- Memory provides content for session checkpoints
- Context-saver triggers memory summarization

### With continuous-learning
- Patterns extracted go to both learnings/ and MEMORY.md
- Memory provides historical context for pattern recognition

### With external-memory
- Task memory is temporary (dev/memory/)
- Project memory is permanent (.claude/memory/)
- Completed tasks can be summarized to project memory

## Configuration

Optional `.claude/memory/config.json`:

```json
{
  "autoLog": true,
  "logLevel": "normal",
  "dailyRetention": 30,
  "excludePatterns": ["*.log", "node_modules/**"],
  "summarizeOnEnd": true
}
```

### Log Levels
- **minimal**: Only major decisions and blockers
- **normal**: Decisions, significant changes, issues (default)
- **verbose**: All file changes, all commands, detailed notes

## Best Practices

1. **Keep MEMORY.md Curated**
   - Not a dump of everything
   - Only persistent, valuable knowledge
   - Review and prune periodically

2. **Daily Logs are Append-Only**
   - Don't edit past entries
   - Corrections go as new entries
   - Preserves history accurately

3. **Decisions Need Rationale**
   - "What" without "why" is useless
   - Include alternatives considered
   - Note any constraints or trade-offs

4. **Memory is for Context, Not Code**
   - Don't duplicate code in memory
   - Reference file paths instead
   - Focus on intent and reasoning
