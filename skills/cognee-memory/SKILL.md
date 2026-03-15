---
description: "Persistent knowledge graph memory via cognee MCP for cross-session learning"
---

# Cognee Memory Skill

Retrieve accumulated knowledge at session start and store learnings during sessions using cognee's knowledge graph. Falls back to markdown storage when cognee is unavailable.

## When to Activate

### Automatic Triggers
- **Session start**: When cognee MCP tools are detected, search for relevant project context
- **User correction**: When the user corrects an approach ("no, do it this way", "don't do X")
- **Pattern solved**: When a significant problem is solved after multiple iterations
- **Explicit request**: User says "remember this", "what do you know about X", or similar

### Detection
Check for cognee MCP tools availability by looking for tools prefixed with `mcp__cognee__` (e.g., `cognee_search`, `cognify`, `save_interaction`, `cognee_add_developer_rules`).

## Behaviors

### 1. Retrieve (Session Start)

When cognee tools are available at session start:

```
cognee_search(
  query="project context, workflow preferences, past corrections",
  search_type="GRAPH_COMPLETION",
  top_k=5,
  dataset_name="<project-directory-name>"
)
```

- Summarize results to ~500 tokens before injecting as context
- Inject alongside (not replacing) git history and auto-memory context
- If search returns empty, skip silently -- new project with no history yet

### 2. Store Corrections (During Session)

When the user corrects your approach:

```
save_interaction(
  text="[CORRECTION] <context>: <what user said>. Previous approach: <what was wrong>. Correct approach: <what to do instead>.",
  dataset_name="<project-directory-name>"
)
```

### 3. Store Patterns (During Session)

When a significant pattern is solved:

```
save_interaction(
  text="[PATTERN] <pattern-name>: <context and problem>. Solution: <approach>. Trade-offs: <pros/cons>.",
  dataset_name="<project-directory-name>"
)
```

### 4. Store Decisions (During Session)

When an architectural or design decision is made:

```
save_interaction(
  text="[DECISION] <decision>. Alternatives considered: <list>. Rationale: <why this choice>.",
  dataset_name="<project-directory-name>"
)
```

### 5. Build Knowledge Graph (Session End / Batch)

After accumulating interactions, or when explicitly triggered:

```
cognify(dataset_name="<project-directory-name>")
```

This processes raw interactions into structured knowledge graph nodes and edges.

### 6. Ingest Rules (On Setup)

When `/cdf:cognee setup` is run, ingest existing project rules:

```
cognee_add_developer_rules(
  rules="<contents of .claude/rules/*.md files>",
  dataset_name="<project-directory-name>"
)
```

## Knowledge Categories

| Category | Storage Tool | Search Type | Prefix |
|----------|-------------|-------------|--------|
| Code Patterns | `save_interaction` / `cognify` | `GRAPH_COMPLETION` | `[PATTERN]` |
| Project Rules | `cognee_add_developer_rules` | `CODING_RULES` | -- |
| Workflow Preferences | `save_interaction` | `GRAPH_COMPLETION` | `[PREFERENCE]` |
| Corrections | `save_interaction` | `GRAPH_COMPLETION` | `[CORRECTION]` |
| Decisions | `save_interaction` | `GRAPH_COMPLETION` | `[DECISION]` |
| Context Knowledge | `cognify` | `GRAPH_COMPLETION` | `[CONTEXT]` |

## Graceful Degradation

If cognee MCP tools are **not** available:

1. Do not error or warn repeatedly -- check once at session start
2. Fall back to continuous-learning skill's markdown storage (`.claude/learnings/`)
3. CDF works identically without cognee; the knowledge graph is an enhancement, not a dependency

## Project Isolation

Use the project directory basename as `dataset_name` in all cognee calls:

```python
# Example: /Users/aswin/projects/my-app → dataset_name="my-app"
dataset_name = os.path.basename(os.getcwd())
```

This ensures one cognee instance can serve multiple projects without data bleed.

## Integration with Continuous Learning

This skill extends (does not replace) the continuous-learning skill:

- Continuous-learning identifies **what** to learn (detection heuristics, extraction process)
- Cognee-memory handles **where** to store it (knowledge graph vs. markdown)
- When cognee is available, learnings go to the graph. When not, they go to markdown files.

## How Skills Improve Over Time

Skills are never edited by this system. Instead, the **context around them** gets richer.

Example flow:
1. Session 1: User runs `/cdf:implement`, corrects Claude: "always check for existing tests first"
2. This skill stores: `[CORRECTION] implementation workflow: always check for existing tests before writing new code`
3. Session 5: User runs `/cdf:implement` again
4. This skill fires `search("implementation workflow preferences")` and retrieves the correction
5. Claude now checks for existing tests without being told

By session 20, the knowledge graph has accumulated dozens of corrections and preferences. `GRAPH_COMPLETION` returns a synthesized view, and Claude's behavior is substantially customized.

## Boundary Conditions

### Always Store
- User corrections (highest priority -- these represent explicit preferences)
- Patterns that required multiple iterations to solve
- Architectural decisions with documented rationale
- Explicit "remember this" requests

### Never Store
- Standard library usage or well-documented patterns
- Temporary workarounds or debugging state
- Sensitive data (API keys, credentials, personal information)
- Information already in `.claude/rules/` files (avoid duplication)
