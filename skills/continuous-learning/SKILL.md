# Continuous Learning Skill

Automatically extract and persist valuable patterns discovered during development sessions.

## When to Activate

- At session end (via Stop hook)
- When significant problem is solved
- When user says "remember this", "save this pattern", or similar
- After completing complex multi-step tasks

## Learning Categories

### 1. Code Patterns
Reusable solutions to common problems.

```markdown
## Pattern: [Descriptive Name]

**Context**: [When this pattern applies]
**Problem**: [What problem it solves]
**Solution**:
\`\`\`typescript
// Code snippet or approach
\`\`\`
**Trade-offs**: [Pros and cons]
**Related**: [Similar patterns or alternatives]
```

### 2. Project Rules
Conventions and requirements specific to the project.

```markdown
## Rule: [Rule Name]

**ID**: RULE-001
**Type**: Convention | Requirement | Best Practice
**Applies To**: [File patterns, contexts]
**Rule**: [What to do or avoid]
**Rationale**: [Why this rule exists]
**Enforcement**: Auto-check | Manual review | Warning only
```

### 3. Workflow Skills
Multi-step procedures that can be automated.

```markdown
## Skill: [Skill Name]

**Trigger**: [When to activate]
**Prerequisites**: [What must be true before running]
**Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]
**Output**: [Expected result]
**Cleanup**: [Any cleanup needed]
```

### 4. Context Knowledge
Domain-specific information about the project.

```markdown
## Context: [Topic]

**Domain**: [Business domain]
**Terminology**:
- Term 1: Definition
- Term 2: Definition
**Key Concepts**: [Important domain concepts]
**Business Rules**: [Domain-specific rules]
```

## Extraction Process

### During Session
1. **Observe**: Note problems solved and approaches used
2. **Identify**: Recognize patterns in solutions
3. **Document**: Capture with context and rationale
4. **Tag**: Categorize for retrieval

### At Session End
1. **Review**: Scan session for undocumented learnings
2. **Consolidate**: Merge similar patterns
3. **Persist**: Save to appropriate scope
4. **Index**: Update learning index for quick retrieval

## Storage Locations

### Session Scope
- Memory only, not persisted
- Used for temporary working knowledge

### Project Scope
```
.claude/
├── learnings/
│   ├── patterns/
│   │   ├── error-handling.md
│   │   └── state-management.md
│   ├── rules/
│   │   ├── naming-conventions.md
│   │   └── file-structure.md
│   └── skills/
│       └── deployment/
│           └── SKILL.md
└── learning-index.md
```

### Global Scope
```
~/.claude/
├── learnings/
│   ├── patterns/
│   └── skills/
└── learning-index.md
```

## Pattern Detection Heuristics

### Indicators of Valuable Patterns
- Solution required multiple iterations
- Problem was solved elegantly after struggle
- Approach could apply to other contexts
- User expressed satisfaction with solution
- Pattern was used multiple times in session

### Indicators of Rule Candidates
- Correction made multiple times
- Convention discovered through trial/error
- Explicit project requirement identified
- Anti-pattern consistently avoided

### Indicators of Skill Candidates
- Multi-step workflow completed successfully
- Process has clear trigger and outcome
- Steps are largely deterministic
- Workflow is likely to repeat

## Learning Index Format

```markdown
# Learning Index

## Recently Added
| Date | Type | Name | Scope |
|------|------|------|-------|
| 2024-01-15 | Pattern | Error Boundary | Project |
| 2024-01-15 | Rule | API Response Types | Project |

## By Category

### Patterns
- [Error Boundary](patterns/error-boundary.md) - React error handling
- [Optimistic Updates](patterns/optimistic-updates.md) - UI responsiveness

### Rules
- [API Response Types](rules/api-types.md) - Type all API responses
- [Component Structure](rules/component-structure.md) - File organization

### Skills
- [Database Migration](skills/database-migration/) - Schema changes
- [Release Process](skills/release/) - Deployment workflow

## By Project
- **project-a**: 5 patterns, 8 rules, 2 skills
- **project-b**: 3 patterns, 4 rules, 1 skill
```

## Integration with Other Skills

### With context-saver
- Save learnings before context compaction
- Include learning summary in session handoff

### With rules-generator
- Extracted rules inform project rule generation
- Patterns become rule suggestions

### With skill-creator
- Workflow skills can be promoted to formal skills
- Patterns become skill building blocks

## Example Extraction

### Session Context
User implemented authentication with JWT, faced token refresh issues, solved with interceptor pattern.

### Extracted Learning
```markdown
## Pattern: JWT Token Refresh Interceptor

**Context**: API calls with JWT authentication that may expire

**Problem**: Tokens expire during session, causing 401 errors that disrupt user experience

**Solution**:
\`\`\`typescript
// Axios interceptor for automatic token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true;
      const newToken = await refreshToken();
      error.config.headers.Authorization = \`Bearer \${newToken}\`;
      return api(error.config);
    }
    return Promise.reject(error);
  }
);
\`\`\`

**Trade-offs**:
- Pro: Seamless user experience, automatic retry
- Con: Slightly complex, needs careful error handling

**Related**: Token storage patterns, Auth context
```

## Boundary Conditions

### What to Learn
- Solutions that required thought or iteration
- Patterns used multiple times
- Project-specific conventions
- Successful debugging strategies

### What NOT to Learn
- Standard library usage
- Well-documented patterns
- One-off workarounds
- Temporary fixes (mark as such if saved)
