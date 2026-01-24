# Git Workflow Rules Template

Copy this template to `.claude/rules/git-workflow.md` and customize for your project.

---

## Branch Naming

### Format
```
<type>/<ticket>-<description>

Examples:
feature/PROJ-123-user-authentication
fix/PROJ-456-login-timeout
refactor/PROJ-789-cleanup-utils
```

### Types
- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation only
- `test/` - Test additions/fixes
- `chore/` - Build, config, dependencies

---

## Commit Messages

### Conventional Commits Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting (no code change)
- `refactor` - Refactoring (no feature/fix)
- `test` - Tests
- `chore` - Build, tools, dependencies

### Examples
```bash
feat(auth): add OAuth2 login support

Implemented OAuth2 flow with Google and GitHub providers.
- Added OAuth strategy selection
- Created callback handlers
- Updated user model for social login

Closes #123

---

fix(api): prevent timeout on large file uploads

Increased upload timeout from 30s to 5min for files > 10MB.

Fixes #456
```

### Rules
- Subject line max 72 characters
- Use imperative mood ("add" not "added")
- No period at end of subject
- Body wrapped at 72 characters
- Reference issues in footer

---

## Pull Request Guidelines

### PR Title
Follow same format as commits:
```
feat(auth): add OAuth2 login support
```

### PR Description Template
```markdown
## Summary
[Brief description of changes]

## Changes
- [Change 1]
- [Change 2]

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots
[If applicable]

## Related Issues
Closes #123
```

### PR Size Limits
- Max 500 lines changed (excluding tests)
- Max 10 files changed
- Split larger changes into multiple PRs

---

## Protected Branches

### main/master
- No direct pushes
- Require PR with approval
- Require passing CI
- Require up-to-date branch

### develop (if used)
- No direct pushes
- Require PR with approval
- Require passing CI

---

## Review Requirements

### Required Reviewers
- At least 1 approval required
- Code owner approval for:
  - `src/auth/*` - Security team
  - `src/api/*` - API team lead
  - `*.config.*` - DevOps

### Review Checklist
- [ ] Code follows style guide
- [ ] Tests cover new code
- [ ] No security issues
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

---

## Merge Strategy

### Preferred: Squash and Merge
- Single commit on main
- Clean history
- PR description becomes commit body

### When to Rebase
- Multiple logical commits that should be preserved
- Work that spans multiple features

### Never
- Regular merge commits
- Force push to protected branches

---

## Release Process

### Version Tagging
```bash
# Semantic versioning
v1.2.3

# Pre-release
v1.2.3-beta.1
v1.2.3-rc.1
```

### Release Branch (if used)
```bash
release/v1.2.0
```

### Hotfix Process
```bash
# Branch from main
git checkout -b hotfix/PROJ-999-critical-fix main

# After fix, merge to main AND develop
```

---

## Git Hygiene

### Before Push
- [ ] Run tests locally
- [ ] Run linter
- [ ] Check for console.log
- [ ] Review own changes

### Avoid
- Committing `.env` or secrets
- Committing `node_modules`
- Committing build artifacts
- Force pushing to shared branches
- Rewriting public history

### Clean Up
- Delete branches after merge
- Archive stale branches (> 3 months)
