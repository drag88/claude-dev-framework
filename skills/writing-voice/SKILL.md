---
name: writing-voice
description: Crafts personal writing in Aswin's authentic voice for blogs, LinkedIn, and Twitter/X. Uses editorial pipeline (McPhee, Minto, Zinsser, Forsyth) with voice calibration and platform adaptation. Activates when asked to draft, publish, or post content for blog, LinkedIn, Twitter/X, or social media. Also activates on "tweet this", "post about", "turn this into a post", "make this shareable", "write a post", "help me write". Does NOT activate for code documentation, commit messages, READMEs, technical specs, API docs, SQL queries, or scripts.
hooks:
  PreToolUse:
    - hooks:
        - type: command
          command: "python3 \"${CLAUDE_SKILL_DIR}/scripts/inject-learned.py\""
          timeout: 3
          once: true
---

# Writing Voice

Comprehensive writing framework for crafting authentic content across blog, LinkedIn, and Twitter/X. Combines generative thinking tools with a structured editorial pipeline and agent-based quality review.

## Core Philosophy

Every piece of writing must pass this test: "Would a thoughtful person actually say this to another person over coffee?"

- Lead with genuine curiosity or hard-won insight
- Write as if speaking to one specific person, not a faceless audience
- Let imperfection show — perfect polish reads as artificial
- Substance over signal. Earned authority, not claimed expertise.
- Err toward under-polished and human over smooth and artificial

## Two Modes (Auto-Detected)

### Fast Path
**When:** Tweets, short LinkedIn posts (<400 words), quick reactions.

1. Anchor to nearest core belief from `references/voice-and-beliefs.md` (skip if none obvious)
2. Select generative method from `references/generative-methods.md` (Compression for tweets, any for LinkedIn)
3. Single draft pass
4. Self-review: scan anti-patterns list below, verify platform fit
5. Deliver

### Full Path
**When:** Blog posts, long LinkedIn (400+ words), threads, essays.

1. **Distill** — If input is raw dictation (fragmented sentences, filler words, tangents), produce a 2-3 sentence summary of the core idea and confirm with the user: "Core idea: [summary]. Is this what you meant?" This one confirmation prevents drafting a polished post that misses the point.
2. **Connect** — Identify which core beliefs from `references/voice-and-beliefs.md` the topic relates to
3. **Choose method** — Select articulation method from `references/generative-methods.md`
4. **Scaffold** — Load relevant platform file, determine structure
5. **Draft** — Write first draft using the chosen method and structure
6. **Editorial Loop** — Run the editorial pipeline per `references/editorial-pipeline.md`
7. **Critic Loop** — Spawn critic agent (see Agent Critic Loop below)
8. **Quality Gate** — Final anti-pattern scan and quality checklist
9. **Deliver**

## Dictation Handling

When input looks like raw dictation (no punctuation, filler words like "like/you know/basically", incomplete thoughts, topic jumps), treat it as raw material, not as prose to edit. Extract the core ideas first, confirm understanding, then draft.

CRITICAL: Do not try to polish dictation into a post directly. Distill the ideas first.

## Platform Dispatch

| Platform | Path | Load | Pass Selection |
|----------|------|------|----------------|
| Tweet | Fast | `platform-twitter.md` | Compression method, self-review |
| Thread | Full | `platform-twitter.md` | Full pipeline, arc check |
| LinkedIn <400w | Fast | `platform-linkedin.md` | Any method, self-review |
| LinkedIn 400w+ | Full | `platform-linkedin.md` | Full pipeline, critic loop |
| Blog | Full | `platform-blog.md` | Full pipeline, critic loop |

Always load `references/voice-and-beliefs.md` alongside the platform file.

For editorial pipeline details, load `references/editorial-pipeline.md`.

## Cross-Platform Conversion

When the user says "tweet this", "post this on LinkedIn", or "blog this" after a previous output:

1. Do NOT re-run the full pipeline
2. Take the core idea from the last output
3. Reformat for the target platform's constraints and voice calibration
4. Apply the target platform's self-review checklist
5. Deliver

This is a conversion, not a rewrite. The thinking is already done.

