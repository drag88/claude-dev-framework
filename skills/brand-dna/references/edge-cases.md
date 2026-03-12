# Edge Cases & Fallbacks

Read this file only when encountering problems during extraction: bot protection, blocked pages, missing data, or incomplete results.

---

## Bot Protection / Automation Blocking

**Symptoms:** Cloudflare challenge page, CAPTCHA, 403 error, or page stuck loading.

**Resolution order:**

1. **Try a subpage first.** Homepages are more aggressively protected than interior pages. Try navigating directly to `/about`, `/pricing`, or `/blog` instead.

2. **Wait and retry once.** Some bot protection challenges resolve after a 3-5 second pause. Try navigating again once.

3. **Use WebSearch as fallback.** Search for the brand's public design resources:
   - `[brand name] design system`
   - `[brand name] brand guidelines`
   - `[brand name] figma community`
   - `[brand name] style guide site:github.com`
   - `[brand name] colors fonts design tokens`

   Public design docs are often *more authoritative* than the live site because they're intentionally documented.

4. **Screenshot what loaded.** Even a partial page load may reveal enough for visual analysis. Screenshot before the block triggered.

5. **Mark blocked pages in output.** In the Design DNA Document, note which pages couldn't be accessed: `> Note: [page] was blocked by bot protection. [Section] sourced from [public docs / partial load / inference].`

---

## Pages Not Found

If a standard page (like `/about` or `/pricing`) returns 404 or doesn't exist:

- Check the nav for the actual URL — the page may be at `/company`, `/team`, `/plans`, or `/products`
- Use `mcp__claude-in-chrome__find` to search the nav for links
- Skip the page and continue with the remaining crawl list — 3-4 pages is enough for a solid analysis
- Never fabricate content for a page that wasn't crawled

---

## SPA / React / Next.js Sites

**Symptom:** Page appears blank or partially loaded immediately after navigation.

**Fix:** Wait 2-3 seconds after navigation before running JavaScript extraction or taking screenshots. SPAs need time to hydrate. If content still hasn't loaded, scroll down the page — this often triggers React lazy-loading.

---

## CSS-in-JS / No CSS Variables

**Symptom:** The extraction script returns an empty `cssVars` object. The brand uses CSS-in-JS (styled-components, Emotion) or Tailwind without CSS variables.

**Resolution:**
- Fall back to `computed` styles — these are always populated from actual rendered elements regardless of how CSS is authored
- The `topColors` frequency map is especially valuable here — cluster the colors manually into semantic roles
- Look for a `data-theme` attribute on `<html>` or `<body>` which may hold design tokens even if `:root` doesn't

---

## Custom / Paid Fonts

**Symptom:** Font name detected in CSS is not available on Google Fonts or Fontsource (e.g., Söhne, Graphik, GT Walsheim, Roobert, Neue Haas Grotesk, Canela, etc.)

**Format in output:**
```css
--font-display: 'Söhne', sans-serif;
/*
  PAID FONT: Söhne is a licensed typeface by Klim Type Foundry.
  It requires a commercial license: [source if known]

  Open-source alternative: 'Inter' — closest match for proportions and weight range.
  Install: npm install @fontsource/inter
  Note: Söhne has more optical corrections at large sizes than Inter.
*/
```

**Common paid fonts and their best open-source alternatives:**

| Paid Font | Closest Open-Source Alternative | Notes |
|-----------|--------------------------------|-------|
| Söhne | Inter | Very close in proportions |
| Graphik | Inter | Similar neutral grotesque |
| GT Walsheim | Nunito Sans | More geometric feel |
| Neue Haas Grotesk | Inter or Helvetica system | System Helvetica if acceptable |
| Canela | Playfair Display | Similar display serif warmth |
| Roobert | DM Sans | Similar rounded feel |
| Founders Grotesk | Work Sans | Similar proportions |
| National | IBM Plex Sans | Similar legibility approach |
| Tiempos | Lora | Similar editorial serif quality |
| Domaine | Cormorant | Similar luxury serif character |

---

## Insufficient Data for a Section

If you genuinely cannot determine a value for a token (not enough visual evidence, conflicting signals, or page was blocked):

- Use `/* VERIFY */` comment inline: `--color-primary: /* VERIFY */;`
- In the replication guide, flag it: `> Note: Primary color could not be confirmed. Visually appears to be a deep blue (#0f172a range) — verify against live site.`
- Never fabricate a value and present it as extracted data

---

## Gradients as Primary Colors

Some brands (Linear, Vercel's older brand, etc.) use gradients as their primary brand element rather than flat colors.

**When the primary brand color is a gradient:**
```css
/* Primary is a gradient, not a flat color */
--gradient-brand: linear-gradient(135deg, #[hex1] 0%, #[hex2] 50%, #[hex3] 100%);

/* For contexts requiring a single color (text, small elements): */
--color-primary: #[dominant hex from gradient];     /* use the midpoint or most prominent stop */
--color-primary-start: #[hex1];                     /* gradient start */
--color-primary-end: #[hex2];                       /* gradient end */
```

---

## Very Small or Single-Page Sites

If the brand has fewer than 3 pages to crawl (landing page only, or under-construction site):

- Do a deeper analysis of the single page — scroll through all sections and screenshot each
- Use WebSearch to find any public brand materials, press kits, or design system docs
- Note in output: `> Limited pages available for analysis. Token confidence: Medium. Recommend verifying tokens against [any other touchpoints — app, social, docs].`

---

## Dark-Mode-First Sites

If the site's default is dark mode (Vercel, Linear, many dev tools):

- Extract tokens from the dark theme as the canonical tokens (they're the primary experience)
- If a light mode toggle exists, also extract light mode tokens and include both sets
- In the Color System section, clearly label which set is default: `/* Default theme: DARK */`
