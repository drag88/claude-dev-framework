# Design DNA Document — Output Template

This is the exact structure for the final Design DNA Document. Fill every section. Use `/* VERIFY */` for any value you cannot confirm — never guess.

Save as `[brand-name]-design-dna.md` in the current working directory.

---

```markdown
# Design DNA: [Brand Name]
> Source: [URL] | Pages analyzed: [comma-separated list] | Extracted: [YYYY-MM-DD]

---

## PART I: DESIGN IDEOLOGY

### Philosophy
[2-3 sentences capturing the "why" behind every design decision. What does this brand believe about design? What user feeling are they engineering toward?]

### Aesthetic Direction
**Name:** [Specific evocative name — e.g., "Clinical Precision", "Warm Brutalism", "Dark Techno Craft". Never just "Minimal" or "Modern".]
**Description:** [2-3 sentences: what this aesthetic includes and what it deliberately excludes]

### Brand Archetype
**Primary:** [Name]
**Secondary:** [Name or "None"]
**Evidence:** [2-3 specific examples from copy or design that confirm this — quote actual text or describe specific design choices]

### Design Principles
[5-7 principles. Each must be actionable for a coding agent.]

**1. [Principle Name]**
- Statement: [The principle as a declarative statement]
- Rationale: [Why this brand makes this choice and what it communicates]
- In code: [Specific, actionable implication for building — e.g., "Use font-weight: 700 only for H1 and primary CTAs. All other text uses 400 or 500."]

[Repeat for each principle]

### Anti-patterns — What This Brand Never Does
[5-8 items. Be specific — not "avoids clutter" but "never uses more than 2 font weights in a single component"]
- [Anti-pattern 1]
- [Anti-pattern 2]
- ...

---

## PART II: DESIGN TOKENS

> All values extracted from live site. Copy-paste ready.

### Color System

```css
/* ── Primary Brand Colors ── */
--color-primary:           [hex];   /* [usage context] */
--color-primary-hover:     [hex];   /* [derived — darken primary by ~8%] */
--color-primary-subtle:    [hex];   /* [light tint — tag backgrounds, highlights] */

/* ── Secondary / Accent ── */
--color-secondary:         [hex];   /* [usage context] */
--color-accent:            [hex];   /* [highlight, emphasis, call-outs] */

/* ── Neutral Scale ── */
--color-background:        [hex];   /* [page background] */
--color-surface:           [hex];   /* [cards, panels, inputs] */
--color-surface-raised:    [hex];   /* [modals, dropdowns, tooltips] */
--color-border:            [hex];   /* [dividers, input borders, card borders] */
--color-border-subtle:     [hex];   /* [very light separators] */

/* ── Text ── */
--color-text-primary:      [hex];   /* [headings, primary body text] */
--color-text-secondary:    [hex];   /* [subheadings, labels, secondary body] */
--color-text-muted:        [hex];   /* [captions, placeholders, disabled] */
--color-text-on-primary:   [hex];   /* [text on primary-colored backgrounds] */

/* ── Semantic ── */
--color-success:           [hex];
--color-warning:           [hex];
--color-error:             [hex];
--color-info:              [hex];

