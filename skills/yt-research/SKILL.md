---
name: yt-research
description: YouTube research pipeline — searches YouTube videos on a topic, feeds them into NotebookLM as sources, generates an analysis, then creates an infographic with Nano Banana Pro. Activates when asked to "research X on YouTube", "find YouTube videos about X and create an infographic", or "YouTube research pipeline".
---

# YouTube Research Pipeline

Chains three tools: YouTube search → NotebookLM analysis → Nano Banana Pro infographic.

**Note on transcripts:** NotebookLM natively processes full YouTube transcripts via Google's caption system — no manual transcript download needed. The analysis quality reflects the complete spoken content of every video.

**Output location:** `./output/{topic-slug}/` (configurable — set a custom output directory if needed)

---

## Parameters

| Parameter | Default | Options | Notes |
|-----------|---------|---------|-------|
| topic | required | — | The research topic |
| count | 5 | 1–20 | Number of YouTube videos |
| style | `blueprint` | see Style Presets below | Visual style of the infographic |
| detail | `high` | `high` / `medium` / `low` | How much content to include |
| resolution | `2K` | `1K` / `2K` / `4K` | Image resolution |

---

## Style Presets

When the user specifies a style, use the matching prompt template in Step 5.

### `blueprint` (default)
Deep navy blue background, white and cyan hand-sketched lines, rough pencil textures, faint grid overlay, compass rose, ruler tick marks, revision block. All text looks hand-lettered like engineering drawings.

### `newspaper`
Black/white/red palette. Broadsheet column layout, bold serif headlines, pull-quote boxes, dateline, byline, column dividers. Feels like a front page feature story.

### `neon`
Dark charcoal/black background, glowing neon accents (pink, green, electric blue). Sharp geometric layout, cyberpunk grid lines, stats in oversized glowing numerals. High contrast.

### `minimal`
Clean white background, single muted accent color (slate blue or warm orange), generous whitespace, sans-serif typography hierarchy. No decoration — content only.

### `vintage-poster`
Warm amber/cream/brown palette, Art Deco geometric borders, retro illustration style, bold display fonts, ornamental dividers. Feels like a 1930s exhibition poster.

---

## Detail Levels

| Level | What's included | Prompt guidance |
|-------|----------------|-----------------|
| `high` | All 5 insights + all stats + all trends + all takeaways + decorative elements + source label | Full prompt, all sections, dense content |
| `medium` | Top 3 insights + key stats only + top 3 trends + takeaways as footer | Trimmed prompt, 3 sections, minimal decoration |
| `low` | Single column, 4–5 bullet summary only | Compact prompt, one section, no decoration |

---

## Step-by-Step Workflow

### Step 1 — YouTube Search (auto, no confirmation needed)

```bash
python3 ~/.claude/skills/yt-research/youtube_search.py "{topic}" {count}
```

Display results in a table: title, channel, views, duration, date.

**Then ask:** "Found {N} videos. Should I proceed to add these to NotebookLM and generate a `{style}` infographic at `{detail}` detail?"

Wait for confirmation before continuing.

---

### Step 2 — Create NotebookLM notebook (ask before running)

```bash
notebooklm create "Research: {topic}"
```

Save the notebook ID from the output.

---

### Step 3 — Add YouTube sources (ask before running)

Add each URL from Step 1:
```bash
notebooklm source add "{url}" -n {notebook_id}
```

Wait for all sources in parallel — one `source wait` call per source ID:
```bash
notebooklm source wait {source_id} -n {notebook_id} --timeout 600 &
```
Run all in background, then `wait` for all to complete.

---

### Step 4 — Get research analysis from NotebookLM (ask before running)

Adapt the question based on `detail` level:

**high / medium:**
```bash
notebooklm ask "Analyze these videos and return a structured research summary with:
1. TOP 5 KEY INSIGHTS (one sentence each, specific and concrete)
2. KEY STATISTICS & NUMBERS mentioned across the videos
3. EMERGING TRENDS (what topics/approaches are gaining traction)
4. ACTIONABLE TAKEAWAYS (3-5 things someone could do right now)
Keep it dense and factual — this will be used as the basis for an infographic." -n {notebook_id}
```

**low:**
```bash
notebooklm ask "Give me a 4-5 bullet summary of the most important things covered across these videos. Be concrete and specific." -n {notebook_id}
```

Capture the full text output for Step 5.

---

### Step 5 — Generate infographic with Nano Banana Pro (ask before running)

**IMPORTANT:** Invoke the `nano-banana-pro` skill before this step using the Skill tool — do not call the script directly without loading it first.

**Build the output path:**
- Topic slug: lowercase, spaces → hyphens (e.g. "AI Agents 2026" → `ai-agents-2026`)
- Create directory: `./output/{topic-slug}/`
- Filename: `{yyyy-mm-dd-hh-mm-ss}-{style}-infographic.png`

**Build the image prompt** by combining:
1. The style prompt template from the Style Presets section above
2. The NotebookLM analysis content
3. The detail level (controls how many sections/elements to include)
4. Title: `"{topic} — KEY INSIGHTS"` (or appropriate variant)
5. Footer source label: `"Based on {count} YouTube videos · NotebookLM + Nano Banana Pro"`

**Run via the nano-banana-pro skill:**
```bash
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "{assembled_prompt}" \
  --filename "./output/{topic-slug}/{timestamp}-{style}-infographic.png" \
  --resolution {resolution}
```

---

### Step 6 — Report to user

- NotebookLM notebook ID: `{notebook_id}` (for follow-up: `notebooklm use {notebook_id}`)
- Full path of saved infographic
- Offer follow-ups: "Want a different style, higher detail, or a podcast/report from the same notebook?"

---

## Timing Guide

| Step | Typical Time |
|------|-------------|
| YouTube search | 15–30s |
| Source processing | 1–5 min |
| NotebookLM analysis | 30–60s |
| Infographic generation | 30–90s |
| **Total** | **~3–8 min** |

---

## Error Handling

- **yt-dlp not found:** `uv tool install yt-dlp`
- **notebooklm auth error:** `notebooklm login` then retry
- **Source processing timeout:** Retry `notebooklm source wait {source_id}`
- **Nano Banana Pro API error:** Check `GEMINI_API_KEY` is set in `~/.zshrc`
- **NotebookLM rate limit:** Wait 5–10 min, retry the `notebooklm ask` step
