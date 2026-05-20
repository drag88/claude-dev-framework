# AGENTS.md Best Practices for Codex (GPT-5.5)

Source-backed guidance for writing and auditing `AGENTS.md` files for OpenAI Codex CLI. Use this reference when `/cdf:rules agentsmd` runs, or when opportunistically reviewing a Codex setup. Companion to `claudemd-4-7-rulebook.md`.

## What is AGENTS.md

A flexible Markdown file Codex CLI (and 20+ other coding agents — Cursor, Aider, Jules, Devin, Zed, GitHub Copilot, VS Code) load as project context. Not required. No canonical schema. Functions as "a README for agents."

Source: https://agents.md/ ; https://developers.openai.com/codex/guides/agents-md ; https://github.com/openai/codex/blob/main/docs/agents_md.md

## How Codex loads AGENTS.md

Codex builds the instruction chain in this order:

1. **Global** — `$CODEX_HOME/AGENTS.md` (defaults to `~/.codex/AGENTS.md`). Loads on every session.
2. **Cascading project files** — walks from the Git project root down to the current working directory. At each directory, checks for `AGENTS.override.md` first, then `AGENTS.md`, then the fallback names listed in `project_doc_fallback_filenames`.
3. **Concatenation** — all discovered files concatenate in order (root → cwd). Deeper files appear later in the prompt, so they win because the model weights recent context more.
4. **Size cap** — combined file size hard-caps at `project_doc_max_bytes` (default 32 KiB). Once the cap is hit, no further files load.

When Codex runs from `packages/api/`, the chain loads: `~/.codex/AGENTS.md` + `repo-root/AGENTS.md` + `repo-root/packages/api/AGENTS.md`. Running from repo root only loads the first two.

## What changes vs CLAUDE.md authoring

Four differences that directly affect the file format:

1. **No `@file` imports.** Codex does not expand `@README.md` or `@docs/architecture.md` the way Claude Code does. References are parsed as literal text. Either inline the content you need, or accept that the reference becomes a pointer-only string with no inlined expansion.
2. **No XML tag semantics.** `<use_parallel_tool_calls>...</use_parallel_tool_calls>` is plain text in Codex. The Anthropic-specific tag does not change Codex behavior. Use prose authorization instead.
3. **Nested AGENTS.md replaces path-scoped rules.** Claude Code uses `paths:` frontmatter in `.claude/rules/*.md` to load topic files on demand. Codex achieves the same effect through directory-scoped `AGENTS.md` files. For polyglot monorepos, put per-package conventions in `packages/<name>/AGENTS.md`.
4. **Override file for overlay rules.** `AGENTS.override.md` takes precedence over `AGENTS.md` at the same directory level. Use it for personal or branch-specific overlays that should not ship to the team.

## Authoring rules (apply in this order)

### Structure and size

1. **Target under 60 lines per file.** Codex sessions are token-sensitive; GPT-5.5 is more token-efficient than Opus, which means practitioners run longer sessions and every byte of instruction reload compounds. The hard ceiling is 32 KiB combined across the whole chain.
2. **Open with a one-sentence project role.** Same as CLAUDE.md. "You are a senior TypeScript engineer working on a Next.js SaaS that ..." Anchors tone and scope cheaply.
3. **Inline what CLAUDE.md would import.** If you need a README summary, write the 2-3 sentences directly. Do not write `@README.md`.
4. **Push topic-specific rules into nested `AGENTS.md`.** Per-package conventions belong in `packages/<name>/AGENTS.md`, not crammed into root. Codex loads them only when cwd is inside that package.

### Rule framing

5. **Frame rules as positive imperatives.** "Use X" beats "Never Y." Codex examples in the wild use both styles, but positive framing avoids reverse-psychology failures on any model.
6. **State scope explicitly on every rule.** "Apply to every API handler, including the legacy v1 routes" beats "apply to handlers."
7. **Write concrete, verifiable instructions.** "Run `pnpm test` before committing" beats "test your changes."
8. **Provide the why behind constraints.** "Use Helvetica because react-pdf has no Unicode font" beats a bare "use Helvetica." Lets the model generalize correctly to edge cases.
9. **Use neutral imperatives, not CAPS / MUST / CRITICAL.** Same reasoning as CLAUDE.md — forceful negatives cause overcompliance.

### Host-neutral tool language

10. **Avoid Claude-specific tool names.** Do not reference `Task tool`, `TeamCreate`, `Agent tool`, or other Claude Code APIs that Codex does not expose. Use neutral terms: "subagent", "parallel investigation", "command prompt".
11. **Authorize parallel work in plain prose.** Instead of the `<use_parallel_tool_calls>` XML block, write: "Run independent commands in parallel when fanning out across items, reading multiple files, or running independent investigations."
12. **Reference commands by prompt name, not slash dispatch.** Codex slash-command UX varies by host. Phrase as "Reach for the `/cdf:troubleshoot` prompt when ..." rather than "Run /cdf:troubleshoot" — both work, but the prompt-name framing survives hosts that lack slash dispatch.

### Verification and reporting