/* ── Brand Signature ── */
[Any gradient, overlay, or unique colors not covered above]
[Format for gradients: --gradient-hero: linear-gradient(135deg, #hex 0%, #hex 100%);]
```

**Color story:** [1-2 sentences — e.g., "Near-black background with a single electric indigo accent. The palette communicates focus and technical precision, softened by warm white text that prevents harshness."]

**Dark mode:** [Yes — see dark mode token overrides below / No / Partial — [which components?]]

[If dark mode: include the dark mode CSS block with token overrides under a `.dark` or `[data-theme="dark"]` selector]

### Typography

```css
/* ── Font Families ── */
--font-display:  '[Font Name]', [fallback];
--font-body:     '[Font Name]', [fallback];
--font-mono:     '[Font Name]', monospace;

/*
  Font sources:
  Display: [Google Fonts / Typekit / Self-hosted / System]
  Body:    [Google Fonts / Typekit / Self-hosted / System]

  To load (if Google Fonts):
  @import url('[exact import URL]');

  If paid/custom font:
  [Font Name] requires a paid license.
  Open-source alternative: '[Alt Font Name]' — closest match for [characteristic].
*/

/* ── Type Scale ── */
[Include only sizes the brand actually uses — remove unused rows]
--text-xs:    0.75rem;    /* 12px */
--text-sm:    0.875rem;   /* 14px */
--text-base:  1rem;       /* 16px */
--text-lg:    1.125rem;   /* 18px */
--text-xl:    1.25rem;    /* 20px */
--text-2xl:   1.5rem;     /* 24px */
--text-3xl:   1.875rem;   /* 30px */
--text-4xl:   2.25rem;    /* 36px */
--text-5xl:   3rem;       /* 48px */
--text-6xl:   3.75rem;    /* 60px */

/* ── Font Weights ── */
[Only weights this brand actually uses]
--font-regular:   400;
--font-medium:    500;
--font-semibold:  600;
--font-bold:      700;

/* ── Line Heights ── */
--leading-tight:   1.25;
--leading-normal:  1.5;
--leading-relaxed: 1.625;

/* ── Letter Spacing ── */
--tracking-tight:  -0.02em;
--tracking-normal:  0em;
--tracking-wide:    0.05em;
--tracking-wider:   0.1em;
```

**Typography personality:** [1-2 sentences — e.g., "Tightly tracked display headings signal editorial confidence. Body text is generously spaced — the brand trusts whitespace to do work."]

### Spacing System

```css
/* Base unit: [4px or 8px — state which] */
--space-1:   [px];   /*  [px] */
--space-2:   [px];   /*  [px] */
--space-3:   [px];   /*  [px] */
--space-4:   [px];   /*  [px] */
--space-5:   [px];   /*  [px] */
--space-6:   [px];   /*  [px] */
--space-8:   [px];   /*  [px] */
--space-10:  [px];   /*  [px] */
--space-12:  [px];   /*  [px] */
--space-16:  [px];   /*  [px] */
--space-20:  [px];   /*  [px] */
--space-24:  [px];   /*  [px] */
--space-32:  [px];   /*  [px] */

/* ── Semantic Layout Spacing ── */
--section-gap:         [px];   /* vertical gap between major page sections */
--container-padding-x: [px];   /* horizontal page padding */
--container-max-width:  [px];  /* maximum content width */
--card-padding:         [px];  /* internal card/panel padding */
--nav-height:           [px];
```

### Shape, Depth & Motion

```css
/* ── Border Radius ── */
--radius-none:  0px;
--radius-sm:    [px];   /* small UI elements — badges, inputs */
--radius-md:    [px];   /* buttons, cards */
--radius-lg:    [px];   /* panels, large cards */
--radius-xl:    [px];   /* feature blocks, hero sections */
--radius-full:  9999px; /* pills, avatars, toggle switches */

/* ── Shadows ── */
--shadow-xs: [value];   /* [effect: e.g., "1px border substitute"] */
--shadow-sm: [value];   /* [effect: e.g., "subtle card lift"] */
--shadow-md: [value];   /* [effect: e.g., "card elevation"] */
--shadow-lg: [value];   /* [effect: e.g., "floating panel"] */
--shadow-xl: [value];   /* [effect: e.g., "modal depth"] */
/* If brand uses no shadows: state "This brand avoids shadows — depth is created through [color contrast / borders / background shifts]." */

/* ── Motion ── */
--duration-fast:   [ms];
--duration-normal: [ms];
--duration-slow:   [ms];
--ease-default:    cubic-bezier([a], [b], [c], [d]);
--ease-enter:      cubic-bezier([a], [b], [c], [d]);
--ease-exit:       cubic-bezier([a], [b], [c], [d]);
/* If minimal/no animation: state "Motion energy is minimal. Use transitions ≤150ms with ease-out only on hover states." */
```

### Tailwind Config Extension

```javascript
// tailwind.config.js
const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary:    '[hex]',
          secondary:  '[hex]',
          accent:     '[hex]',
          background: '[hex]',
          surface:    '[hex]',
          border:     '[hex]',
          text: {
            primary:   '[hex]',
            secondary: '[hex]',
            muted:     '[hex]',
          },
          success:    '[hex]',
          warning:    '[hex]',
          error:      '[hex]',
        }
      },
      fontFamily: {
        display: ['[Font Name]', ...defaultTheme.fontFamily.sans],
        body:    ['[Font Name]', ...defaultTheme.fontFamily.sans],
        mono:    ['[Font Name]', ...defaultTheme.fontFamily.mono],
      },
      borderRadius: {
        sm:   '[value]',
        md:   '[value]',
        lg:   '[value]',
        xl:   '[value]',
      },
      boxShadow: {
        sm: '[value]',
        md: '[value]',
        lg: '[value]',
      },
      transitionTimingFunction: {
        'brand': '[cubic-bezier value]',
      },
      transitionDuration: {
        'fast':   '[ms without unit]',
        'normal': '[ms without unit]',
        'slow':   '[ms without unit]',
      },
      maxWidth: {
        'container': '[px]',
      },
    }
  }
}
```

---

## PART III: COMPONENT PATTERNS

> For each component: describe the visual recipe, then provide a Tailwind class string as a starting point. Tailwind class strings use the brand color tokens defined above.

### Navigation

- **Position & behavior:** [sticky|fixed|static] | [scroll behavior description]
- **Background:** [initial color] → [scrolled state: color + blur?]
- **Structure:** [description of logo, links, CTA arrangement]
- **Link style:** [size, weight, color, hover treatment]

```
nav wrapper:    "[Tailwind classes]"
nav link:       "[Tailwind classes]"
nav cta button: "[Tailwind classes — reference primary button below]"
```

### Buttons

**Primary**
- Background: `[hex]`
- Text: `[hex]`, `font-[weight]`, `text-[size]`
- Border: [none / 1px solid `[hex]` / gradient]
- Border radius: `[value]`
- Padding: `[py] [px]`
- Hover: [background shifts to `[hex]` / shadow added / scale 1.02]
- Focus: [ring color, width, offset]

```
"bg-brand-primary text-brand-text-on-primary font-[weight] text-[size]
 px-[x] py-[y] rounded-[radius]
 hover:bg-[color] active:scale-[95]
 transition-colors duration-fast
 focus:outline-none focus:ring-2 focus:ring-brand-primary focus:ring-offset-2"
