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

Delegate pre-landing diff review to the `compound-engineering:ce-code-review` host skill.

**Requires**: the compound-engineering plugin. If it is not installed, stop and tell the user to install the compound-engineering plugin for their host (install commands are in the README) — do not improvise a replacement flow.

Pass the diff from `git diff origin/main` and request report-only review output. CDF handles any follow-up fixes.

For each CRITICAL issue: separate question with:
   - Problem (`file:line` + description)
   - Recommended fix
   - Options: A) Fix now (recommend), B) Acknowledge and ship, C) False positive

If user chose A on any issue: apply fixes, commit them through `compound-engineering:ce-commit-push-pr` as a fix commit, then **STOP** and tell user to run `/cdf:ship` again.

If only informational or no issues: continue.

## Step 5: Commit, Push, and Create PR

Delegate to the `compound-engineering:ce-commit-push-pr` host skill **once** — a single invocation runs commit, push, and PR creation end to end. Pass the test results, review findings, branch, and diff context.

**CDF constraints (bind on top of the skill)**:
- Preserve the pre-flight, merge-main, tests, and abort conditions above.
- Use conventional commit format.
- Do not include AI attribution of any kind.

Output the PR URL — this is the final output the user sees.

If the shipped work solved a non-obvious problem, capture the learning with the `compound-engineering:ce-compound` host skill after the PR is open.

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
