# Visual System

## Table of Contents

- [Color & Theme](#color--theme)
- [Spatial Composition](#spatial-composition)
- [Motion & Animation](#motion--animation)
- [Backgrounds & Visual Details](#backgrounds--visual-details)

---

## Color & Theme

### Escape the Purple Trap

**INSTEAD of** purple/indigo gradients, draw from:

| Source | Example Palettes |
|--------|------------------|
| **IDE Themes** | Dracula (purple+pink+cyan), Nord (arctic blues), Solarized (warm yellows), Monokai (vibrant accents), One Dark (muted jewel tones) |
| **Cultural** | Japanese (indigo, vermillion, gold), Scandinavian (muted naturals, warm whites), Mediterranean (terracotta, olive, azure) |
| **Eras** | Art Deco (black, gold, cream), 70s (burnt orange, avocado, mustard), 80s (neon pink, cyan, black), 90s (teal, purple, silver) |
| **Nature** | Forest (deep greens, bark brown), Desert (sand, terracotta, sage), Ocean (navy, foam white, coral) |

### Color Strategy

- **Dominant + sharp accent** beats evenly-distributed palettes
- Use CSS custom properties for semantic naming (`--accent`, `--surface`, `--text-primary`)
- Commit to light OR dark as primary, design the other as intentional variant
- High contrast for hierarchy, not decoration

### Dark Mode

Design dark mode as a first-class theme, not an afterthought:
- Invert thoughtfully—don't just swap black/white
- Reduce contrast slightly for comfort (not pure #000/#FFF)
- Accent colors may need adjustment for dark backgrounds

---

## Spatial Composition

### Layout Principles

- **Asymmetry** over centered symmetry
- **Z-depth effects** with layering and shadows
- **Full-bleed sections** breaking container constraints
- **Dramatic scale jumps** between elements
- **Overlap and layering** for depth
- **Grid-breaking elements** that escape rigid structure
- **Generous negative space** OR controlled density (commit to one)

### Layout Anti-Patterns (NEVER Use)

- Three-column symmetric grids with icons
- Everything centered on every section
- Uniform card grids without hierarchy
- Safe Tailwind defaults without customization
- Equal spacing everywhere (vary rhythm)

---

## Motion & Animation

### High-Impact Moments

Focus animation budget on:
- **Page load**: Staggered reveals with `animation-delay`
- **Scroll triggers**: Elements animating into view
- **Hover states**: Personality in interactions
- **State transitions**: Smooth feedback on actions

### Implementation

- CSS-only for HTML (keyframes, transitions)
- Framer Motion for React
- One orchestrated sequence > scattered micro-interactions

### Motion Anti-Patterns

- Generic fade-in on everything
- No motion at all
- Bounce/elastic on every element
- Motion that delays interaction

---

## Backgrounds & Visual Details

### Create Atmosphere

| Technique | Effect | When to Use |
|-----------|--------|-------------|
| **Glassmorphism (Preferred)** | Frosted depth, modern elegance | Cards, modals, overlays, navigation |
| Gradient meshes | Depth, dimension | Hero sections, feature backgrounds |
| Noise/grain textures | Tactile, organic | Retro, editorial, artisanal |
| Geometric patterns | Structure, rhythm | Tech, brutalist, art deco |
| Layered transparencies | Depth, complexity | Modern, minimalist |
| Subtle shadows | Soft hierarchy | Cards, buttons (keep it light) |
| Halftone/duotone | Print-inspired, bold | Editorial, retro |
| Parallax layers | Immersion, depth | Landing pages, storytelling |
| Knockout typography | Bold, graphic | Headers, hero text |

### Background Anti-Patterns

- Solid white backgrounds everywhere
- Generic gradient blobs
- Stock pattern overlays
- Decorative SVGs with no purpose
