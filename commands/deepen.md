---
description: "Parallel agent saturation for comprehensive analysis of plans or complex tasks"
argument-hint: "[plan-file-or-task] [--agents all|review|research] [--synthesize]"
---

# /cdf:deepen - Parallel Agent Saturation

> Spawn all available agents in parallel to comprehensively analyze a plan or task. Let agents self-filter for relevance rather than pre-filtering.

## Philosophy

**When facing complex decisions, more perspectives are better.** Instead of carefully selecting which agents might be relevant, spawn them all and let each decide if they have something to contribute.

## Quick Start

```bash
# Deepen an existing plan
/cdf:deepen docs/plans/2024-01-15-user-auth-plan.md

# Deepen current flow plan
/cdf:deepen

# Deepen with specific agent categories
/cdf:deepen dev/active/migration/flow-plan.md --agents review

# Deepen and synthesize findings
/cdf:deepen --synthesize
```

## When to Use

Use `/cdf:deepen` when:
- Planning a major architectural change
- Unsure if your plan covers all concerns
- Want comprehensive code review from multiple perspectives
- Need to validate approach before significant investment
- Used automatically by `/cdf:flow --deepen`

**Don't use this command for**: Simple tasks, quick fixes, or when you need speed over thoroughness.

## Behavioral Flow

### Phase 1: Discover All Agents

```bash
# Discover from ALL sources:
find .claude/agents -name "*.md"           # Project-local
find ~/.claude/agents -name "*.md"         # User global
find ~/.claude/plugins/cache -path "*/agents/*.md"  # All plugins
```

### Phase 2: Spawn Agent Wave (Parallel)

**CRITICAL**: Do NOT filter agents by perceived relevance. Spawn ALL discovered agents.

```
Task @system-architect: "Review this plan using your expertise: [plan content]"
Task @backend-architect: "Review this plan using your expertise: [plan content]"
Task @frontend-architect: "Review this plan using your expertise: [plan content]"
Task @security-engineer: "Review this plan using your expertise: [plan content]"
Task @performance-engineer: "Review this plan using your expertise: [plan content]"
Task @quality-engineer: "Review this plan using your expertise: [plan content]"
... (ALL agents)
```

Each agent receives the full plan and decides independently if they have relevant feedback.

### Phase 3: Collect Findings

Each agent returns structured feedback:
- Relevance assessment (skip if not applicable)
- Concerns or issues found
- Suggestions for improvement
- Best practices to consider

### Phase 4: Synthesize (if --synthesize)

1. Collect all agent outputs
2. Deduplicate similar findings
3. Categorize by type (security, performance, architecture, etc.)
4. Prioritize by impact
5. Flag conflicts for human resolution

## Arguments

| Argument | Description |
|----------|-------------|
| `[plan-file-or-task]` | Path to plan file, or task description |
| `--agents` | Agent filter: `all` (default), `review`, `research`, `design` |
| `--synthesize` | Merge and deduplicate findings (default: true) |
| `--output` | Write findings to file instead of inline |
| `--max` | Maximum agents to spawn (default: unlimited) |

## Agent Categories

### Review Agents
Focus on code quality, patterns, and standards:
- @system-architect
- @backend-architect
- @frontend-architect
- @security-engineer
- @performance-engineer
- @quality-engineer
- @refactoring-expert

### Research Agents
Focus on information gathering:
- @deep-research-agent
- @codebase-navigator
- @library-researcher

### Design Agents
Focus on architecture and UI:
- @frontend-architect
- @system-architect

## Output Format

### Per-Agent Output
```markdown
## @security-engineer

**Relevance**: High - Plan involves authentication

### Concerns
1. **Token Storage** (P1): Plan doesn't specify where tokens are stored client-side
2. **CSRF Protection** (P2): No mention of CSRF tokens for state-changing requests

### Suggestions
- Use HttpOnly cookies for token storage
- Implement CSRF protection using synchronizer token pattern

### Best Practices
- Consider OAuth 2.0 PKCE for public clients
- Implement token rotation on refresh
```

### Synthesized Output (--synthesize)
```markdown
# Deepen Analysis: User Authentication Plan

## Summary
- **Agents Consulted**: 21
- **Relevant Responses**: 8
- **Total Findings**: 15

## Findings by Priority

### P1 - Critical (3)
1. **Token Storage** (@security-engineer): Specify client-side token storage
2. **N+1 Query Risk** (@performance-engineer): User lookup may cause N+1
3. **Error Handling** (@backend-architect): No error recovery strategy

### P2 - Important (7)
...

### P3 - Nice to Have (5)
...

## Conflicts Requiring Resolution
- @performance-engineer suggests caching; @security-engineer warns about cache invalidation

## Consensus Points
- All agents agree on need for rate limiting
- Strong support for using existing auth library vs. custom
```

## Integration with /cdf:flow

When `/cdf:flow --deepen` is used:
1. Deepen runs after docs phase completes
2. Findings are incorporated into flow-plan.md
3. High-priority findings may trigger plan revision
4. Agent outputs saved to `dev/active/[task]/agents/`

## Scaling Considerations

- **20-40 agents is normal** - Don't worry about spawning many
- **Parallel execution** - All agents run simultaneously
- **Self-filtering** - Agents skip if not relevant
- **Timeout handling** - Agents have 60s timeout, failures don't block others

## MCP Integration

- **Context7 MCP**: Agents can query framework docs
- **Sequential MCP**: Used for synthesis phase reasoning

## Tool Coordination

| Tool | Purpose |
|------|---------|
| `Read` | Load plan file |
| `Task` | Spawn parallel agents |
| `Write` | Save synthesized findings |
| `Glob` | Discover available agents |

## Examples

### Deepen a Migration Plan
```bash
/cdf:deepen docs/plans/2024-01-15-graphql-migration-plan.md
# Spawns all 21+ agents
# Each reviews from their specialty perspective
# Outputs consolidated findings
```

### Deepen with Review Focus
```bash
/cdf:deepen dev/active/auth-refactor/flow-plan.md --agents review
# Only spawns review-category agents
# Faster, focused on code quality
```

### Deepen Current Flow
```bash
# While in /cdf:flow
/cdf:deepen
# Auto-detects active flow plan
# Enhances current planning phase
```

## Boundaries

**Will:**
- Spawn all available agents without filtering
- Let agents self-determine relevance
- Synthesize and deduplicate findings
- Identify conflicts between agent recommendations

**Will Not:**
- Pre-filter agents based on task type
- Limit agent count without explicit --max
- Execute any changes (analysis only)
- Override agent assessments

## Related Commands

- `/cdf:flow --deepen` - Integrated deepen in workflow
- `/cdf:analyze` - Single-perspective analysis
- `/cdf:panel` - Multi-expert discussion (interactive)