```

**Secondary**
[Same structure]

**Ghost / Text** (if present)
[Same structure]

**Size variants:**
- sm: `px-[x] py-[y] text-[size]`
- md: `px-[x] py-[y] text-[size]` (default)
- lg: `px-[x] py-[y] text-[size]`

### Cards / Containers

- Background: `[hex]`
- Border: [none / `1px solid [hex]`]
- Shadow: `[value or none]`
- Border radius: `[value]`
- Padding: `[value]`
- Hover: [lift / glow / border shift / none]

```
"bg-brand-surface border border-brand-border rounded-[radius] p-[padding]
 [shadow class if any]
 hover:[treatment]
 transition-[property] duration-[speed]"
```

### Forms & Inputs

- **Input treatment:** [outlined / filled / underline]
- **Border:** `1px solid [hex]`, radius `[value]`
- **Focus:** ring `[color]`, border `[color]`
- **Label:** [above / floating / placeholder-only]
- **Error state:** border `[hex]`, message `text-[size] text-brand-error`

```
input: "w-full bg-brand-surface border border-brand-border rounded-[radius]
        px-[x] py-[y] text-[size] text-brand-text-primary
        placeholder:text-brand-text-muted
        focus:outline-none focus:ring-2 focus:ring-brand-primary focus:border-transparent
        disabled:opacity-50 disabled:cursor-not-allowed"

label: "block text-[size] font-[weight] text-brand-text-secondary mb-[space]"

