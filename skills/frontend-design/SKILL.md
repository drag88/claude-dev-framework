---
name: frontend-design
description: "Activates when building web interfaces, design systems, or styling components with high visual quality"
license: Complete terms in LICENSE.txt
---

# Frontend Design

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. The goal is to implement real working code with exceptional attention to aesthetic details and creative choices.

## When to Activate

- Building web components, pages, or applications
- Creating landing pages or marketing sites
- Designing dashboards or admin interfaces
- Styling or beautifying any web UI
- Creating HTML/CSS layouts or React components
- When visual design quality matters

---

## User Preferences (Default Style)

Unless explicitly overridden, apply these preferences:

| Preference | Direction |
|------------|-----------|
| **Typography** | Helvetica (or Helvetica Neue) as primary font |
| **Aesthetic** | Minimalist — clean, restrained, essential |
| **Visual Style** | Glassmorphism — frosted glass, backdrop blur, subtle transparency |
| **Approach** | Less is more — every element must earn its place |

### Minimalist Execution

- **Whitespace as design element** — generous, intentional negative space
- **Limited color palette** — 2-3 colors maximum, one accent
- **Typography-driven hierarchy** — size and weight, not decoration
- **Subtle depth** — glassmorphism over heavy shadows
- **Refined details** — precision in spacing, alignment, micro-interactions
- **No visual clutter** — remove anything that doesn't serve a purpose

### Glassmorphism Implementation

```css
/* Glass card pattern */
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}

/* Dark variant */
.glass-dark {
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

Key glassmorphism principles:
- Subtle blur (8-16px) — not overwhelming
- Low-opacity backgrounds (0.1-0.3)
- Thin, semi-transparent borders
- Works best with colorful or image backgrounds behind
- Maintain text contrast for accessibility

---

## The AI Slop Problem

LLMs generate UI by sampling from training data patterns. Without explicit guidance, outputs converge toward the statistical median: **generic, safe, forgettable**.

### The AI Slop Signature (Reject These Patterns)

| Category | Generic Pattern | Why It's Slop |
|----------|-----------------|---------------|
| **Typography** | Inter, Roboto, Arial, Open Sans, Lato | Every tutorial default |
| **Colors** | Purple/indigo gradients on white | SaaS template cliche |
| **Layout** | 3-column grid with icon boxes | Tailwind tutorial median |
| **Hero** | Centered text + gradient blob + "Get Started" CTA | Every landing page ever |
| **Corners** | `rounded-xl` on everything | "Safe" modern look |
| **Spacing** | Timid, evenly-distributed | Avoids bold decisions |
| **Motion** | None, or generic fade-in | Performance "safety" |
| **Backgrounds** | Solid white or gray | Zero creative risk |
| **Decorations** | Blob SVGs, abstract shapes | Lazy visual filler |

### Specific Elements to NEVER Use

- Three icon boxes arranged in a symmetric grid
- Centered hero with gradient blob behind headline
- Purple-to-blue diagonal gradients
- Tailwind default colors (`indigo-500`, `purple-600`, `blue-500`)
- "Get Started" or "Learn More" as CTA text
- Blob SVG decorations from blobmaker
- `rounded-xl` or `rounded-2xl` on every element
- Stock illustration style (Undraw, Humaaans)

---

## Design Thinking

Before coding, understand the context and commit to a **BOLD aesthetic direction**.

### Key Considerations

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick a distinctive aesthetic direction (see below)
- **Constraints**: Technical requirements (framework, performance, accessibility)
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

### Aesthetic Directions

Choose a direction and commit fully—these are starting points, not limits:

| Direction | Character |
|-----------|-----------|
| **Minimalist (Default)** | Clean, restrained, essential, glassmorphism |
| Brutally minimal | Stark, severe, almost empty |
| Maximalist chaos | Dense, layered, overwhelming |
| Retro-futuristic | Vintage meets tomorrow |
| Organic/natural | Flowing, living, imperfect |
| Luxury/refined | Premium, sophisticated, elegant |
| Playful/toy-like | Fun, bouncy, joyful |
| Editorial/magazine | Typography-forward, print-inspired |
| Brutalist/raw | Exposed structure, anti-design |
| Art deco/geometric | Bold shapes, symmetry, gold accents |
| Soft/pastel | Gentle, approachable, calming |
| Industrial/utilitarian | Functional, no-nonsense, exposed |
| Dark/moody | Deep colors, dramatic contrast |
| Lo-fi/zine | Raw, handmade, photocopied |
| Handcrafted/artisanal | Warm, human, imperfect |

### Critical Principle

**Choose a clear conceptual direction and execute it with precision.** Bold maximalism and refined minimalism both work—the key is intentionality, not intensity.

> See `references/typography.md` for font selection tables by aesthetic, contrast rules, and banned fonts.

> See `references/visual-system.md` for color/theme palettes, spatial composition, motion/animation, and backgrounds.

---

## Implementation Requirements

Implement working code (HTML/CSS/JS, React, Vue, etc.) that is:

- **Production-grade** and functional
- **Visually striking** and memorable
- **Cohesive** with a clear aesthetic point-of-view
- **Responsive** across viewport sizes
- **Accessible** with proper contrast and focus states
- **Meticulously refined** in every detail

---

## Accessibility Requirements

Non-negotiable baseline:

| Requirement | Standard |
|-------------|----------|
| **Color contrast** | 4.5:1 for body text, 3:1 for large text (WCAG AA) |
| **Focus states** | Visible keyboard focus on all interactive elements |
| **Touch targets** | Minimum 44x44px for mobile |
| **Alt text** | Descriptive for images, empty for decorative |
| **Semantic HTML** | Proper headings, landmarks, form labels |

---

## Form & Interactive States

Design all states, not just default:

| State | Design Consideration |
|-------|---------------------|
| **Default** | Clear affordance, visible labels |
| **Hover** | Subtle feedback, cursor change |
| **Focus** | Prominent ring, high contrast |
| **Active/Pressed** | Tactile feedback |
| **Disabled** | Reduced opacity, no pointer |
| **Error** | Red accent, icon, helpful message |
| **Success** | Green accent, confirmation |
| **Loading** | Spinner or skeleton, disable submit |

---

## Process

1. **Understand** the context, purpose, and audience
2. **Reject** AI slop patterns explicitly
3. **Commit** to a bold aesthetic direction
4. **Select** distinctive typography and color palette
5. **Implement** with meticulous attention to detail
6. **Verify** accessibility (contrast, focus, touch targets)
7. **Refine** motion, spacing, and micro-interactions
8. **Confirm** the design feels distinctive, not generic

---

## Final Reminder

**Claude is capable of extraordinary creative work.** The default patterns exist because they're statistically common—not because they're good. Reject the median. Make bold choices. Execute with precision.

Every design decision is an opportunity to create something memorable instead of forgettable.

## Suggested Commands
- `/cdf:implement` — Build interfaces with design skill guidance
- `/cdf:design` — Design UI components and pages

Opus 4.7 plays the frontend-engineer role from the Role line in CLAUDE.md when given visual design context — no dedicated frontend-architect agent needed.

## Reference Files

| File | Contents |
|------|----------|
| `references/typography.md` | Font selection by aesthetic, contrast rules, banned fonts |
| `references/visual-system.md` | Color/theme, spatial composition, motion/animation, backgrounds |
