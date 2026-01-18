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
   - Keep < 100 lines
   - Include: Quick Start, Critical Rules, Plans Format, Commit Rules, Key Directories
   - Point to `.claude/rules/` for full details

4. **Inform user**
   - File created at `CLAUDE.generated.md`
   - Review and rename to `CLAUDE.md` if satisfied

## Template Sections

Required sections in generated file:
- Overview (1-2 sentences)
- Quick Start (4-5 bash commands)
- Critical Rules (4 standard rules)
- Plans Format (plans_instruction block)
- Commit Messages (no attribution rule)
- Project Rules (pointer to .claude/rules/)
- Key Directories (max 5-7 dirs)

## Related Commands

- `/cdf:rules claudemd` - Manually trigger generation
- `/cdf:rules generate` - Regenerate rules (auto-chains to claudemd)
