# Code Patterns

## Command Definition Pattern

Commands use markdown with YAML frontmatter:

```yaml
---
name: command-name
description: Brief description
---

# /cdf:command-name - Title

## Quick Start
## Subcommands
## Examples
## Guidelines
```

## Agent Definition Pattern

Agents define specialized personas:

```yaml
---
name: agent-name
triggers:
  - "keyword1"
  - "keyword2"
---

# Agent Title

## Mindset
## Focus Areas
## Key Actions
## Boundaries
```

## Skill Definition Pattern

Skills are directories with `SKILL.md`:

```
skills/skill-name/
├── SKILL.md       # Trigger conditions and behavior
└── templates/     # Optional templates
```

## Hook Configuration Pattern

Hooks in `hooks/hooks.json`:

```json
{
  "hooks": {
    "SessionStart": [
      { "command": "python3 \"$CLAUDE_PLUGIN_ROOT/scripts/script.py\"" }
    ],
    "PreToolUse": [
      { "matcher": "Edit|Write", "hooks": [...] }
    ]
  }
}
```

## Python Hook Script Pattern

```python
#!/usr/bin/env python3
import sys
import json

def main():
    # Read context from stdin (JSON with tool_name, tool_input, etc.)
    input_data = json.loads(sys.stdin.read())
    # Process and return result
    result = {"additionalContext": "Injected context for Claude"}
    # Or block: {"decision": "block", "reason": "..."}
    print(json.dumps(result))

if __name__ == "__main__":
    main()
```

## Hook I/O Contract

- **Input**: JSON on stdin with tool context (tool_name, tool_input, etc.)
- **Output**: JSON on stdout — either `{"additionalContext": "..."}` for injection or `{"decision": "block", "reason": "..."}` to block
- **Timeouts**: 3-60s depending on hook complexity
- **No external dependencies**: stdlib only

## Error Handling

- Hooks have configurable timeouts (5s for validators, 60s for analysis)
- Failure recovery skill activates after 3 consecutive failures
- Pattern: STOP → REVERT → DOCUMENT → CONSULT

## Configuration Pattern

- Project-specific settings in `.claude/settings.local.json`
- Permission allowlists for security
- Environment variables for plugin paths (`$CLAUDE_PLUGIN_ROOT`)

## Testing Patterns

- TDD workflow enforces RED-GREEN-REFACTOR
- E2E patterns use Page Object Model
- Minimum 80% coverage threshold
- AAA pattern: Arrange-Act-Assert

## Command Routing

Use the narrowest CDF surface that matches the request:
- **Simple implementation** -> `/cdf:implement` (delegates to `compound-engineering:ce-work`)
- **Raw idea, bug, or error needing a plan** -> `/cdf:plan` (delegates to `compound-engineering:ce-plan`; the single planning entry point)
- **Bug report** -> `/cdf:troubleshoot` (delegates to `compound-engineering:ce-debug`)
- **Diff or PR review** -> `compound-engineering:ce-code-review`
- **Ideation / grounded options** -> `compound-engineering:ce-ideate`
- **Quality or risk audit** -> `/cdf:analyze` (repo-wide audits)
- **Tests or TDD** -> `/cdf:test` or `/cdf:tdd`
- **Complex multi-file work** -> `/cdf:task` with real-expertise agents
- **Full lifecycle work** -> `/cdf:brainstorm` (delegates to `compound-engineering:ce-brainstorm`) -> `/cdf:design` (delegates to `compound-engineering:ce-plan`) -> `/cdf:plan-review` (delegates to `compound-engineering:ce-doc-review`) for high-stakes work

Deleted orchestrators stay deleted: do not reintroduce `/cdf:flow` or `/cdf:workflow`.

## Naming Conventions

- **Python variables/functions**: `snake_case`
- **Python classes**: `PascalCase`
- **Markdown files**: `kebab-case` (e.g., `rules-templates/`)
- **Command names**: `cdf:verb` or `cdf:verb-noun` (e.g., `cdf:rules`, `cdf:tdd`)
- **Hook scripts**: Descriptive verb-noun (`session-context.py`, `pre-push-checks.py`)
- **Agent names**: Real-expertise nouns (`codebase-navigator`, `quality-engineer`, `library-researcher`)
- **Skill names**: Action-oriented (`failure-recovery`, `rules-generator`)
