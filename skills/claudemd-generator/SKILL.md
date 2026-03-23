---
name: generating-project-docs
description: "Auto-generates CLAUDE.generated.md from project rules when rules change or are missing"
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
- Workflow (COPY VERBATIM from Workflow Section below — all 8 subsections required)
- Plans Format (plans_instruction block)
- Memory (exactly 2 lines: check auto-memory + save key decisions. NO daily logs, NO session context injection)
- Commit Messages (no attribution rule)
- CDF Agents (use `/cdf:task` NOT `/cdf:spawn` in command column)
- Project Rules (pointer to .claude/rules/)
- Key Directories (max 5-7 dirs)

## Workflow Section

**CRITICAL**: Copy the Workflow section below VERBATIM into every generated CLAUDE.md. Do NOT paraphrase, reorganize, summarize, or omit any subsections. Do NOT replace this with a "Subagent Strategy" standalone section or a table. All 8 subsections below are required exactly as written.

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
- For visual/UI changes: verify in the browser before confirming to the user
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"

### Self-Improvement Loop
- After ANY correction from the user: capture the pattern in `.claude/rules/`
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these rules until mistake rate drops
- Review rules at session start for relevant project

### Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes — don't over-engineer
- Challenge your own work before presenting it

### Autonomous Bug Fixing
- Given a bug report: identify root cause, fix it, add regression test, verify
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user

### Context Management
- Run /clear between unrelated tasks
- Use /compact when context grows large
- After 2 failed corrections on the same issue, clear context and restart with a better prompt

### Core Principles
- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Only touch what's necessary. No side effects with new bugs.
```

## Memory Section

Copy this EXACTLY — no additions, no "daily activity logs", no "session context injection":

```markdown
## Memory
- Check auto-memory for prior context at session start
- Save key decisions, debugging insights, and project patterns to auto-memory during work
```

## CDF Agents Section

Use `/cdf:task` (NOT `/cdf:spawn`) in the Command column for all agents except research, troubleshoot, test, analyze, improve, docs, tdd, e2e which use their specific commands.

## Related Commands

- `/cdf:rules claudemd` - Manually trigger generation
- `/cdf:rules generate` - Regenerate rules (auto-chains to claudemd)
