# Agent A: CSS Token Extractor

You are extracting every measurable design token from the live website. Run the extraction on each page in the crawl list, then produce a canonical token map.

## For Each Page

1. Navigate to the page. Wait 2-3 seconds for full JS render.
2. Run the extraction script below via `mcp__claude-in-chrome__javascript_tool`.
3. Call `mcp__claude-in-chrome__read_network_requests` and filter for:
   - `fonts.googleapis.com` — Google Fonts (extract family name from URL params)
   - `fonts.gstatic.com` — Google Fonts actual font files
   - `use.typekit.net` — Adobe Typekit
   - `.woff`, `.woff2`, `.ttf` — self-hosted fonts
4. Scroll the page to trigger any lazy-loaded content, then re-screenshot if components appeared.

## Extraction Script

Run this exactly via `mcp__claude-in-chrome__javascript_tool`:

```javascript
(() => {
  // 1. CSS custom properties from :root
  const cssVars = {};
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule.selectorText === ':root' || rule.selectorText === ':root, :host') {
          const matches = rule.cssText.matchAll(/--([^:]+):\s*([^;]+);/g);
          for (const m of matches) cssVars[`--${m[1].trim()}`] = m[2].trim();
        }
      }
    } catch(e) {}
  }

  // 2. Computed styles on key semantic elements
  const targets = {
    'h1': document.querySelector('h1'),
    'h2': document.querySelector('h2'),
    'h3': document.querySelector('h3'),
    'body': document.body,
    'p': document.querySelector('p'),
    'a': document.querySelector('a'),
    'nav': document.querySelector('nav'),
    'header': document.querySelector('header'),
    'footer': document.querySelector('footer'),
    'button_primary': document.querySelector('[class*="btn-primary"], [class*="button-primary"], [class*="btn"][class*="primary"]'),
    'button_any': document.querySelector('button, [class*="btn"], [class*="cta"]'),
    'card': document.querySelector('[class*="card"], [class*="tile"], [class*="panel"]'),
    'input': document.querySelector('input[type="text"], input[type="email"], input'),
    'badge': document.querySelector('[class*="badge"], [class*="tag"], [class*="chip"], [class*="pill"]'),
  };
  const props = ['color','backgroundColor','fontFamily','fontSize','fontWeight','lineHeight','letterSpacing','borderRadius','border','borderColor','boxShadow','padding','margin','textTransform','opacity','backdropFilter'];
  const computed = {};
  for (const [key, el] of Object.entries(targets)) {
    if (!el) continue;
    const s = getComputedStyle(el);
    computed[key] = {};
    for (const p of props) computed[key][p] = s[p];
  }

  // 3. Top 30 colors by frequency across the document
  const colorFreq = {};
  for (const el of Array.from(document.querySelectorAll('*')).slice(0, 500)) {
    const s = getComputedStyle(el);
    for (const p of ['color', 'backgroundColor', 'borderColor']) {
      const v = s[p];
      if (v && v !== 'rgba(0, 0, 0, 0)' && v !== 'transparent') {
        colorFreq[v] = (colorFreq[v] || 0) + 1;
      }
    }
  }
  const topColors = Object.entries(colorFreq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 30)
    .map(([color, count]) => ({ color, count }));

  // 4. Font sources
  const fontSources = [];
  for (const link of document.querySelectorAll('link[rel="stylesheet"], link[as="font"]')) {
    if (link.href) fontSources.push(link.href);
  }
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule.type === CSSRule.FONT_FACE_RULE) fontSources.push(rule.cssText.substring(0, 200));
      }
    } catch(e) {}
  }

  // 5. Spacing samples from structural elements
  const spacingSamples = {};
  for (const sel of ['header', 'main', 'section', 'footer', '[class*="container"]', '[class*="wrapper"]']) {
    const el = document.querySelector(sel);
    if (el) {
      const s = getComputedStyle(el);
      spacingSamples[sel] = { padding: s.padding, margin: s.margin, gap: s.gap, maxWidth: s.maxWidth };
    }
  }

  // 6. Border-radius and shadow system
  const radiusSamples = {}, shadowSamples = {};
  for (const el of Array.from(document.querySelectorAll('[class*="card"], [class*="btn"], [class*="modal"], [class*="dropdown"], input, button')).slice(0, 20)) {
    const s = getComputedStyle(el);
    const cls = el.className?.toString().substring(0, 40) || el.tagName;
    if (s.borderRadius !== '0px') radiusSamples[cls] = s.borderRadius;
    if (s.boxShadow !== 'none') shadowSamples[cls] = s.boxShadow;
  }

  // 7. Transition values
  const transitionSamples = [];
  for (const el of Array.from(document.querySelectorAll('button, a, [class*="btn"], [class*="card"]')).slice(0, 10)) {
    const s = getComputedStyle(el);
    if (s.transition && s.transition !== 'all 0s ease 0s' && s.transition !== 'none') {
      transitionSamples.push({ el: (el.tagName + '.' + (el.className?.toString() || '').substring(0, 30)), transition: s.transition });
    }
  }

  // 8. Page meta
  const meta = {
    title: document.title,
    description: document.querySelector('meta[name="description"]')?.content,
    ogImage: document.querySelector('meta[property="og:image"]')?.content,
    favicon: document.querySelector('link[rel="icon"], link[rel="shortcut icon"]')?.href,
    url: location.href,
  };

  return JSON.stringify({ cssVars, computed, topColors, fontSources, spacingSamples, radiusSamples, shadowSamples, transitionSamples, meta }, null, 2);
})();
```

