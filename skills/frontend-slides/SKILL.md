---
name: frontend-slides
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices.
---

# Frontend Slides Skill

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser. This skill helps non-designers discover their preferred aesthetic through visual exploration ("show, don't tell"), then generates production-quality slide decks.

## Core Philosophy

1. **Zero Dependencies** -- Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** -- People don't know what they want until they see it. Generate visual previews, not abstract choices.
3. **Distinctive Design** -- Avoid generic "AI slop" aesthetics. Every presentation should feel custom-crafted.
4. **Production Quality** -- Code should be well-commented, accessible, and performant.
5. **Viewport Fitting (CRITICAL)** -- Every slide MUST fit exactly within the viewport. No scrolling within slides, ever. This is non-negotiable.

---

## CRITICAL: Viewport Fitting Requirements

**Every slide MUST fit exactly in the viewport. No scrolling within slides, ever.**

### Content Density Limits

| Slide Type | Maximum Content |
|------------|-----------------|
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid | 1 heading + 6 cards maximum (2x3 or 3x2 grid) |
| Code slide | 1 heading + 8-10 lines of code maximum |
| Quote slide | 1 quote (max 3 lines) + attribution |
| Image slide | 1 heading + 1 image (max 60vh height) |

**If content exceeds these limits, split into multiple slides.**

### Required CSS Rules (every presentation)

- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- All font sizes use `clamp(min, preferred, max)`
- All spacing uses `clamp()` or viewport units
- Content containers have `max-height` constraints
- Images have `max-height: min(50vh, 400px)` or similar
- Grids use `auto-fit` with `minmax()` for responsive columns
- Breakpoints exist for heights: 700px, 600px, 500px
- No fixed pixel heights on content elements

> See `references/style-presets.md` for mandatory base CSS block and full viewport fitting checklist.

### When Content Doesn't Fit

**DO:** Split into multiple slides, reduce bullets (max 5-6), shorten text, use smaller code snippets, create "continued" slides.

**DON'T:** Reduce font below readable limits, remove padding entirely, allow any scrolling, cram content.

---

## Phase 0: Detect Mode

| Mode | Trigger | Next Phase |
|------|---------|------------|
| A: New Presentation | User wants slides from scratch | Phase 1 |
| B: PPT Conversion | User has .ppt/.pptx file | Phase 4 |
| C: Enhancement | User has existing HTML presentation | Read file, then enhance |

---

## Phase 1: Content Discovery (New Presentations)

Ask via AskUserQuestion:

1. **Purpose** -- Pitch deck / Teaching / Conference talk / Internal presentation
2. **Length** -- Short (5-10) / Medium (10-20) / Long (20+)
3. **Content readiness** -- All ready / Rough notes / Topic only

If user has content, ask them to share it.

---

## Phase 2: Style Discovery (Visual Exploration)

### How Users Choose Presets

**Option A: Guided Discovery (Default)** -- User answers mood questions, skill generates 3 preview files, user picks favorite.

**Option B: Direct Selection** -- User requests a preset by name (e.g., "Use Bold Signal"). Skip to Phase 3.

### Available Presets

| Preset | Vibe | Best For |
|--------|------|----------|
| Bold Signal | Confident, high-impact | Pitch decks, keynotes |
| Electric Studio | Clean, professional | Agency presentations |
| Creative Voltage | Energetic, retro-modern | Creative pitches |
| Dark Botanical | Elegant, sophisticated | Premium brands |
| Notebook Tabs | Editorial, organized | Reports, reviews |
| Pastel Geometry | Friendly, approachable | Product overviews |
| Split Pastel | Playful, modern | Creative agencies |
| Vintage Editorial | Witty, personality-driven | Personal brands |
| Neon Cyber | Futuristic, techy | Tech startups |
| Terminal Green | Developer-focused | Dev tools, APIs |
| Swiss Modern | Minimal, precise | Corporate, data |
| Paper & Ink | Literary, thoughtful | Storytelling |

> See `references/style-presets.md` for full preset definitions (colors, typography, signature elements).

### Step 2.1: Mood Selection (Guided Discovery)

Ask about desired feeling: Impressed/Confident, Excited/Energized, Calm/Focused, Inspired/Moved (multi-select up to 2).

| Mood | Style Options |
|------|---------------|
| Impressed/Confident | Bold Signal, Electric Studio, Dark Botanical |
| Excited/Energized | Creative Voltage, Neon Cyber, Split Pastel |
| Calm/Focused | Notebook Tabs, Paper & Ink, Swiss Modern |
| Inspired/Moved | Dark Botanical, Vintage Editorial, Pastel Geometry |

### Step 2.2: Generate 3 Style Previews

Create in `.claude-design/slide-previews/` as self-contained HTML files (~50-100 lines each). Each shows one title slide with the aesthetic's typography, colors, and animation style.

**Never use:** Purple gradients on white, Inter/Roboto/system fonts, standard blue primaries, predictable hero layouts.

### Step 2.3: Present and Choose

Show user the 3 previews. Ask which they prefer (or "Mix elements" for custom combination).

---

## Phase 3: Generate Presentation

Build the full presentation using content from Phase 1 and style from Phase 2.

**File structure:** Single `presentation.html` (self-contained) + optional `assets/` directory for images.

> See `references/html-templates.md` for the full HTML architecture template, JS requirements, and code quality standards.

**Responsive & Viewport Fitting:** Apply all rules from the viewport fitting section above. See `references/style-presets.md` for the mandatory base CSS block.

---

## Phase 4: PPT Conversion

1. **Extract content** using `python-pptx` (see `references/html-templates.md` for extraction code)
2. **Confirm** extracted content structure with user
3. **Style selection** -- proceed to Phase 2
4. **Generate HTML** preserving all text, images, slide order, and speaker notes

---

## Phase 5: Delivery

1. Clean up `.claude-design/slide-previews/` if it exists
2. Open presentation with `open [filename].html`
3. Provide summary with navigation instructions and customization tips (CSS variables, fonts, animation timings)

> See `references/animation-patterns.md` for effect-to-feeling mapping and CSS/JS animation code examples.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Fonts not loading | Check Fontshare/Google Fonts URL and CSS font names |
| Animations not triggering | Verify Intersection Observer and `.visible` class |
| Scroll snap broken | Ensure `scroll-snap-type` on html/body, `scroll-snap-align` on slides |
| Mobile issues | Disable heavy effects at 768px, test touch events |
| Performance | Use `will-change` sparingly, prefer `transform`/`opacity` animations |

> See `references/style-presets.md` for detailed viewport troubleshooting.

---

## Related Skills

- **frontend-design** -- For more complex interactive pages beyond slides
- **pptx** -- For PowerPoint-specific workflows

## Reference Files

| File | Contents |
|------|----------|
| `references/style-presets.md` | All 12 preset definitions, mandatory base CSS, viewport checklist |
| `references/html-templates.md` | HTML architecture template, JS features, code quality, PPT extraction |
| `references/animation-patterns.md` | Effect-to-feeling mapping, CSS entrance/background animations, JS interactive effects |
