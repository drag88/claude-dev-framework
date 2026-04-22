# CLAUDE.md Best Practices for Claude Opus 4.7

Source-backed guidance for auditing and writing CLAUDE.md files for Opus 4.7. Use this reference when running the `/prompt47` skill in `audit-claudemd` mode or when opportunistically flagging CLAUDE.md issues during a normal prompt-optimization run.

## What changed in 4.7 that affects CLAUDE.md

Opus 4.7 differs from 4.6 in five ways that directly change how CLAUDE.md should be written:

1. **More literal interpretation.** It will not silently generalize an instruction or infer a request you did not make.
2. **Lower default tool / subagent use.** It calls tools less often and spawns fewer subagents unless explicitly authorized.
3. **Stronger default aesthetics.** Generic negations ("don't use X style") shift it from one default to another, not to variety.
4. **Deep reasoning every turn.** Multi-turn drip-feed of context is wasteful and hurts quality.
5. **Self-filters findings before reporting.** "Be conservative" or "only flag important" silently drops real issues. This matters for code-review-style instructions in CLAUDE.md.

CLAUDE.md files written for 4.6 mostly still work, but each of these shifts has a corresponding authoring change.

## Verified rules (apply in this order)

### Structure and length

1. **Keep CLAUDE.md under 200 lines per file.** Longer files burn context and reduce adherence. Split topic-specific rules into `.claude/rules/*.md` with `paths:` frontmatter so they only load when matching files are touched. (Anthropic memory docs)

2. **Open with a one-sentence project role.** "You are a senior TypeScript engineer working on a Next.js SaaS that..." Anchors tone and scope cheaply.

3. **Use XML tags only for grouped, non-trivial sections.** Wrap aesthetics, tool policy, or forbidden-words lists with `<frontend_aesthetics>...</frontend_aesthetics>` style tags when they have internal structure. Do not wrap every section.

4. **Use `@path/to/file` imports rather than duplicating content.** Imports expand inline at launch (max five hops). Reference an existing README, package.json, or architecture doc instead of restating it.

5. **Match prompt style to desired output style.** If you want plain prose answers, write CLAUDE.md mostly in prose. If you want bulleted output, use bullets.

### Rule framing

6. **Frame rules as positive instructions, not prohibitions.** "Use X" beats "Never Y." 4.7 wastes tokens on "don't" rules and can pattern-match into them via reverse-psychology.

7. **State scope explicitly on every rule.** "Apply to every component, including third-party wrappers" beats "apply to components." 4.7 will not silently generalize.

8. **Write concrete, verifiable instructions.** "Use 2-space indentation" beats "format code properly." (Anthropic memory docs, official example)

9. **Provide the why behind constraints.** "Never use ellipses because the response is read aloud by a text-to-speech engine" beats a bare "no ellipses." 4.7 generalizes correctly from explained constraints.

10. **Use neutral imperatives, not CAPS / MUST / CRITICAL.** Forceful negative imperatives cause overcompliance and hostile reading on 4.7. "Use this tool when..." beats "CRITICAL: You MUST use this tool when..."

11. **Front-load action verbs over hedges.** "Run X, then Y" beats "consider running X." 4.7 will literally just suggest if you ask it to suggest.

### Tool and subagent policy

12. **Explicitly authorize subagent fan-out.** 4.7 spawns fewer subagents by default. State when to fan out: "Spawn multiple subagents in the same turn when fanning out across items or reading multiple files."

13. **Explicitly authorize tool use for scenarios that benefit from it.** 4.7 calls tools less by default. State the trigger: "Use [tool] when reasoning about X" rather than relying on inference.

14. **Authorize parallel tool calls explicitly.** Anthropic provides a `<use_parallel_tool_calls>` snippet that pushes parallel-call success near 100%. Include it (or close to it) when you want concurrent reads.

15. **Avoid "if in doubt, use [tool]" / "default to [tool]."** Caused undertriggering pre-4.5 and now causes overtriggering. 4.7 already reasons about tool choice.

