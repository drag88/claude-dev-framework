---
description: "Auto-generate CLAUDE.generated.md from project rules when rules change or are missing"
---

# CLAUDE.md Generator Skill

Auto-generate `CLAUDE.generated.md` from project rules.

## When to Activate

- `.claude/rules/` exists but no `CLAUDE.md` or `CLAUDE.generated.md` in project root
- User asks "generate claude.md" or similar
- User asks "create project documentation"
- After `/cdf:rules generate` completes (auto-chain)

## Actions

1. **Verify rules exist**
   - Check `.claude/rules/` has at least one `.md` file
   - If not, suggest running `/cdf:rules generate` first

2. **Read rule files**
   - `architecture.md` → project name, description, key dirs
   - `tech-stack.md` → language, framework, libraries
   - `commands.md` → setup, test, lint, run
   - `patterns.md` → critical rules

3. **Generate CLAUDE.generated.md**
   - Use WHY/WHAT/HOW framework
   - Keep < 150 lines (Anthropic recommends < 200; first 200 lines are prioritized)
   - Include: Quick Start, Critical Rules, Workflow, Plans Format, Commit Rules, Key Directories
   - Point to `.claude/rules/` for full details
   - Only include instructions that would cause Claude to make mistakes if removed

4. **Inform user**
   - File created at `CLAUDE.generated.md`
   - Review and rename to `CLAUDE.md` if satisfied

## Template Sections

Required sections in generated file:
- Overview (1-2 sentences)
- Quick Start (4-5 bash commands)
- Critical Rules (4 standard rules)
- Workflow (see Workflow Section below)
- Plans Format (plans_instruction block)
- Commit Messages (no attribution rule)
- Project Rules (pointer to .claude/rules/)
- Key Directories (max 5-7 dirs)

## Workflow Section

Include these workflow instructions in every generated CLAUDE.md. These align with official Claude Code best practices from Anthropic.

```markdown
## Workflow

### Explore → Plan → Code → Verify
- Use plan mode for non-trivial tasks (3+ steps or multi-file changes)
- For small fixes (typo, rename, single-file change), skip planning and execute directly
- If something goes sideways, STOP and re-plan — do not push through a broken approach

### Subagent Strategy
- Use subagents for exploration and research to keep main context clean
- One atomic goal per subagent — return summaries, not raw file dumps
- For complex problems, spawn parallel subagents covering different angles
- Main context is for implementation only

### Verification Before Done
- Never mark a task complete without proving it works
- Run tests, check logs, demonstrate correctness
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"

### Autonomous Bug Fixing
- Given a bug report: identify root cause, fix it, add regression test, verify
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user

### Context Management
- Run /clear between unrelated tasks
- Use /compact when context grows large
- After 2 failed corrections on the same issue, clear context and restart with a better prompt
```

**What NOT to include in the Workflow section:**
- File-based task tracking (tasks/todo.md) — Claude has built-in task tools
- File-based lessons (tasks/lessons.md) — Claude has auto-memory at `~/.claude/projects/*/memory/`
- "Demand Elegance" or subjective quality guidance — self-evident, not actionable
- Anything Claude can infer from reading the codebase

## Related Commands

- `/cdf:rules claudemd` - Manually trigger generation
- `/cdf:rules generate` - Regenerate rules (auto-chains to claudemd)
