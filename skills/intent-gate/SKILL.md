# Intent Gate Skill

Classify user requests before taking action to ensure appropriate response strategy.

## When to Activate

- At the start of every new user request
- When request scope is unclear
- Before executing potentially large changes
- When multiple valid interpretations exist
- When `/cdf:flow` needs complexity classification

## Flow State Detection

**Before classifying any intent, check if a flow is active:**

1. Look for `dev/active/*/flow-state.md`
2. If found, read the current phase from YAML frontmatter
3. Inject phase context into response strategy

**Active Flow Behavior:**
- If `current_phase: docs` → Planning mode, use `/cdf:docs plan`
- If `current_phase: implement` → Implementation mode, follow task checkboxes
- If `current_phase: verify` → Verification mode, run checks
- If `current_phase: compound` → Knowledge capture mode

**CRITICAL**: When flow is active, do NOT:
- Use EnterPlanMode or `.claude/plans/`
- Skip to implementation without completing docs phase
- Ignore the flow-state.md tracking

## Task Complexity Classification

For `/cdf:flow` and multi-phase workflows, classify task complexity:

### Simple
**Signals**:
- Keywords: "fix", "typo", "update", "correct", "rename", "remove"
- Single-file scope
- Estimated changes < 50 lines
- Clear, specific instructions
- Bug fixes with known location

**Workflow**: docs(lite) -> implement -> verify(quick)

### Standard
**Signals**:
- Keywords: "add", "implement", "create", "extend"
- Multi-file scope (2-5 files)
- Estimated changes 50-500 lines
- Feature additions to existing systems
- Clear requirements

**Workflow**: docs -> implement -> verify -> compound(optional)

### Complex
**Signals**:
- Keywords: "design", "architect", "migrate", "restructure", "refactor"
- Multi-domain scope (>5 files, multiple directories)
- Estimated changes > 500 lines
- New systems or major refactors
- Ambiguous requirements
- Architectural decisions required

**Workflow**: brainstorm -> docs -> implement -> verify -> compound

### Complexity Override
User can override with `--complexity simple|standard|complex` flag.

## Intent Categories

### 1. Trivial
**Signals**: Simple questions, single-file edits, typo fixes, formatting changes
**Response**: Execute directly without planning

Examples:
- "Fix the typo in README.md"
- "What does this function do?"
- "Add a newline at the end of the file"

### 2. Explicit
**Signals**: Specific command given, clear scope, defined outcome
**Response**: Execute the specified command/action

Examples:
- "Run `npm test`"
- "Delete the unused import on line 15"
- "Rename `getUserData` to `fetchUserProfile`"

### 3. Exploratory
**Signals**: Understanding requests, "how does X work", architecture questions
**Response**: Use `/cdf:explain` or `/cdf:analyze` to investigate first

Examples:
- "How does authentication work in this codebase?"
- "What's the data flow for user creation?"
- "Why is this test failing?"

### 4. GitHub Work
**Signals**: PR review, issue triage, commit preparation, branch management
**Response**: Follow full GitHub workflow with proper validation

Examples:
- "Review this PR"
- "Create a commit for my changes"
- "What issues are assigned to me?"

### 5. Ambiguous
**Signals**: Multiple interpretations possible, scope unclear, missing context
**Response**: Ask clarifying questions before proceeding

Examples:
- "Make this better"
- "Fix the bug"
- "Update the tests"

## Classification Process

```
1. Read the full request
2. Identify key action words (fix, add, explain, review, etc.)
3. Assess scope indicators (single file vs. multiple, small vs. large)
4. Check for explicit commands or paths
5. Look for ambiguity markers (vague terms, missing specifics)
6. Classify into category
7. Apply appropriate response strategy
```

## Response Strategies by Category

### Trivial → Direct Execution
```
- Acknowledge briefly
- Execute the action
- Confirm completion
```

### Explicit → Command Execution
```
- Parse the explicit instruction
- Validate parameters
- Execute as specified
- Report results
```

### Exploratory → Research First
```
- Acknowledge the question
- Use appropriate exploration tools
- Synthesize findings
- Present structured answer
```

### GitHub Work → Full Workflow
```
- Identify the GitHub operation type
- Gather necessary context
- Execute with proper checks
- Validate result
```

### Ambiguous → Clarification
```
- Acknowledge the request
- Identify specific ambiguities
- Ask targeted questions
- Wait for clarification before proceeding
```

## Clarification Questions Template

When request is ambiguous, ask:

1. **Scope**: "Should this change affect [specific area] or [broader area]?"
2. **Approach**: "Would you prefer [option A] or [option B]?"
3. **Priority**: "Which aspect is most important: [X], [Y], or [Z]?"
4. **Constraints**: "Are there any constraints I should know about?"

## Anti-Patterns to Avoid

- Assuming scope when it's unclear
- Starting large changes without confirming intent
- Treating exploratory requests as implementation requests
- Ignoring ambiguity and guessing
- Over-clarifying trivial requests

## Related Commands

- `/cdf:explain` - For exploratory intents
- `/cdf:analyze` - For understanding codebase structure
- `/cdf:brainstorm` - When multiple approaches exist
- `/cdf:flow` - For multi-phase development workflows
