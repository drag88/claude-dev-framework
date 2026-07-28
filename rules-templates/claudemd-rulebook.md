# CLAUDE.md Best Practices for Current Claude Models

Source-backed guidance for auditing and writing CLAUDE.md files for the current Claude
generation (Claude 5 family and later). This is the authoritative rulebook the CDF generators
read at generation time (`/cdf:rules`, claudemd-generator). Supersedes the retired
`claudemd-4-7-rulebook.md`.

## What changed in the Claude 5 generation that affects CLAUDE.md

Anthropic removed over 80% of Claude Code's own system prompt for Claude 5 models with no
measurable loss on coding evals. The failure mode flipped: older models under-delivered and
needed rules and authorization; current models over-deliver and need judgement framing,
expressive interfaces, and the facts they cannot infer. Five shifts change how CLAUDE.md
should be written:

1. **Rules → judgement.** Worst-case guardrails ("NEVER write comments") are wrong for a
   subset of prompts and now degrade output. State the principle instead ("write code that
   reads like the surrounding code").
2. **Examples → interfaces.** Few-shot tool-use examples constrain the exploration space.
   Expressive parameter names, enums, and tight descriptions teach usage better.
3. **Upfront → progressive disclosure.** CLAUDE.md loads every session; it should carry only
   what every session needs. Detail moves to skills and referenced files loaded on demand.
4. **Repetition → one home per fact.** Duplicated instructions drift and eventually conflict;
   conflicts force the model to deliberate or guess on every task.
5. **Manual memory → auto-memory.** Instructions to hand-maintain notes in CLAUDE.md are
   obsolete; auto-memory owns ephemeral, per-user, time-bound learnings.

## Verified rules (apply in this order)

### Structure and length

1. **Keep CLAUDE.md under 200 lines per file; aim for 60–80.** Longer files burn context and
   reduce adherence. Split topic-specific rules into `.claude/rules/*.md` with `paths:`
   frontmatter so they load only when matching files are touched. What counts is the
   **auto-loaded total** (root + rules + user-level), not the root file alone.

2. **Open with a one-sentence project role.** "You are a senior TypeScript engineer working on
   a Next.js SaaS that..." Anchors tone and scope cheaply.

3. **Spend the tokens on gotchas, not the obvious.** Briefly say what the repo is, then record
   only what the model cannot learn by looking: invariants, traps, incident-derived knowledge,
   house conventions. Never restate what `ls`, `package.json`, or the code itself shows.

4. **Use `@path/to/file` imports rather than duplicating content.** Reference an existing
   README, package.json, or architecture doc instead of restating it.

5. **Use XML tags only for grouped, non-trivial sections.** Do not wrap every section.

6. **Match prompt style to desired output style.** Prose begets prose; bullets beget bullets.

### Rule framing

7. **Frame rules as positive instructions with the why.** "Use parameterized queries —
   interpolating user input into SQL is an injection" beats "NEVER concatenate SQL." Models
   generalize correctly from explained constraints.

8. **State scope explicitly on non-obvious rules.** "Apply to every component, including
   third-party wrappers" beats "apply to components."

9. **Write concrete, verifiable instructions.** "Use 2-space indentation" beats "format code
   properly" — but if a formatter enforces it, replace the rule with "run the lint fix script."

10. **Use neutral imperatives, not CAPS / MUST / CRITICAL.** Forceful emphasis causes
    overcompliance and hostile reading. Reserve hard absolutes for genuinely unacceptable
    worst cases: security boundaries, secrets, destructive or irreversible operations.

11. **Keep hard rules only where violation is truly costly.** Everything else becomes
    judgement framing or gets deleted — if the model would infer it anyway, delete it.

### Tooling

12. **Do not add tool/subagent authorization boilerplate.** `<use_parallel_tool_calls>`
    blocks, "default to subagents," "explicitly authorize tool use" — the harness and current
    models handle all of this natively. Deleting these sections is the upgrade.

13. **Instructions about a tool or skill live in that tool or skill's description, once.**
    Not in CLAUDE.md, not repeated at the end of the file "so the model sees it."

14. **No tool-use few-shot examples.** Design the interface instead: an enum of
    `pending | in_progress | completed` plus one line of intent teaches more than three
    worked transcripts.

### Verification and reporting

15. **Make verification gates concrete commands, not aspirations.** "Run `npm test` and paste
    the output" beats "make sure tests pass."

16. **For coverage tasks, instruct "report everything, filter later."** "Be conservative" or
    "only flag important issues" silently drops real findings.

17. **Never instruct the model to echo or explain its internal reasoning in output.**
    "Show your thinking" style lines can trigger the reasoning-extraction refusal on current
    models. Asking for evidence-backed justification is fine; asking to reveal the thinking
    process is not.

18. **Delete forced interim-progress scaffolding.** "Summarize every N tool calls" burns
    tokens and duplicates native progress behavior.

### Design / aesthetics

19. **Specify a concrete palette and typography for design work.** Negation ("don't use the
    default look") shifts the model from one fixed default to another; only concrete direction
    (or a propose-then-build step) produces variety.

### Hierarchy and conflicts

20. **Audit for conflicts across files and layers.** If CLAUDE.md, a rules file, a skill, and
    a tool description disagree, the model picks one arbitrarily — per task. Cross-layer
    conflicts are the highest-value findings in any audit. One instruction, one home.

21. **Reserve `.claude/rules/` for human-curated standards; let auto-memory handle ephemeral
    learnings.** Never instruct the model to write its own rules there.

### Deprecated patterns

22. **No API parameter scaffolding** (temperature, top_p, prefills) in guidance about calling
    Claude — current models reject these.

23. **No multi-turn drip-feed guidance.** CLAUDE.md is durable context loaded once;
    front-load it.

## Anti-patterns to flag

| Anti-pattern | Why it hurts | Fix |
|---|---|---|
| Walls of "Never X" prohibitions | Encodes preference as constraint; degrades judgement | Rewrite as the principle, or delete |
| "Be conservative / only flag important" | Silent drops in coverage tasks | "Report everything, filter downstream" |
| `<use_parallel_tool_calls>` / subagent-authorization blocks | Harness-native now; pure token cost | Delete |
| Tool-use few-shot examples | Constrain exploration | Expressive parameters + one line of intent |
| "Show your thinking / explain your reasoning" | Reasoning-extraction refusal risk | Ask for evidence, not process |
| Same fact in two auto-loaded files | Copies drift into conflicts | One home per fact |
| CRITICAL / MUST / ALL CAPS | Overcompliance, hostile reading | Neutral imperatives; absolutes only for real dangers |
| Codemaps, command lists, test inventories mirroring the repo | Derivable; goes stale | Pointer + only the non-derivable annotations |
| Forced interim summaries / progress rituals | Redundant with native behavior | Delete |
| "Save learnings to CLAUDE.md" | Auto-memory owns this | Delete |
| Vague aesthetic guidance ("clean, modern") | Swaps one default for another | Concrete palette/type, or propose-then-build |
| Untouched auto-generated boilerplate | No human reviewed it | Hand-curate or delete |
| Code style rules an autoformatter enforces | Wastes context | "Run the lint fix script" |

## Audit checklist (yes/no)

Each "no" is a candidate fix.

1. Is the auto-loaded total (root + rules + user-level) modest, with the root under 200 lines?
2. Does it open with a one-sentence project role?
3. Is every fact stated in exactly one auto-loaded home?
4. Are there conflicts across CLAUDE.md, nested files, `.claude/rules/`, skills, and tool
   descriptions?
5. Are "Never X" rules either genuinely load-bearing (security, data loss, irreversibility)
   or rewritten as principles?
6. Is anything present that the model could derive from the repo (trees, command lists,
   test tables) without an annotation earning its place?
7. Are there leftover authorization blocks (parallel calls, subagent fan-out, tool use)?
   Delete them.
8. Are there tool-use few-shot examples that should become interface descriptions?
9. Are there "show your reasoning" instructions? Strip them.
10. Are verification gates concrete commands with pasted output?
11. Do coverage-style instructions say "report everything, filter later"?
12. Are topic-specific rules path-scoped in `.claude/rules/*.md` rather than crammed into root?
13. Do constraints include the why?
14. Are imports used instead of duplicated static content?
15. Is memory-keeping delegated to auto-memory rather than instructed into CLAUDE.md?

## Recommended skeleton

Target 60–120 lines. Anything longer should be split into `.claude/rules/` or skills.

```markdown
# <Project Name> — <one-line identity>

## Role
One sentence describing what kind of collaborator Claude is on this project.

## Quick start
Five to ten copy-pasteable commands: install, dev, test, lint, build.

## Architecture (one screen)
A bird's-eye paragraph. For depth, link out: `See @docs/architecture.md`.

## Gotchas
The non-obvious only: invariants, traps, incident-derived knowledge, house conventions.
Each with the why. This is the section that earns the file its tokens.

## Rules
Positive imperatives, each with explicit scope and the why where non-obvious.
Five to fifteen at root. Hard absolutes only for security/secrets/irreversible operations.
Topic-specific rules live in `.claude/rules/` (path-scoped).

## Verification gates
Concrete commands to run before marking work done.

## Procedures
Pointers only: deploys `/deploy`, reviews `/review`. Detail lives in the skills.

## What lives elsewhere
- Topic rules: `.claude/rules/*.md` (path-scoped, load on demand)
- Ephemeral learnings: auto-memory
- Personal/local: `CLAUDE.local.md` (gitignored)
```

## Audit output format

When auditing an existing CLAUDE.md, return:

1. **Summary line** — total findings by severity. High = cross-layer conflicts, rules that
   block correct behavior, stale facts an agent would act on. Medium = over-constraint,
   redundancy, always-loaded bulk. Low = style.
2. **Findings table** — line range, quoted text (~80 chars), rule number from this doc,
   severity, and a concrete copy-pasteable rewrite (or "delete" + why safe).
3. **Suggested patch** — before/after blocks the user can apply directly.
4. **What to leave alone** — sections already aligned, so the user does not over-edit.
5. **Split recommendations** — if oversized, which sections move to `.claude/rules/<topic>.md`
   or a skill.

## Sources

- Anthropic, "The new rules of context engineering for Claude 5 models" (Thariq, Claude Code
  team, 2026-07) — x.com/trq212/status/2080710971228918066
- Anthropic, "Prompting Claude Fable 5" —
  `platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5`
- Anthropic, "Prompting best practices" —
  `platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices`
- Anthropic, "Effective context engineering for AI agents" —
  `anthropic.com/engineering/effective-context-engineering-for-ai-agents`
- Anthropic, "How Claude remembers your project" — `code.claude.com/docs/en/memory`
- HumanLayer, "Writing a good CLAUDE.md" — `humanlayer.dev/blog/writing-a-good-claude-md`
