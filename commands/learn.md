---
description: "Mid-session pattern extraction and continuous learning"
---

# /cdf:learn - Continuous Learning

## Triggers
- Mid-session pattern extraction requests
- Knowledge capture for future sessions
- Learning new patterns from current work
- Skill and rule generation needs

## Usage
```
/cdf:learn [--type patterns|rules|skills] [--scope session|project|global]
```

## Arguments
- `--type`: What to extract (default: patterns)
  - `patterns`: Code patterns and solutions discovered
  - `rules`: Project-specific rules and conventions
  - `skills`: Reusable skills from workflows
- `--scope`: Where to save learnings (default: project)
  - `session`: Current session only
  - `project`: Project's .claude/ directory
  - `global`: User's global Claude config

## Behavioral Flow

### 1. Analyze Current Session
Review the current session to identify:
- Problems solved and their solutions
- Patterns used repeatedly
- Project-specific conventions discovered
- Tools and commands that worked well

### 2. Extract Learnings
Categorize discoveries into:

#### Code Patterns
```markdown
## Pattern: [Name]
**Context**: When to use this pattern
**Problem**: What problem it solves
**Solution**: Code or approach
**Example**: Concrete implementation
```

#### Project Rules
```markdown
## Rule: [Name]
**Type**: Convention | Requirement | Best Practice
**Applies To**: [file patterns or contexts]
**Rule**: What to do or avoid
**Rationale**: Why this rule exists
```

#### Workflow Skills
```markdown
## Skill: [Name]
**Trigger**: When to activate
**Steps**: Numbered workflow steps
**Tools**: Tools to use
**Output**: Expected result
```

### 3. Persist Learnings

Save to appropriate location:
- Session: Memory only
- Project: `.claude/learnings/`
- Global: `~/.claude/learnings/`

### 4. Apply in Future

Learnings are automatically loaded in future sessions:
- Patterns inform implementation choices
- Rules guide behavior
- Skills activate on relevant triggers

## Examples

### Extract Session Patterns
```
/cdf:learn --type patterns
```

Output:
```markdown
## Patterns Discovered This Session

### 1. Error Boundary with Retry
**Context**: React components with async data fetching
**Solution**: Wrap with ErrorBoundary + retry button
**Used in**: Dashboard, UserProfile, OrderHistory

### 2. Optimistic Updates
**Context**: Form submissions with immediate feedback
**Solution**: Update UI before API confirms, rollback on error
**Used in**: TodoList, CommentForm
```

### Generate Project Rules
```
/cdf:learn --type rules --scope project
```

Output:
```markdown
## Rules Extracted from Session

### R001: API Response Typing
**Applies To**: src/api/**/*.ts
**Rule**: All API functions must return typed responses using ApiResponse<T>
**Rationale**: Discovered multiple untyped API calls causing runtime errors

### R002: Component File Structure
**Applies To**: src/components/**/*.tsx
**Rule**: Each component directory must contain: Component.tsx, Component.test.tsx, index.ts
**Rationale**: Consistent structure makes navigation easier
```

### Create Reusable Skill
```
/cdf:learn --type skills
```

Output:
```markdown
## Skill: Database Migration Workflow

**Trigger**: "create migration", "add database field"

**Steps**:
1. Generate migration file with timestamp
2. Add up() and down() methods
3. Run migration locally
4. Add seed data if needed
5. Update TypeScript types
6. Run tests to verify

**Tools**: Bash (migration commands), Edit (migration files)

**Saved to**: .claude/skills/database-migration/
```

## MCP Integration
- **Memory MCP**: Persist learnings across sessions
- **Serena MCP**: Store project-specific knowledge

## Tool Coordination
- **Read**: Analyze files modified during session
- **Grep**: Find patterns across codebase
- **Write**: Save learning documentation

## Learning Categories

### Technical Patterns
- Architectural decisions and their rationale
- Code patterns that solved specific problems
- Integration approaches that worked

### Process Knowledge
- Effective debugging strategies
- Testing approaches for this project
- Deployment and release procedures

### Project Context
- Domain terminology and concepts
- Team conventions and preferences
- External dependencies and their quirks

## Boundaries

**Will:**
- Extract valuable patterns from current session
- Generate rules based on discovered conventions
- Create reusable skills from workflows
- Persist learnings for future sessions

**Will Not:**
- Modify production code during learning extraction
- Generate learnings without session context
- Override existing project rules without confirmation
- Share project-specific learnings globally without consent
