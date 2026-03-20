---
name: running-retrospectives
description: "Engineering retrospective analyzing git history for velocity, work patterns, quality signals, and trends with persistent snapshots"
---

# /retro — Engineering Retrospective

Generates a comprehensive engineering retrospective from git history. Surfaces velocity, patterns, and quality signals that are invisible in day-to-day work.

## When to Activate

- User types `/retro`
- User asks for "weekly metrics", "engineering stats", "how productive was I", "shipping velocity"

## Arguments

- `/retro` — default: last 7 days
- `/retro 24h` — last 24 hours
- `/retro 14d` — last 14 days
- `/retro 30d` — last 30 days
- `/retro compare` — compare current window vs prior same-length window
- `/retro compare 14d` — compare with explicit window

Validate argument format: number + `d`/`h`/`w`, or `compare` optionally followed by window. If invalid, show usage and stop.

## Instructions

### Step 1: Gather Raw Data

Fetch origin first, then run ALL git commands in parallel:

```bash
git fetch origin --quiet

# 1. Commits with stats
git log origin/main --since="<window>" --format="%H|%ai|%s" --shortstat

# 2. Per-commit test vs production LOC (test/|spec/|__tests__/ = test files)
git log origin/main --since="<window>" --format="COMMIT:%H" --numstat

# 3. Timestamps for session detection
git log origin/main --since="<window>" --format="%at|%ai|%s" | sort -n

# 4. Hotspot analysis
git log origin/main --since="<window>" --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn

# 5. PR numbers from commit messages
git log origin/main --since="<window>" --format="%s" | grep -oE '#[0-9]+' | sed 's/^#//' | sort -n | uniq | sed 's/^/#/'
```

### Step 2: Compute Metrics

Present as summary table:

| Metric | Value |
|--------|-------|
| Commits to main | N |
| PRs merged | N |
| Total insertions | N |
| Total deletions | N |
| Net LOC added | N |
| Test LOC (insertions) | N |
| Test LOC ratio | N% |
| Active days | N |
| Detected sessions | N |
| Avg LOC/session-hour | N |

### Step 3: Commit Time Distribution

Hourly histogram with bar chart:
```
Hour  Commits  ████████████████
 00:    4      ████
 07:    5      █████
```

Call out: peak hours, dead zones, bimodal patterns, late-night clusters (after 10pm).

### Step 4: Work Session Detection

Detect sessions using **45-minute gap** between consecutive commits. Classify:
- **Deep sessions** (50+ min)
- **Medium sessions** (20-50 min)
- **Micro sessions** (<20 min)

Calculate: total active time, average session length, LOC per hour of active time.

### Step 5: Commit Type Breakdown

Categorize by conventional commit prefix (feat/fix/refactor/test/chore/docs):
```
feat:     20  (40%)  ████████████████████
fix:      27  (54%)  ███████████████████████████
refactor:  2  ( 4%)  ██
```

Flag if fix ratio exceeds 50% — signals "ship fast, fix fast" pattern.

### Step 6: Hotspot Analysis

Top 10 most-changed files. Flag:
- Files changed 5+ times (churn hotspots)
- Test files vs production files in the list
- Config/version files (discipline indicator)

### Step 7: PR Size Distribution

Bucket by LOC changed:
- **Small** (<100 LOC)
- **Medium** (100-500 LOC)
- **Large** (500-1500 LOC)
- **XL** (1500+ LOC) — flag with file counts

### Step 8: Focus Score + Ship of the Week

**Focus score:** % of commits touching single most-changed top-level directory. Higher = deeper focused work.

**Ship of the week:** Highest-LOC PR — number, title, LOC, why it matters.

### Step 9: Week-over-Week Trends (if window >= 14d)

Split into weekly buckets: commits, LOC, test ratio, fix ratio, session count.

### Step 10: Streak Tracking

Consecutive days with at least 1 commit, counting back from today:
```bash
git log origin/main --format="%ad" --date=format:"%Y-%m-%d" | sort -u
```

Display: "Shipping streak: N consecutive days"

### Step 11: Load History & Compare

Check for prior retro snapshots:
```bash
ls -t .context/retros/*.json 2>/dev/null
```

If prior retros exist, load most recent and show delta table:
```
                    Last        Now         Delta
Test ratio:         22%    →    41%         +19pp
Sessions:           10     →    14          +4
LOC/hour:           200    →    350         +75%
Fix ratio:          54%    →    30%         -24pp (improving)
```

If first retro, note: "First retro recorded — run again next week to see trends."

### Step 12: Save Retro History

```bash
mkdir -p .context/retros
```

Save JSON snapshot to `.context/retros/YYYY-MM-DD-N.json`:
```json
{
  "date": "2026-03-13",
  "window": "7d",
  "metrics": {
    "commits": 47,
    "prs_merged": 12,
    "insertions": 3200,
    "deletions": 800,
    "net_loc": 2400,
    "test_loc": 1300,
    "test_ratio": 0.41,
    "active_days": 6,
    "sessions": 14,
    "deep_sessions": 5,
    "avg_session_minutes": 42,
    "loc_per_session_hour": 350,
    "feat_pct": 0.40,
    "fix_pct": 0.30,
    "peak_hour": 22
  },
  "streak_days": 47,
  "tweetable": "Week of Mar 8: 47 commits, 3.2k LOC, 41% tests, 12 PRs, peak: 10pm"
}
```

### Step 13: Write the Narrative

Output directly to conversation (NOT to files except the JSON snapshot).

Structure:

**Tweetable summary** (first line):
```
Week of Mar 8: 47 commits, 3.2k LOC, 41% tests, 12 PRs, peak: 10pm | Streak: 47d
```

Then:
1. **Summary Table** (from Step 2)
2. **Trends vs Last Retro** (from Step 11, skip if first)
3. **Time & Session Patterns** — when productive hours are, session trends, estimated active hours/day
4. **Shipping Velocity** — commit type mix, PR size discipline, fix-chain detection, version bump discipline
5. **Code Quality Signals** — test ratio trend, hotspot churn, XL PRs that should have been split
6. **Focus & Highlights** — focus score with interpretation, ship of the week
7. **Top 3 Wins** — highest-impact things shipped, why they matter, what's impressive
8. **3 Things to Improve** — specific, actionable, anchored in actual commits
9. **3 Habits for Next Week** — small, practical, <5 minutes to adopt
10. **Week-over-Week Trends** (if applicable)

## Compare Mode

When `/retro compare` or `/retro compare 14d`:
1. Compute current window metrics using `--since`
2. Compute prior same-length window using `--since` and `--until` to avoid overlap
3. Side-by-side comparison table with deltas
4. Narrative highlighting biggest improvements and regressions
5. Save only current-window snapshot

## Tone

- Encouraging but candid, no coddling
- Specific — always anchor in actual commits/code
- Skip generic praise ("great job!") — say exactly what was good and why
- Frame improvements as leveling up, not criticism
- 2500-3500 words total
- Markdown tables and code blocks for data, prose for narrative

## Important Rules

- Use `origin/main` for all git queries (not local main)
- If zero commits in window, say so and suggest different window
- Round LOC/hour to nearest 50
- Treat merge commits as PR boundaries
- ALL narrative output goes to conversation — only file written is `.context/retros/` JSON
- On first run, skip comparison gracefully
- Do not read CLAUDE.md — this skill is self-contained