### Verification and reporting

16. **Make verification gates concrete commands, not aspirations.** "Run `npm test` and paste the output" beats "make sure tests pass." 4.7 self-filters, so vague checks get skipped silently.

17. **For coverage tasks, instruct "report everything, filter later."** Words like "be conservative" or "only flag important issues" cause silent drops on 4.7. Use: "Report every issue you find, including low-severity and uncertain ones. Include confidence and severity. Do not filter at this stage."

18. **Delete forced interim-progress scaffolding.** "After every 3 tool calls, summarize" is redundant with 4.7's native progress updates and burns tokens.

### Design / aesthetics

19. **Specify a concrete palette and typography for design work.** "Use #0D1B2A navy + #E8A838 amber + Inter at 14px base" beats "don't use the default cream + serif look." Negation shifts 4.7 to another fixed default.

### Hierarchy and conflicts

20. **Audit for conflicts across files.** If two files give different guidance for the same behavior, 4.7 may pick one arbitrarily. Periodically diff project CLAUDE.md, nested CLAUDE.md, `.claude/rules/`, and `~/.claude/CLAUDE.md`.

21. **Reserve `.claude/rules/` for human-curated standards. Let auto-memory handle ephemeral learnings.** Instructing Claude to write its own rules into `.claude/rules/` after every correction creates rule sprawl and conflict. Auto-memory at `~/.claude/projects/<project>/memory/` already exists for that.

### Deprecated patterns

22. **Do not include API parameter scaffolding (temperature, top_p, prefills).** 4.7 returns 400 on these. Strip any guidance that mentions them.

23. **Do not include multi-turn drip-feed style guidance.** "We will discuss the spec turn by turn" hurts both efficiency and quality. CLAUDE.md is durable context loaded once.

## Anti-patterns to flag

When auditing, look for these patterns and propose fixes:

| Anti-pattern | Why it hurts 4.7 | Fix |
|---|---|---|
| Walls of "Never X" prohibitions | Reverse-psychology + literal interpretation; 4.7 may echo the list back | Rewrite as positive "Use Y" examples |
| "Be conservative / only flag important" | Silent drops in coverage tasks | "Report everything, filter downstream" |
| Forced interim summaries | Redundant with native progress; burns tokens | Delete |
| "If in doubt, use [tool]" | Overtriggers; 4.7 already reasons about tools | Replace with specific trigger conditions |
| Vague aesthetic guidance ("clean, modern, minimal") | Pushes 4.7 from one default to another | Specify exact palette / typography / spacing |
| CRITICAL / MUST / ALL CAPS | Causes overcompliance and hostile reading | Use neutral imperatives |
| Implicit scope ("apply to components") | 4.7 will not generalize | "Apply to every X, including Y" |
| Untouched auto-generated CLAUDE.md from `/init` | Boilerplate no human reviewed | Hand-curate or delete sections |
| Code style rules that an autoformatter handles | Wastes context | Move to lint/prettier; remove from CLAUDE.md |
| Multi-turn drip-feed style guidance | Hurts efficiency and quality | Front-load |

## Audit checklist (yes/no)

Run these against any CLAUDE.md. Each "no" is a candidate fix.

1. Is the file under 200 lines (excluding imports)?
2. Does it open with a one-sentence project role / identity statement?
3. Are there any "Never X" rules that could be rewritten as "Always Y" or shown as a positive example?
4. Do rules with implicit scope ("apply to components") explicitly say "every component" or name the directory?
5. Is there forced-progress scaffolding ("summarize every N tool calls") that can be deleted?
6. Are there "be conservative / only flag important" instructions that silently filter findings?
7. Are tool use and subagent fan-out explicitly authorized in their own block?
8. Is there a `<use_parallel_tool_calls>` style block (or equivalent) for parallel execution?
9. Are forceful imperatives (CRITICAL, MUST, ALL CAPS) tuned down to neutral imperatives?
10. Are concrete examples ("Use 2-space indentation") used instead of vague directives ("format properly")?
11. Do constraints include the why (so 4.7 can generalize correctly)?
12. Are topic-specific rules (testing, API, frontend) in `.claude/rules/*.md` with `paths:` frontmatter rather than crammed into root CLAUDE.md?
13. Are there conflicts between project CLAUDE.md, nested CLAUDE.md, `.claude/rules/`, and `~/.claude/CLAUDE.md`?
14. Are verification gates explicit ("run `npm test` and paste output") rather than implicit ("make sure tests pass")?
15. Are deprecated API knobs (temperature, top_p, prefills) absent from any guidance about how to call Claude?
16. Are imports (`@README`, `@package.json`) used to avoid duplicating long static content?
17. Does the file avoid auto-generated boilerplate that no human has reviewed?

