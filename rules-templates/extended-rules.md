# Extended Critical Rules (opt-in)

> **Status:** opt-in reference. CDF's default generator (`/cdf:rules claudemd`) ships a 6-rule Critical Rules section, not this 12-rule set. Import individual rules from here only when you have a project-specific reason. Three rules in the source set are anti-patterns on Claude Opus 4.7 — those are flagged below.

This file is a community 12-rule CLAUDE.md template that has circulated as a starting point. CDF retains it for reference and selective adoption. Each rule below carries a verdict against the [4.7 rulebook](claudemd-4-7-rulebook.md) and the gist's coding-agent best practices ([skills/tuning-coding-agent-codebases/SKILL.md](../skills/tuning-coding-agent-codebases/SKILL.md)).

## Verdict legend

- **Default** — already in CDF's 6-rule Critical Rules section.
- **Keep** — additive, ships in CDF's 6-rule set.
- **Optional** — useful but better placed in a topic-specific rule file (e.g., `testing.md`) rather than root CLAUDE.md.
- **Skip** — duplicates content elsewhere or adds low signal.
- **Reject** — actively harmful on 4.7 (forced summaries, unenforceable budgets, wrong layer).

## The 12 rules with verdicts

### Rule 1 — Think Before Coding *(Skip)*
State assumptions explicitly. If uncertain, ask rather than guess. Push back when a simpler approach exists.

**Why skip:** Duplicates CDF's Critical Rule #1 (Read before edit) and the plan-mode default in `workflow.md`. 4.7 handles ambiguity surfacing natively.

### Rule 2 — Simplicity First *(Skip)*
Minimum code that solves the problem. No abstractions for single-use code.

**Why skip:** Covered by the `simplify` skill, by `workflow.md`'s "Demand Elegance" section, and by the general "don't over-engineer" guidance in CDF's root `CLAUDE.md`.

### Rule 3 — Surgical Changes *(Skip with caution)*
Touch only what you must. Don't refactor what isn't broken. Match existing style.

**Why skip:** The scope-discipline intent is fine, but the phrasing ("don't refactor what isn't broken") overlaps with the gist's old-model-compensating grep (phrase #7: "Do not refactor existing code"). 4.7 doesn't drift into adjacent code the way 3.5 did. Conformance is already implicit in CDF Critical Rule #1.

### Rule 4 — Goal-Driven Execution *(Skip)*
Define success criteria. Loop until verified.

**Why skip:** Vague. 4.7 loops to verification by default. Adds noise without changing behavior.

### Rule 5 — Use the model only for judgment calls *(Reject)*
Use Claude for classification, drafting, summarization, extraction. Do NOT use Claude for routing, retries, deterministic transforms.

**Why reject:** Wrong layer. This is API/system-design guidance about *how an application invokes Claude*, not about Claude's in-session behavior. CLAUDE.md governs the agent inside the session; this rule belongs in the project's architecture doc or service README.

### Rule 6 — Token budgets are not advisory *(Reject)*
Per-task: 4,000 tokens. Per-session: 30,000 tokens. If approaching budget, summarize and start fresh.

**Why reject:** The model cannot observe token counts mid-turn. 4.7's context window is 1M tokens; a 30K session cap is below normal working size. This rule hallucinates a control surface that does not exist. Token budgets, if enforced, belong in client-side telemetry, not in CLAUDE.md.

### Rule 7 — Surface conflicts, don't average them *(Keep — now CDF Critical Rule #5)*
When two patterns contradict, pick one (more recent / more tested). Explain why. Flag the other for cleanup. Don't blend.

**Why keep:** Genuinely additive. Aligns with 4.7 rulebook rule 20 (audit for conflicts across files). 4.7 will silently average plausible contradictions if not told otherwise.

### Rule 8 — Read before you write *(Default)*
Read exports, immediate callers, shared utilities before adding code.

**Why default:** This is CDF Critical Rule #1.

### Rule 9 — Tests verify intent, not just behavior *(Optional)*
Tests must encode why behavior matters, not just what it does. A test that can't fail when business logic changes is wrong.

**Why optional:** Good design principle but abstract. Better placed in `rules-templates/testing.md` so it loads when test files are touched, not as a root-CLAUDE.md rule.

### Rule 10 — Check after every significant step *(Reject)*
Summarize what was done, what's verified, what's left at every significant step.

**Why reject:** This is the **forced interim summary** pattern. The 4.7 rulebook (rule 18, "Delete forced interim-progress scaffolding") and the gist both flag this as a delete-on-sight pattern. 4.7's native progress updates already cover this. Forced summaries burn tokens and don't improve outcomes.

### Rule 11 — Match the codebase's conventions *(Skip)*
Conformance > taste inside the codebase. If a convention is harmful, surface it.

**Why skip:** Already implicit in CDF Critical Rule #1 (Read before edit) and the `patterns.md` auto-loaded rules.

### Rule 12 — Fail loud *(Keep — now CDF Critical Rule #6)*
"Completed" is wrong if anything was skipped. "Tests pass" is wrong if any were skipped. Default to surfacing uncertainty, not hiding it.

**Why keep:** Genuinely additive. Counters 4.7's mild tendency to declare success when one step was silently bypassed. Pairs with the failure-recovery skill.

## Summary

| Action | Rules |
|--------|-------|
| Already CDF default | 8 |
| Adopted into CDF's 6-rule core | 7, 12 |
| Move to topic file | 9 (→ `testing.md`) |
| Skip (duplicate or low signal) | 1, 2, 3, 4, 11 |
| Reject (anti-pattern on 4.7) | 5, 6, 10 |

## Adoption guidance

Do not paste this entire file into a generated CLAUDE.md. If a project genuinely needs one of the *Skip* rules (for example, a junior team where "Match the codebase's conventions" is load-bearing guidance), copy that single rule into the project's root CLAUDE.md with the *why* attached. Leave the *Reject* rules out — they cost tokens and degrade 4.7's behavior.

## Source

Community-circulated 12-rule template. Annotations are CDF's, based on:
- Anthropic, "What's new in Claude Opus 4.7"
- Anthropic, "How Claude Code works in large codebases" (the gist behind `skills/tuning-coding-agent-codebases`)
- The vendored `claudemd-4-7-rulebook.md` in this directory
