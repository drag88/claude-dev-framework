---
description: "Git operations with intelligent commit messages and workflow optimization"
---

# /cdf:git - Git Operations

## Triggers
- Git repository operations: status, add, commit, push, pull, branch
- Need for intelligent commit message generation
- Repository workflow optimization requests
- Branch management and merge operations

## Usage
```
/cdf:git [operation] [args] [--interactive]
```

## Behavioral Flow
1. **Analyze**: Check repository state and working directory changes
2. **Route**: Commit operations delegate to `compound-engineering:ce-commit`; status, branch, merge, and other non-commit operations stay native.
3. **Validate**: Ensure operation is appropriate for current Git context
4. **Execute**: Run the native Git operation or delegated commit flow
5. **Report**: Provide status and next steps guidance

Key behaviors:
- Commit operations require the compound-engineering plugin and the `compound-engineering:ce-commit` host skill
- Apply consistent branch naming conventions
- Handle merge conflicts with guided resolution
- Provide clear status summaries and workflow recommendations

## Delegation: compound-engineering

Commit operations delegate to the `compound-engineering:ce-commit` host skill.

**Requires**: the compound-engineering plugin. If it is not installed, stop and tell the user to install the compound-engineering plugin for their host (install commands are in the README) — do not improvise a replacement flow.

**Flow**: Invoke the `compound-engineering:ce-commit` host skill, passing the user's arguments, selected files, and any flags as context.

**CDF constraints (bind on top of the skill)**:
- Use conventional commit format.
- Do not include AI attribution of any kind.
- Keep non-commit git operations native to this command.

## Tool Coordination
- **Bash**: Git command execution and repository operations
- **Read**: Repository state analysis and configuration review
- **Grep**: Log parsing and status analysis
- **Host skill**: Commit creation through `compound-engineering:ce-commit`

## Key Patterns
- **Commit Delegation**: Commit request → `compound-engineering:ce-commit`
- **Status Analysis**: Repository state → actionable recommendations
- **Branch Strategy**: Consistent naming and workflow enforcement
- **Error Recovery**: Conflict resolution and state restoration guidance

## Commit Message Rules

### No Claude Attribution
Do NOT include Claude attribution in commits:
```
# BAD - Don't include this:
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Conventional Format
Follow conventional commit format:
- `feat:` - new feature
- `fix:` - bug fix
- `docs:` - documentation
- `refactor:` - code refactoring
- `test:` - adding tests
- `chore:` - maintenance

### Message Guidelines
- Use imperative mood ("Add feature" not "Added feature")
- Keep subject line under 50 characters
- Add body for complex changes explaining WHY, not WHAT
- Reference issue numbers when applicable

## Examples

### Smart Status Analysis
```
/cdf:git status
# Analyzes repository state with change summary
# Provides next steps and workflow recommendations
```

### Interactive Operations
```
/cdf:git merge feature-branch --interactive
# Guided merge with conflict resolution assistance
```

## Boundaries

**Will:**
- Execute Git operations with intelligent automation
- Delegate commit creation to `compound-engineering:ce-commit`
- Provide workflow optimization and best practice guidance

**Will Not:**
- Modify repository configuration without explicit authorization
- Execute destructive operations without confirmation
- Handle complex merges requiring manual intervention
