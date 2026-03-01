# Project Memory Skill

Persistent, project-scoped memory that automatically logs session activity, decisions, and learnings for future context recall.

## When to Activate

- **SessionStart**: Initialize memory structure, load relevant context
- **During Session**: Log significant events (file changes, decisions, discoveries)
- **SessionEnd**: Summarize session to daily log, update long-term memory
- **On Request**: When user asks about past work, decisions, or context

## Memory Structure

Each project gets daily activity logs in `.claude/memory/`:

```
.claude/memory/
└── daily/
    ├── 2026-01-30.md      # Today's session log
    └── 2026-01-29.md      # Previous days
```

**Memory Split**: CDF hooks manage `.claude/memory/daily/` only (file mutation logs). Semantic memory — decisions, patterns, architectural context — lives in Claude's native auto-memory at `~/.claude/projects/<project-key>/memory/MEMORY.md`. Do not conflate the two.

## File Formats

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

## Actions

### On Session Start

1. **Initialize Structure**
   - Create `.claude/memory/` if missing
   - Create daily/ directory if missing

2. **Load Context (Progressive Disclosure)**
   - Claude's native auto-memory provides long-term context automatically
   - Read today's daily log if exists
   - Read yesterday's log for continuity

3. **Inject Context → `.claude/rules/memory-context.md`**
   - Claude auto-loads this file at session start
   - Uses progressive disclosure to prioritize:
     - **Level 1 (Critical)**: Open TODOs, Known Issues
     - **Level 2 (Recent)**: Yesterday's summary, Today's activity
     - **Level 3 (Background)**: Key decisions
   - Keeps context concise to preserve token budget
   - Points to full memory files for deep dives

### Progressive Disclosure Hierarchy

```
Priority 1 (Always shown):
├── 🎯 Open TODOs (max 5)
└── ⚠️ Known Issues

Priority 2 (Recent context):
├── 📅 Yesterday's Summary
└── 🕐 Recent Activity (today, last 10)

Priority 3 (Background):
└── 📋 Key Decisions

Footer:
└── Pointer to full memory files
```

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

3. **Update Long-term Memory (Claude's responsibility)**
   - Claude saves patterns, decisions, and issues to native auto-memory (`~/.claude/projects/<project-key>/memory/MEMORY.md`)
   - CDF hooks do not write to auto-memory — this is Claude's domain

## Memory Recall

### Automatic Recall
At session start, automatically surface:
- Recent activity summary (last 2-3 days)
- Open TODOs or follow-ups
- Relevant context based on current directory/files

### On-Demand Recall
When user asks about past work:
1. Search daily logs for relevant entries
2. Check Claude's auto-memory (`~/.claude/projects/<project-key>/memory/MEMORY.md`) for decisions, patterns, and high-level context

### Search Patterns
- "What did we do yesterday?" → Read daily/[yesterday].md
- "Why did we choose X?" → Search auto-memory for decisions and rationale
- "What's the status of Y?" → Search daily logs for Y
- "Any issues with Z?" → Check auto-memory for known issues

## Integration with Other Skills

### With continuous-learning
- Patterns extracted go to Claude's native auto-memory
- Memory provides historical context for pattern recognition

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

1. **Keep Auto-Memory Curated**
   - Claude's native auto-memory (`~/.claude/projects/<project-key>/memory/MEMORY.md`) is Claude's responsibility
   - Only persistent, valuable knowledge — not a dump of everything
   - Claude reviews and prunes periodically

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
