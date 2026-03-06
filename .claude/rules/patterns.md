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

- Hooks have configurable timeouts (3s for loggers, 60s for analysis)
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

## Context Modes

Quality thresholds vary by mode:
- **dev**: Ship first, iterate. Tests 70%, lint warnings OK
- **review**: Trust but verify. Tests 80%, no lint/security issues
- **research**: Understand before acting. Informational thresholds only

## Naming Conventions

- **Python variables/functions**: `snake_case`
- **Python classes**: `PascalCase`
- **Markdown files**: `kebab-case` (e.g., `memory-logger.py`, `rules-templates/`)
- **Command names**: `cdf:verb` or `cdf:verb-noun` (e.g., `cdf:rules`, `cdf:tdd`)
- **Hook scripts**: Descriptive verb-noun (`memory-logger.py`, `keyword-amplifier.py`)
- **Agent names**: Domain-specific nouns (`backend-architect`, `root-cause-analyst`)
- **Skill names**: Action-oriented (`intent-gate`, `failure-recovery`)
