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
    # Read context from environment or stdin
    # Process and return result
    result = {"status": "success", "message": "..."}
    print(json.dumps(result))

if __name__ == "__main__":
    main()
```

## Error Handling

- Hooks have configurable timeouts (default 5-10s)
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

## Intent Classification

Every request classified before action:
- **Trivial** → Direct execution
- **Explicit** → Command execution
- **Exploratory** → Research first
- **GitHub Work** → Full workflow
- **Ambiguous** → Clarification needed
