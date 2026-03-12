---
name: brand-dna
description: Extract the complete design DNA and ideology of any brand from its website. Produces a structured Design DNA Document that a coding agent can use as source of truth to build or replicate the brand's design system. Triggers on "/brand-dna <url>" or requests like "extract the design DNA of...", "analyze the brand identity of...", "I want to build something that looks like...".
allowed-tools: mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__javascript_tool, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__get_page_text, mcp__claude-in-chrome__read_network_requests, mcp__claude-in-chrome__tabs_create_mcp, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__find, mcp__claude-in-chrome__read_page, WebSearch, Write, Read, Agent
---

# Brand DNA Skill

Extract the complete design DNA, ideology, and visual language of any brand from its website. Output is a **Design DNA Document** — a structured specification a coding agent uses as the sole source of truth to build something that authentically replicates the brand's design system and feel.

This is not a CSS scraper. It is full design intelligence: visual tokens + design ideology + brand personality + replication guide.

## Invocation

```
/brand-dna <url>
/brand-dna <url> "<brand name>"   # brand name is inferred if omitted
```

## Execution Philosophy

- **Real browser.** Use `mcp__claude-in-chrome__*` tools. Handles SPAs, lazy-loaded content, JS-rendered styles.
- **Multi-page.** Crawl up to 5 pages: homepage → about → pricing/product → features → blog.
- **Three parallel agents.** CSS/Token, Visual, Copy — each reads its own reference file. Synthesizer reads the output template.
- **Prescriptive output.** Every section tells a coding agent what to do, not just what the brand looks like.

---

## Step 0: Setup

1. Call `mcp__claude-in-chrome__tabs_context_mcp` to check browser state.
2. Create a new tab with `mcp__claude-in-chrome__tabs_create_mcp`.
3. Navigate to the target URL. Wait for full load.
4. Infer brand name from `<title>`, meta tags, or logo alt text if not provided.
5. Discover available pages: check nav for `/about`, `/about-us`, `/pricing`, `/features`, `/product`, `/blog`, `/careers`.
6. Select up to 5 pages. Priority: homepage > about > pricing or product > features > blog.
7. **Divide pages across the three agents** before spawning. Each agent crawls its own assigned subset — they do NOT share pages sequentially.

**Page assignment example for 5 pages (p1–p5):**
- Agent A (CSS): p1 (homepage) + p3 (pricing) — homepage is canonical for tokens
- Agent B (Visual): p1 + p2 (about) + p4 (features)
- Agent C (Copy): p1 + p2 + p5 (blog)
- Homepage overlaps intentionally — each agent needs it for its domain.

---

## Step 1: Spawn Three Parallel Extraction Agents

**CRITICAL: Spawn all three agents simultaneously in a single batch. Never run them sequentially.**
Call the `Agent` tool three times in the same response (parallel tool calls). Each agent navigates its own pages independently in the browser.

Pass to each agent: the brand name, its assigned page URLs, and the path to its reference file.

### Agent A — CSS Token Extractor
**Assigned pages:** Homepage + 1–2 product/pricing pages.
**Goal:** Extract every measurable design token from the live site.
**Read `references/agent-css-extractor.md` for full instructions and the JavaScript extraction script.**
**Output:** Raw token map per page. Homepage is canonical for primary tokens.

### Agent B — Visual Analyst
**Assigned pages:** Homepage + about + 1–2 feature/product pages.
**Goal:** Analyze visual design through screenshots. Infer layout, hierarchy, whitespace personality, image/icon treatment, motion signals.
**Read `references/agent-visual-analyst.md` for the full visual analysis checklist.**
**Output:** Structured visual profile synthesized across all pages.

### Agent C — Copy & Tone Analyst
**Assigned pages:** Homepage + about + blog/careers (content-rich pages).
**Goal:** Analyze all written content to extract brand voice, tone, personality, and messaging architecture.
**Read `references/agent-copy-analyst.md` for the full tone framework and brand archetype reference.**
**Output:** Brand voice + personality profile.

---

## Step 2: Synthesize — Design DNA Document

After all three agents complete:

1. Read `references/output-template.md` for the full document structure and formatting rules.
2. Apply these synthesis rules:
   - Convert all colors to hex (no `rgb()` in the output tokens).
   - If multiple pages show different values, homepage is canonical for primary tokens.
   - For paid/custom fonts: name the font exactly, state it requires a license, provide the closest open-source alternative. Format: `/* Paid: [Font] — Open-source alternative: '[Alt]' */`
   - If a token cannot be confidently determined, mark it `/* VERIFY */` rather than guessing.
   - Design ideology must be written as principles a coding agent can act on — not description.
3. Save the final document as `[brand-name]-design-dna.md` in the current working directory using the Write tool.

---

## Edge Cases

If a page blocks automation (Cloudflare, CAPTCHA) or data is incomplete, read `references/edge-cases.md` before proceeding.

---

## Quality Gate

Before saving, verify:
- [ ] All color values are hex (no `rgb()`)
- [ ] Font names confirmed from network requests, not guessed
- [ ] The 3 visual signatures in the replication guide are specific to this brand — not generic
- [ ] Tailwind config is valid JavaScript syntax
- [ ] Anti-patterns are precise ("never uses gradients on text") not vague ("avoid clutter")
- [ ] Aesthetic name is specific and evocative — not just "minimal" or "modern"
- [ ] Value proposition uses actual site copy — not inferred generically
- [ ] File saved as `[brand-name]-design-dna.md`
