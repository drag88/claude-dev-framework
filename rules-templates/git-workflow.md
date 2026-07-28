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
`feature/` · `fix/` · `refactor/` · `docs/` · `test/` · `chore/`

---

## Commit Messages

### Conventional Commits Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
`feat` · `fix` · `docs` · `style` · `refactor` · `test` · `chore`

### Example
```bash
feat(auth): add OAuth2 login support

Implemented OAuth2 flow with Google and GitHub providers.

Closes #123
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

### PR Size
Keep a PR to one reviewable idea; split when the reviewer would need two mental models.

---

## Merge Strategy

### Preferred: Squash and Merge
- Single commit on main
- Clean history
- PR description becomes commit body

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

### Avoid
- Committing `.env` or secrets
- Committing `node_modules`
- Committing build artifacts
- Force pushing to shared branches
- Rewriting public history

### Clean Up
- Delete branches after merge
- Archive stale branches (> 3 months)