## Anti-Patterns (Never Do These)

### Language
- "I'm humbled to announce..." (false modesty)
- "Thrilled to share..." (performative enthusiasm)
- "Let that sink in." (condescending)
- "Read that again." (manipulative)
- "Here's the thing..." repeated (filler)
- Excessive emojis (more than 1-2 if any)

### Structure
- Broetry (one sentence per line for artificial drama)
- Humble-bragging disguised as lessons
- "X years ago I was [struggling]. Now I [success]" formula
- Listicles without genuine insight
- Engagement bait ("Comment below if you agree!")
- Claiming mastery in fields without demonstrated depth

### Tone
- Preaching from above rather than sharing alongside
- Absolute certainty on nuanced topics
- Generic advice that applies to no one specifically
- Recycled wisdom presented as original thought
- Corporate jargon (synergy, leverage as verb, move the needle)
- Hedging language (I think maybe, perhaps we could consider)
- Manufactured punchline closers designed for impact rather than genuine observation
- Hyphens, em dashes, or en dashes anywhere in the output

## Quality Checklist

Before finalizing any output, verify:

1. **Authenticity** — Does this sound like Aswin speaking, not a template?
2. **Substance** — Is there a genuine insight or just noise?
3. **Emotion** — Will this make someone feel something?
4. **Specificity** — Could only someone with this experience write this?
5. **Cringe** — Would this be embarrassing to read in 5 years?

## Agent Critic Loop

**Scope:** Blog posts and LinkedIn 400+ words only. Tweets and short posts skip this.

After completing the editorial pipeline draft:

1. Spawn a critic subagent using the Agent tool
2. Pass the draft, target platform, and the prompt from `references/critic-prompt.md`
3. The critic reviews against 5 criteria and returns specific line-level feedback
4. Revise the draft based on critic feedback
5. If the critic found 3+ substantive issues, run a second critic pass on the revised draft
6. Proceed to quality gate with the final draft

The critic runs in an isolated context — its token usage does not pollute the main conversation.

## Feedback Protocol

**Silent by design.** Never ask "Anything to adjust?" — just deliver the output.

**When the user corrects output** ("too long", "punchier", "not what I meant"):
1. Apply the correction to the current output
2. Evaluate confidence:
   - HIGH (explicit "always/never" language, or same correction seen before): write to `learned.md` immediately, silently
   - LOW (single correction, context-specific): note mentally, do NOT write. Wait for repetition.
3. Do not announce that feedback was logged

**When the user signals quality** ("this is good", "save this", "this missed the mark"):
- Append to `references/examples.md` with annotation about what worked or failed

**Consolidation:** Run `/cdf:learn consolidate writing-voice` when `learned.md` reaches ~20 entries. This deduplicates, merges, and promotes recurring patterns into `references/voice-and-beliefs.md`. User-initiated only.

**Runtime loading:** `learned.md` (at skill root) and `references/voice-and-beliefs.md` load alongside SKILL.md. `references/examples.md` loads only when calibration is needed.

**Universal command:** `/cdf:learn` for all learning operations (capture, view, remove, reset, consolidate).

## Reference Files

| File | Purpose | When Loaded |
|------|---------|-------------|
| `voice-and-beliefs.md` | Voice DNA + 10 core beliefs + influence calibration | Every writing task |
| `editorial-pipeline.md` | McPhee Loop with operational checklists | Full path only |
| `generative-methods.md` | Articulation methods (Micro Story, Pyramid, Cross-Domain, Compression) | When choosing method |
| `platform-blog.md` | Blog adaptation rules | Blog tasks |
| `platform-linkedin.md` | LinkedIn adaptation with Naval/Karpathy voice guides | LinkedIn tasks |
| `platform-twitter.md` | Twitter adaptation with Naval/Karpathy voice guides | Twitter tasks |
| `critic-prompt.md` | Instructions for critic subagent | Full path critic loop |
| `examples.md` | Good + bad output examples with annotations | On demand |

**Skill root:** `learned.md` contains learned preferences (Do/Don't/Style). Loaded every writing task alongside SKILL.md.
