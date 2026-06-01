# Code Patterns

## Command Definition Pattern

Commands use markdown with YAML frontmatter. The file is the complete behavioral spec — no executable code.

```yaml
---
name: command-name
description: Brief description
---

# /cdf:command-name - Title

## Quick Start
## Subcommands
## Behavioral Flow
## Examples
## Guidelines
## Boundaries
```

## Agent Definition Pattern

Agents define real-expertise personas (codebase-navigator, library-researcher, quality-engineer, etc.). Generic role stubs are forbidden — for backend/frontend/devops roles, use `/cdf:task` with role framing.

```yaml
---
name: agent-name
description: One-line capability
---

# Agent Title

## Mindset
## Focus Areas
## Key Actions
## Boundaries
```

## Skill Definition Pattern

Skills are directories with `SKILL.md`. They activate on trigger conditions, never via explicit invocation.

```
skills/skill-name/
├── SKILL.md       # Trigger conditions and behavior
├── templates/     # Optional templates
└── references/    # Optional reference docs
```

## Hook Configuration Pattern

`hooks/hooks.json` is the single source of truth. Every script lives under `scripts/` or `scripts/hooks/`.

```json
{
  "hooks": {
    "SessionStart": [
      { "hooks": [
        { "type": "command", "command": "test -f \"$CLAUDE_PLUGIN_ROOT/scripts/script.py\" && python3 \"$CLAUDE_PLUGIN_ROOT/scripts/script.py\" || true", "timeout": 60 }
      ] }
    ],
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ ... ] }
    ],
    "PostToolUse": [
      { "matcher": "Edit|Write|MultiEdit", "hooks": [ ... ] }
    ]
  }
}
```

The `test -f ... && python3 ... || true` guard keeps the plugin silent when an optional script is absent — never let a missing hook block the session.

## Python Hook Script Pattern

```python
#!/usr/bin/env python3
import json
import sys

def main():
    input_data = json.loads(sys.stdin.read())  # tool_name, tool_input, etc.
    # ...
    result = {"additionalContext": "Injected context for the host"}
    # or block: {"decision": "block", "reason": "..."}
    print(json.dumps(result))

if __name__ == "__main__":
    main()
```

## Hook I/O Contract

- **Input**: JSON on `sys.stdin` with a `tool_input` key (not `sys.argv`, not `$TOOL_INPUT`).
- **Output**: JSON on `sys.stdout` — either `{"additionalContext": "..."}` to inject context or `{"decision": "block", "reason": "..."}` to block the action.
- **Timeouts**: 5s for validators, 10s for pre-push checks, 60s for analysis hooks.
- **Dependencies**: Python stdlib only.
- **Path conventions**: Use `$CLAUDE_PLUGIN_ROOT` for plugin-relative paths inside `hooks.json`.

## Error Handling

- Hooks have explicit timeouts per script class (5s validators, 10s pre-push, 60s session analysis).
- Optional hooks guard with `test -f ... || true` so a missing script never blocks the session.
- After 3 consecutive failures, the `failure-recovery` skill activates: STOP → REVERT → DOCUMENT → CONSULT.

## Configuration Pattern

- Project-specific settings: `.claude/settings.local.json`.
- Permission allowlists: `.claude/settings.json`.
- Plugin path: `$CLAUDE_PLUGIN_ROOT` environment variable.
- MCP credentials: `.mcp/settings.json` (machine-local, never committed).

## Testing Patterns

- TDD workflow enforces RED-GREEN-REFACTOR via `/cdf:tdd`.
- E2E patterns use Page Object Model under `/cdf:e2e`.
- Minimum 80% coverage threshold tracked through `/cdf:test`.
- AAA pattern (Arrange-Act-Assert) is the default test structure.

## Command Routing

Match the request to the narrowest CDF surface:

- **Simple change** → direct edit or `/cdf:implement`
- **Multi-file change with known approach** → `/cdf:task`
- **Bug report** → `/cdf:troubleshoot`
- **Quality / security / perf audit** → `/cdf:analyze`
- **Tests or TDD** → `/cdf:test` or `/cdf:tdd`
- **Pre-PR check** → `/cdf:verify --mode pre-pr`
- **Plan-first work** → `/cdf:brainstorm` → `/cdf:design` → `/cdf:plan-review` → `/cdf:approve`
- **Release** → `/cdf:ship`
- **Full lifecycle** → clear prompt at `xhigh` effort (do not reintroduce `/cdf:flow` or `/cdf:workflow`).

## Naming Conventions

- **Python variables/functions**: `snake_case`
- **Python classes**: `PascalCase`
- **Markdown files**: `kebab-case` (e.g., `rules-templates/`, `plan-review.md`)
- **Command names**: `cdf:verb` or `cdf:verb-noun` (e.g., `cdf:rules`, `cdf:tdd`, `cdf:plan-review`)
- **Hook scripts**: descriptive `verb-noun` (`session-context.py`, `pre-push-checks.py`)
- **Agent names**: real-expertise nouns (`codebase-navigator`, `quality-engineer`, `library-researcher`)
- **Skill names**: action-oriented (`failure-recovery`, `product-review`, `visual-explainer`)

## Documentation Sync

Count-bearing docs that must stay in sync when components change:
- `README.md` (top of repo)
- `.claude/rules/architecture.md` (codemap table)
- `.claude/rules/tech-stack.md` (plugin components table)
- `.claude-plugin/marketplace.json` (description string)
- `CLAUDE.md` and `AGENTS.md` (project-specific notes)

Run `python3 scripts/health-check.py` after edits to catch drift.