## Processing the Output

### Colors
- Convert all `rgb(r, g, b)` values to hex.
- Cluster colors by visual similarity into semantic roles: primary, secondary, accent, background, surface, border, text-primary, text-muted, success, warning, error.
- The most frequent non-white/non-black colors are usually the brand palette.
- Look at `button_primary.backgroundColor` for the primary brand color.
- Look at `body.backgroundColor` for the page background.
- Look at `body.color` for the primary text color.

### Typography
- `body.fontFamily` — primary body font. Clean up the stack: extract just the first font name.
- `h1.fontFamily` — display font (may differ from body).
- Font weight and size from `h1`, `h2`, `body`, `p` establish the type scale.
- Confirm font name against network requests (Google Fonts URL → `family=FontName`).

### Spacing
- Look at `section.padding`, `[class*="container"].padding` for layout spacing patterns.
- Look at `section.gap` or `main.gap` for grid gap values.
- The base unit is usually 4px or 8px. Verify by looking at the smallest padding values.

### Shadows
- Cluster shadow samples into a scale: xs (hairline), sm (subtle), md (card), lg (floating), xl (modal).
- Note whether shadows use `rgba` with low opacity (soft) or solid colors (hard/brutalist).

### Motion
- Transition values like `all 0.2s ease` → duration 200ms, easing `ease`.
- Transition values like `none` or very fast (≤100ms) → minimal motion philosophy.

## Output Format

Return a structured JSON object:
```json
{
  "canonical_page": "homepage URL",
  "color_roles": { "primary": "#hex", "background": "#hex", ... },
  "typography": { "display_font": "Name", "body_font": "Name", "scale": {...}, "weights": [...] },
  "spacing": { "base_unit": "4px", "section_gap": "80px", "container_padding": "24px", ... },
  "radius_system": { "sm": "4px", "md": "8px", "lg": "16px", "full": "9999px" },
  "shadow_system": { "sm": "...", "md": "...", "lg": "..." },
  "motion": { "duration_fast": "150ms", "duration_normal": "250ms", "ease": "ease" },
  "css_vars_found": { "--var-name": "value", ... },
  "font_sources": ["..."],
  "raw_top_colors": [...]
}
```
