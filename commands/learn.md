---
name: learn
description: Universal skill learning system. Captures corrections, views learned preferences, removes entries, resets skills, and consolidates patterns. Use when providing feedback on any skill or managing learned preferences.
---

# /cdf:learn

Universal skill learning command. One command for capture, viewing, removal, and consolidation.

## Usage

```
/cdf:learn "preference or correction"              # Capture (infers skill)
/cdf:learn skill-name "preference or correction"    # Capture (explicit skill)
/cdf:learn status                                   # Overview across all skills
/cdf:learn show skill-name                          # Show entries for a skill
/cdf:learn remove skill-name number                 # Remove specific entry
/cdf:learn reset skill-name                         # Clear all for a skill
/cdf:learn consolidate skill-name                   # Deduplicate and merge
```

## Subcommands

### Capture (default)

`/cdf:learn "preference"` or `/cdf:learn skill-name "preference"`

1. **Determine target skill:**
   - Explicit name provided → use it (validate exists in `skills/`)
   - No name → infer from conversation context (which skill was most recently active)
   - Inference fails → ask: "Which skill?" and list recently active ones
   - No skill applies → log to Claude's auto-memory instead (this command is for skill-specific learning)

2. **Classify into section:**
   - **Do**: Positive instructions ("always X", "prefer X", "use X")
   - **Don't**: Negative instructions ("never X", "avoid X", "stop doing X")
   - **Style**: Tone, format, voice preferences ("be more concise", "use parentheses not dashes")

3. **Write to `skills/{skill-name}/learned.md`:**
   - Create from template if it does not exist
   - Append dated entry: `- {description} (YYYY-MM-DD)`
   - Silent. Do NOT announce that feedback was logged.

4. **Check cap:** If 20+ entries, notify: "Run `/cdf:learn consolidate {skill-name}` to merge."

### Status

`/cdf:learn status`

Scan `skills/*/learned.md` across all skill directories. Show:

```
Learned preferences across skills:

  writing-voice:     9 entries (last updated 2026-03-28)
  coding-standards:  2 entries (last updated 2026-03-25)
  frontend-patterns: (no learned.md)

Total: 11 entries across 2 skills
```

### Show

`/cdf:learn show skill-name`

Display all entries with numbered indices:

```
# writing-voice: 9 learned preferences

## Do
1. Use parenthetical asides for context, not dashes (2026-03-28)
2. Name specific tools over generic descriptions (2026-03-28)

## Don't
3. Never use hyphens, em dashes, or en dashes (2026-03-28)

## Style
4. "More often than not" is a natural qualifier, not clutter (2026-03-28)
```

### Remove

`/cdf:learn remove skill-name number`

Remove a specific numbered entry. Show the entry text, confirm removal, delete the line.

### Reset

`/cdf:learn reset skill-name`

Clear ALL learned preferences for a skill. Confirm first: "This will remove all {N} preferences for {skill-name}. Are you sure?" Replace with empty template on confirmation.

### Consolidate

`/cdf:learn consolidate skill-name`

When `learned.md` grows large (20+ entries):

1. Identify duplicates (same concept, different wording)
2. Identify entries that merge into broader rules
3. Identify contradictions (flag for user decision)
4. Propose consolidated version as a diff
5. Apply only after user approval
6. For skills with reference files (like writing-voice), propose promoting patterns into permanent reference files

## learned.md Template

```markdown
# Learned Preferences: {skill-name}

Corrections and preferences that persist across sessions. Manage via `/cdf:learn`.

## Do
(none yet)

## Don't
(none yet)

## Style
(none yet)
```

## Silent Feedback Protocol (Opt-In Per Skill)

Skills that want automatic learning can include this in their SKILL.md:

```markdown
## Feedback Protocol

When the user corrects output produced by this skill:
1. Apply the correction to the current output
2. Evaluate confidence:
   - HIGH (explicit "always/never", or same correction seen in prior sessions): write to learned.md immediately
   - LOW (single correction, context-specific): note mentally, do NOT write. Wait for repetition.
3. Never announce that feedback was logged
```

## Dynamic Hook Enforcement (Opt-In Per Skill)

Skills enforce learned preferences automatically via scoped hooks in SKILL.md frontmatter. The hook fires once when the skill activates, injecting all learned preferences as `additionalContext`.

### Add to SKILL.md frontmatter (shared script, recommended):

```yaml
hooks:
  PreToolUse:
    - hooks:
        - type: command
          command: "python3 \"$CLAUDE_PLUGIN_ROOT/scripts/inject-skill-learned.py\" \"${CLAUDE_SKILL_DIR}\""
          timeout: 3
          once: true
```

### How enforcement works:

1. Skill activates → Claude loads SKILL.md
2. First tool use triggers the PreToolUse hook
3. Hook reads `learned.md`, extracts Do/Don't/Style entries
4. Returns as `additionalContext` with "MUST follow" preamble
5. `once: true` prevents repeated injection

Capture happens via the Feedback Protocol or explicit `/cdf:learn`. Enforcement happens via the hook. Two halves of the same loop.

## Examples

```
/cdf:learn "never use hyphens or em dashes in output"
→ Infers writing-voice → writes to ## Don't

/cdf:learn coding-standards "prefer guard clauses over nested if/else"
→ Explicit target → writes to ## Do

/cdf:learn status
→ Shows all skills with learned.md counts

/cdf:learn show writing-voice
→ Shows numbered entries

/cdf:learn remove writing-voice 3
→ Removes entry #3
```