error: "mt-[space] text-[size] text-brand-error"
```

### Badges / Tags

- Shape: [pill `rounded-full` / slightly rounded `rounded-md` / square `rounded-sm`]
- Padding: `px-[x] py-[y]`
- Font: `text-[size] font-[weight]`
- Variants and their colors:

```
base:    "inline-flex items-center px-[x] py-[y] rounded-[radius] text-[size] font-[weight]"
default: "bg-brand-surface border border-brand-border text-brand-text-secondary"
primary: "bg-brand-primary/10 text-brand-primary"
success: "bg-brand-success/10 text-brand-success"
```

---

## PART IV: LAYOUT PHILOSOPHY

### Grid System
- **Columns:** [12 / custom]
- **Max container width:** [px]
- **Horizontal padding:** [px at md] / [px at lg] / [px at xl]
- **Column gap:** [px]
- **Typical feature grid:** [3-col at desktop / 2-col at tablet / 1-col at mobile]

### Whitespace
**Rating:** [X/10]
**Pattern:** [Specific description of where and how whitespace is used in this brand's design]

### Page Architecture
Typical page section order:
1. [Section name + treatment]
2. [Section name + treatment]
...

### Section Separation
[How sections transition: pure whitespace / background color alternation / gradient dividers / angled cuts / wave SVGs / full-bleed image breaks]

---

## PART V: ASSET SIGNATURES

### Icon System
- **Style:** [outline / filled / duotone / illustrated / custom]
- **Stroke weight:** [thin / regular / bold — or Xpx]
- **Corners:** [sharp / rounded / circular]
- **Sizing:** [small Xpx inline / medium Xpx standalone / large Xpx feature]
- **Color:** [monochrome brand color / gray / semantic contextual]
- **Recommended library:** [name]
  - Install: `npm install [package]`
  - Import: `import { IconName } from '[package]'`
  - [If custom/no match: "Closest open-source match: [library], using [subset/style]"]

### Imagery & Visual Assets
- **Photography:** [yes/no — style]
- **Illustration:** [yes/no — style + creation tool recommendation if relevant]
- **Gradients:** [description + exact CSS value if prominent]
- **Image treatment:** [raw / overlay / tinted / grayscale]
- **Aspect ratios:** [list]

---

## PART VI: VOICE & TONE

### Brand Voice Formula
[Brand] is **[adj]**, **[adj]**, **[adj]**, **[adj]**, and **[adj]** — but never **[adj]**.

### Tone Spectrum
| Dimension | Score | Description |
|-----------|-------|-------------|
| Formal ←→ Casual | [X]/10 | [label] |
| Technical ←→ Plain | [X]/10 | [label] |
| Serious ←→ Playful | [X]/10 | [label] |
| Confident ←→ Humble | [X]/10 | [label] |
| Warm ←→ Efficient | [X]/10 | [label] |
| Verbose ←→ Terse | [X]/10 | [label] |

### Headline Examples
[6-8 actual headlines from site, tagged by page]
- "[headline]" — [page]

### Headline Formula
[Pattern + example]

### CTA Language
All CTAs observed:
- "[exact CTA]" — [location]

Pattern: [description]

### Value Proposition
**One-liner:** [their words]
**Problem solved:** [pain they remove]
**Differentiation:** [their "only we..." claim]
**Target audience:** [who this is for]

---

## PART VII: AGENT REPLICATION GUIDE

> Read this section first. Everything else is reference material.

### "To build something that feels like [Brand]..."

#### Step 1 — Environment Setup
```bash
# Install fonts
npm install @fontsource/[font-name]
# or: load from Google Fonts (see import URL in Part II Typography)

# Install icon library
npm install [package-name]
```

```css
/* Add to your global CSS */
@import '@fontsource/[font-name]/400.css';
@import '@fontsource/[font-name]/700.css';
/* Then copy all CSS custom properties from Part II into :root */
```

#### Step 2 — Build Order
1. Define all CSS custom properties from Part II into `:root`
2. Set `body { background: var(--color-background); color: var(--color-text-primary); font-family: var(--font-body); }`
3. Build the primary button — it's the single clearest expression of the brand
4. Build a card component — establishes surface, depth, and radius language
5. Build the navigation
6. Lay out a hero section
7. Apply the whitespace philosophy (section gap from spacing tokens)

#### Step 3 — The 3 Visual Signatures
These 3 things make it unmistakably [Brand]. Get these right and the rest follows.

1. **[Signature name]**
   [Specific description] → In code: [exact implementation note]

2. **[Signature name]**
   [Specific description] → In code: [exact implementation note]

3. **[Signature name]**
   [Specific description] → In code: [exact implementation note]

#### Step 4 — The 5 Brand Breakers
These 5 things will immediately make it NOT feel like [Brand].

1. [Precise anti-pattern with explanation]
2. [Precise anti-pattern with explanation]
3. [Precise anti-pattern with explanation]
4. [Precise anti-pattern with explanation]
5. [Precise anti-pattern with explanation]

#### Step 5 — Copy Guidelines for Generated Content
- Tone: [3-5 specific guidance points]
- Headline formula: [formula] → Example: "[example]"
- CTA formula: [formula] → Example: "[example]"
- Avoid in copy: [3-5 specific things]

---

*Design DNA extracted by Claude Code brand-dna skill.*
*Verify token values against live site before shipping — design systems change.*
```
