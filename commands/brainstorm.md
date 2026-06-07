---
description: "Turn a vague or ambitious idea into a right-sized requirements brief through disciplined Socratic dialogue and premise pressure-testing"
argument-hint: "[idea or problem] [--depth lightweight|standard|deep]"
---

# /cdf:brainstorm - Requirements Discovery

> Answer **WHAT** to build through collaborative dialogue, then write a right-sized requirements brief. Brainstorm precedes `/cdf:plan`, which answers **HOW**.

## Quick Start

```bash
# Explore an idea
/cdf:brainstorm "AI-powered project management tool"

# Force a depth instead of auto-sizing
/cdf:brainstorm "add saved filters to the dashboard" --depth lightweight
/cdf:brainstorm "rethink our onboarding" --depth deep
```

## When to Use

Use `/cdf:brainstorm` when the idea is vague, ambitious, or unscoped and you want to shape *what* to build before *how*. It also fits non-code thinking — a strategy direction, a product bet, a data initiative.

Do not use it when requirements are already concrete (go straight to `/cdf:plan`), to break down a defined task (`/cdf:task --breakdown`), or to execute one (`/cdf:task`). If you open it on something already clear, say so and skip to the handoff rather than manufacturing ceremony.

## Behavioral Flow

### Beat 0 — Size the work, skip if clear

Classify scope from the idea plus a light repo scan, and match ceremony to it:

| Scope | Looks like | Ceremony |
|-------|-----------|----------|
| **Lightweight** | small, well-bounded, low ambiguity | confirm understanding, brief brief (or none) |
| **Standard** | a real feature/decision with open questions | full dialogue + a requirements brief |
| **Deep** | cross-cutting, strategic, or highly ambiguous | full dialogue + premise pressure-test + approaches |

If requirements are **already clear** (acceptance criteria given, pattern to follow named, exact behavior described), do not force a long brainstorm — confirm the understanding and route straight to the handoff. Right-sizing is the point; padding a clear idea with ceremony is the failure mode.

### Beat 1 — Understand the idea

Scan first: search the repo and `docs/solutions/` for anything that already solves part of this, and read relevant `.claude/rules/`. If a claim depends on what exists (a table, an endpoint, a dependency), verify it in the code before asserting it's missing.

Then run a **disciplined dialogue** — see Interaction Rules below. Ask what the user is already thinking before offering your own framings (prevents fixation on AI-generated ideas). Start broad (problem, who it's for, the value) and narrow toward constraints, exclusions, and edge cases.

### Beat 2 — Pressure-test the premise

Before generating approaches, scan the opening for rigor gaps and probe only the ones genuinely present — folded into the dialogue, not fired as a checklist:

- **Evidence** — has anyone actually *done* something about this (paid, built a workaround, quit a tool over it), or is it asserted want?
- **Specificity** — can you name the real person or narrow segment it helps, and what changes for them when it ships?
- **Counterfactual** — what do they do today when this problem hits, and what breaks if nothing ships?
- **Attachment** — what's the smallest version that still delivers real value? (Probe this last, before approaches.)

Keep this light. It sharpens the idea; it does not bulldoze the user's intent. For a full pre-implementation gauntlet (10-dimension founder-mode review, dream-state mapping), defer to the `product-review` skill — this beat is the lightweight, in-dialogue version, not a replacement for it.

### Beat 3 — Explore approaches

If multiple plausible directions remain, propose **2-3 concrete approaches** — each with a one-line description, the key trade-off, and when it's best. Include at least one **non-obvious angle**: inversion (what if we did the opposite?), constraint removal (what if X weren't a limit?), or analogy from another domain. The first ideas are usually variations on one axis.

Present all options *before* recommending — leading with the recommendation anchors the user prematurely. Then state your pick and why, preferring the simpler option unless added complexity buys real value. If one approach is clearly best, skip the menu and say so.

Keep approaches at the level of *mechanism / product shape*, not implementation — column names, file paths, and schemas are `/cdf:plan`'s job, not brainstorm's.

### Beat 4 — Capture a right-sized brief

Write a requirements brief **only when the conversation produced durable decisions worth preserving**. Skip the artifact when brief alignment is enough and the decisions can flow straight into `/cdf:plan`.

When warranted, write to `dev/active/[topic]/[topic]-requirements.md` with: the problem and who it's for, the requirements (what must be true after shipping), scope boundaries (and explicit non-goals), success criteria, and open questions. Keep it **WHAT, not HOW** — no libraries, schemas, or endpoints unless the brainstorm is itself about a technical decision. Write tight: one idea per sentence, no padding a section just because it's present.

### Beat 5 — Hand off

Don't stop at announcing the next step — route there. Offer, via AskUserQuestion: **`/cdf:plan`** (turn this into a grounded plan — the usual next move), **`/cdf:design`** (if it needs technical design first), or **refine further**. Fire the chosen command.

## Interaction Rules

- **One question per turn.** Even when sub-questions feel related, pick the single most useful one. Stacked questions get diluted answers.
- **Default to AskUserQuestion** (the blocking choice tool) for opening, elicitation, and narrowing questions. Well-chosen options scaffold the answer and surface dimensions the user hadn't separated; "Other" keeps it open. Load its schema via ToolSearch (`select:AskUserQuestion`) if needed.
- **Single-select by default.** Use multi-select only for sets that genuinely coexist (goals, constraints, non-goals).
- **Go open-ended only when the question is truly open** — narrative ("walk me through how you got here"), introspective ("what worries you most?" — where a menu would bias the answer), or when you can't write 3-4 distinct real options without strawmen. The rigor probes in Beat 2 are open-ended for this reason. Still one question per turn.

## Output Format

```markdown
## Brainstorm: [topic]

Scope: lightweight | standard | deep
Premise check: [what the pressure-test surfaced, or "no gaps found"]

### Approaches (if multiple)
1. [name] — [mechanism], [key trade-off], best when [...]

Recommendation: [pick + why]

### Requirements brief → dev/active/[topic]/ (if warranted)
- Problem / who it's for:
- Requirements:
- Scope boundaries & non-goals:
- Success criteria:
- Open questions:

### Next
[AskUserQuestion: /cdf:plan | /cdf:design | refine]
```

## Boundaries

**Will:**
- Right-size ceremony to the work, and skip the brainstorm when the idea is already clear
- Run a disciplined one-question-at-a-time dialogue via AskUserQuestion
- Pressure-test the premise before generating solutions
- Produce a WHAT-level requirements brief and hand off to `/cdf:plan`

**Will Not:**
- Make implementation decisions or specify HOW (that is `/cdf:plan`)
- Override the user's vision with prescriptive solutions during exploration
- Pad a clear idea with ceremony, or a brief with sections that carry no content
- Duplicate the full `product-review` gauntlet — this carries only the light, in-dialogue premise probes

## Related Commands

- `/cdf:plan` — turn the requirements into a grounded, structured plan (the usual handoff)
- `/cdf:design` — technical design when the idea needs architecture before planning
- `product-review` skill — heavyweight founder-mode premise + dream-state gauntlet
- `/cdf:task` — execute or break down once the plan exists
