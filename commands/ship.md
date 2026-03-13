---
description: "Fully automated release pipeline: merge main, test, review, commit, push, and open PR in one command"
---

# /cdf:ship — Automated Release Pipeline

You are running the `/cdf:ship` workflow. This is **non-interactive and fully automated**. Do NOT ask for confirmation at any step. The user said `/cdf:ship` which means DO IT.

**Only stop for:**
- On `main` branch (abort)
- Merge conflicts that can't be auto-resolved
- Test failures
- CRITICAL review findings (one question per issue with fix recommendation)

**Never stop for:**
- Uncommitted changes (always include them)
- Commit message approval
- PR body content

## Step 1: Pre-flight

1. Check current branch. If on `main`, **abort**: "You're on main. Ship from a feature branch."
2. Run `git status` (never use `-uall`). Uncommitted changes are always included.
3. Run `git diff main...HEAD --stat` and `git log main..HEAD --oneline` to understand what's being shipped.
4. Print a brief summary of what will be shipped.

## Step 2: Merge origin/main

Merge latest main so tests run against the merged state:

```bash
git fetch origin main && git merge origin/main --no-edit
```

If merge conflicts: try auto-resolve for simple cases (lock files, generated files). If complex or ambiguous, **STOP** and show conflicts.

If already up to date: continue silently.

## Step 3: Run Tests

Detect and run the project's test suite. Check for these in order:

1. `package.json` → look for `test`, `test:unit`, `test:integration` scripts
2. `pytest.ini`, `pyproject.toml`, `setup.cfg` → run `pytest`
3. `Gemfile` → run `bundle exec rspec` or `bin/rails test`
4. `Makefile` → look for `test` target
5. `go.mod` → run `go test ./...`

Run all discovered test suites. If multiple exist (e.g., backend + frontend), run them in parallel.

**If any test fails:** Show failures and **STOP**. Do not proceed.
**If all pass:** Note counts briefly and continue.

## Step 4: Pre-Landing Review

Review the diff for structural issues tests don't catch.

1. Get full diff: `git diff origin/main`

2. Two-pass review:
   - **Pass 1 (CRITICAL):** SQL injection (string interpolation in queries), race conditions (check-then-set without atomicity, find_or_create without unique index), XSS (html_safe/raw on user data), LLM trust boundary (unvalidated LLM outputs persisted to DB)
   - **Pass 2 (INFORMATIONAL):** Conditional side effects (branches forgetting effects), dead code, test gaps, magic numbers, type coercion at boundaries

3. Output: `Pre-Landing Review: N issues (X critical, Y informational)`

4. For each CRITICAL issue: separate question with:
   - Problem (`file:line` + description)
   - Recommended fix
   - Options: A) Fix now (recommend), B) Acknowledge and ship, C) False positive

   If user chose A on any issue: apply fixes, commit them (`fix: apply pre-landing review fixes`), then **STOP** and tell user to run `/cdf:ship` again.

5. If only informational or no issues: continue.

## Step 5: Commit

Create bisectable commits — logical groups, not one-file-per-commit.

**Ordering** (dependencies first):
1. Infrastructure: migrations, config, routes
2. Models & services (with their tests)
3. Controllers, views, components (with their tests)
4. Everything else

**Rules:**
- A module and its test file go in the same commit
- If total diff is small (<50 lines across <4 files), single commit is fine
- Each commit must be independently valid — no broken imports
- Conventional format: `feat:`, `fix:`, `chore:`, `refactor:`, `docs:`
- No Claude attribution in commit messages

## Step 6: Push

```bash
git push -u origin $(git branch --show-current)
```

## Step 7: Create PR

```bash
gh pr create --title "<type>: <summary>" --body "$(cat <<'EOF'
## Summary
<bullet points describing what changed and why>

## Pre-Landing Review
<findings from Step 4, or "No issues found.">

## Tests
- All tests pass (N tests)

EOF
)"
```

Output the PR URL — this is the final output the user sees.

## Important Rules

- **Never skip tests.** If tests fail, stop.
- **Never force push.** Regular `git push` only.
- **Never ask for confirmation** except for CRITICAL review findings.
- **Detect the project's test runner** — don't assume any specific framework.
- **Goal: user says `/cdf:ship`, next thing they see is the review + PR URL.**

## When to Use

Use `/cdf:ship` when:
- Feature is complete and ready for PR
- All code changes are on a feature branch
- You want the full ceremony: merge main → test → review → commit → push → PR

**Don't use this command for**: Work-in-progress code, draft PRs, or when you need manual control over the commit structure.

## Next Commands
- `/cdf:verify` — Run quality checks without shipping
- `/cdf:git` — Manual git operations with smart commit messages