## Recommended skeleton

Target 100 to 180 lines including blank lines. Anything longer should be split into `.claude/rules/`.

```markdown
# <Project Name> — <one-line identity>

## Role
One sentence describing what kind of collaborator Claude is on this project. Anchors tone and scope.

## Quick start
Five to ten copy-pasteable commands: install, dev, test, lint, type-check, build.

## Architecture (one screen)
A bird's-eye paragraph plus a directory map. For depth, link out: `See @docs/architecture.md`.

## Rules
Positive imperatives only, each with explicit scope and (where non-obvious) the why.
Group by domain with `###` subheaders. Five to fifteen rules at the root level.
Move topic-specific rules to `.claude/rules/`.

## Tool and subagent policy
Explicitly authorize tool use, subagent fan-out, and parallel calls.
State when NOT to spawn subagents (single-file edits, trivial reads).

<use_parallel_tool_calls>
For maximum efficiency, whenever you perform multiple independent operations,
invoke all relevant tools simultaneously rather than sequentially.
</use_parallel_tool_calls>

## Verification gates
Concrete commands the assistant must run before marking work done
(npm test, tsc --noEmit, screenshot diff). Frame as steps, not aspirations.

## Voice and style
For user-facing copy: short positive examples. If you must list forbidden words,
keep it tight and pair each with a preferred alternative.

## Imports
@README.md
@docs/architecture.md

## What lives elsewhere
- Topic rules: `.claude/rules/*.md` (path-scoped, load on demand)
- Ephemeral learnings: auto-memory at `~/.claude/projects/<project>/memory/`
- Personal/local: `CLAUDE.local.md` (gitignored)
```

## Audit output format

When the skill runs in `audit-claudemd` mode, return:

1. **Summary line** — total findings, broken down by severity (high / medium / low). Severity:
   - **High** — silently drops information (rule 17), conflicts with another file (rule 20), or includes deprecated API knobs (rule 22).
   - **Medium** — wastes tokens, causes mild overcompliance, or violates positive-framing rules.
   - **Low** — stylistic or future-proofing.

2. **Findings table** — for each issue:
   - Line number range in the audited file
   - The exact text of the offending passage (quoted, truncated to ~80 chars)
   - Which rule it violates (number from this doc)
   - Severity
   - Suggested rewrite (concrete, copy-pasteable)

3. **Suggested patch** — a unified diff or before/after blocks the user can apply directly. Group related rewrites.

4. **What to leave alone** — call out sections that are already 4.7-aligned, so the user does not over-edit.

5. **Optional: split recommendations** — if the file is over 200 lines, propose which sections move to `.claude/rules/<topic>.md` with `paths:` frontmatter.

## Sources

- Anthropic, "What's new in Claude Opus 4.7" — `platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-7`
- Anthropic, "Migration guide" — `platform.claude.com/docs/en/about-claude/models/migration-guide`
- Anthropic, "Prompting best practices" — `platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices`
- Anthropic, "How Claude remembers your project" — `code.claude.com/docs/en/memory`
- HumanLayer, "Writing a good CLAUDE.md" — `humanlayer.dev/blog/writing-a-good-claude-md`
- claudefa.st, "Claude Opus 4.7 Best Practices" — `claudefa.st/blog/guide/development/opus-4-7-best-practices`