13. **Make verification gates concrete commands.** "Run `pnpm typecheck && pnpm test` and paste the output" beats "make sure things pass." Codex self-filters less than Opus 4.7 but still benefits from explicit gates.
14. **Report everything, filter later, for coverage tasks.** Same as 4.7. Words like "be conservative" cause silent drops in any modern coding agent.

### Deprecated patterns

15. **No `@file` syntax.** Codex parses these literally.
16. **No XML-tagged sections** that rely on the host treating the tag specially. Wrap with `##` headers and prose instead.
17. **No multi-turn drip-feed style guidance.** Same as 4.7. AGENTS.md is durable context loaded once.
18. **No API-parameter scaffolding** (temperature, top_p, prefills) — these do not belong in any agent-instructions file.

## Sync with CLAUDE.md

CDF treats `.claude/rules/` as the single source of truth. `/cdf:rules claudemd` and `/cdf:rules agentsmd` each generate a host-tailored output file from the same source.

**Shared content** (regenerated identically into both files):
- Role
- Overview
- Quick Start (commands work in both hosts, or the host's invocation is substituted in place)
- Critical Rules (6-rule core from `commands/rules.md`)
- Project-Specific Notes
- Key Directories

**Diverging content** (regenerated differently for each host):

| Element | CLAUDE.md | AGENTS.md |
|---------|-----------|-----------|
| Imports | `@README.md` | inlined 2-line summary, or omitted |
| Parallel-call authorization | `<use_parallel_tool_calls>` XML block | one-sentence prose authorization |
| Subagent vocabulary | "Task tool", "TeamCreate", "Agent tool" | "subagent", "parallel investigation", "host skill" |
| Tool routing block | "CDF tools available" with Claude tool refs | same block, with neutral tool language |
| Size target | 80-120 lines | under 60 lines |
| Topic-specific overflow | `.claude/rules/*.md` with `paths:` frontmatter | nested `<subdir>/AGENTS.md` |

When `/cdf:rules generate` runs, it auto-chains to both generators. Diffs between the two outputs are expected only in the diverging-content rows above. Anything else that diverges is a generator bug.

## Audit checklist (yes/no)

Run these against any AGENTS.md.

1. Is each file under 60 lines? Is the chain under 32 KiB combined?
2. Does it open with a one-sentence project role?
3. Are there any `@file` imports that Codex will not expand?
4. Are there `<xml_tag>` blocks that Codex parses as plain text?
5. Are there references to Claude-specific tools (`Task tool`, `TeamCreate`, `Agent tool`)?
6. Are rules framed as positive imperatives with explicit scope and the why?
7. Are verification gates concrete commands rather than vague aspirations?
8. Are topic-specific conventions in nested `AGENTS.md` files rather than crammed into root?
9. Is forceful language (CAPS, MUST, CRITICAL) tuned down to neutral imperatives?
10. Is the file in sync with CLAUDE.md on shared content (Role, Overview, Quick Start, Critical Rules, Notes, Directories)?

## Recommended skeleton

Target 40-60 lines.

```markdown
# <Project Name>

## Role
One sentence. Anchors tone and scope.

## Overview
One or two sentences. What the project is.

## Quick Start
```bash
codex                          # launch Codex in this repo
/cdf:rules generate            # regenerate project rules
/cdf:test                      # run tests
```

## Critical Rules
1. Read before edit — understand the full context before changing anything.
2. Search before write — run `rg` or `grep` to find existing implementations.
3. Delete deprecated code immediately — no backwards-compat shims.
4. Tests required — every feature ships with a test.
5. Surface conflicts, don't average them — pick the more recent/tested pattern, explain why.
6. Fail loud — "completed" is wrong if any step was skipped.

## Tool and subagent policy
Run independent commands in parallel when fanning out across items, reading multiple files, or running independent investigations. Skip fan-out for single-file edits or trivial reads.

## CDF tools available
- Debugging — `/cdf:troubleshoot` prompt
- Pre-PR check — `/cdf:verify --mode pre-pr`
- Tests — `/cdf:test`, or `/cdf:tdd` for RED-GREEN-REFACTOR
- Multi-file investigation — `/cdf:task` with codebase-navigator
- Refactoring — `/cdf:improve`
- Commit / ship — `/cdf:git`, `/cdf:ship`

## Commit Messages
Conventional format (`feat:`, `fix:`, `docs:`), no AI attribution.

## Key Directories
- `commands/` — slash command prompts
- `agents/` — specialized agent personas
- `skills/` — auto-invoked skill directories
- `scripts/` — lifecycle and analysis scripts
- `rules-templates/` — rule generation templates
```

## Sources

- AGENTS.md spec — https://agents.md/
- OpenAI Codex CLI AGENTS.md guide — https://developers.openai.com/codex/guides/agents-md
- OpenAI Codex source docs — https://github.com/openai/codex/blob/main/docs/agents_md.md
- Codex vs Claude Code authoring comparison — https://www.mindstudio.ai/blog/codex-agents-md-vs-claude-code-claude-md-comparison

This rulebook is the operational pass on the Codex AGENTS.md docs. The docs are the canonical source.
