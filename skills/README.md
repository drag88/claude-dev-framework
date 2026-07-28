# Skills Index

Quick reference for all auto-invoked skills, organized by category.

---

## Core Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| [rules-generator](rules-generator/SKILL.md) | Missing `.claude/rules/` | Auto-generates `.claude/rules/` documentation for any codebase |
| [claudemd-generator](claudemd-generator/SKILL.md) | After rules generation | Auto-generates `CLAUDE.generated.md` from project rules |
| [agentsmd-generator](agentsmd-generator/SKILL.md) | After rules generation | Auto-generates `AGENTS.generated.md` from project rules |
| [failure-recovery](failure-recovery/SKILL.md) | 3 consecutive failures | Protocol for handling consecutive failures to prevent thrashing |

---

## Development Pattern Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| [coding-standards](coding-standards/SKILL.md) | Code implementation | Naming conventions, DRY/KISS/YAGNI, and code quality standards |
| [backend-patterns](backend-patterns/SKILL.md) | Backend development | API design, repository pattern, caching, auth middleware, error handling |
| [frontend-patterns](frontend-patterns/SKILL.md) | Frontend development | React component patterns, state management, hooks, performance |
| [tdd-workflow](tdd-workflow/SKILL.md) | TDD mode active | Test-driven development with RED-GREEN-REFACTOR cycle enforcement |
| [e2e-patterns](e2e-patterns/SKILL.md) | E2E testing | Playwright patterns, Page Object Model, locator strategies, test reliability |

---

## Review & Planning Skills

| Skill | Trigger | Description |
|-------|---------|-------------|

| [frontend-design](frontend-design/SKILL.md) | UI/UX design tasks | Design system guidance and component patterns |
| [retro](retro/SKILL.md) | Retrospective requests | Git-history retrospective: velocity, quality signals, trends |
| [agentsmd-generator](agentsmd-generator/SKILL.md) | After rules generation (Codex host) | Creates `AGENTS.generated.md` |
| [comprehension-coach](comprehension-coach/SKILL.md) | Teaching/understanding requests | Guided comprehension of unfamiliar code |
| [tuning-coding-agent-codebases](tuning-coding-agent-codebases/SKILL.md) | Agent-codebase audits | Practices for making codebases agent-friendly |

---

## How Skills Work

Skills are automatically invoked based on context triggers. They provide specialized behaviors without requiring explicit commands.

### Activation Flow

```
1. Request received
2. Relevant skills activate based on triggers (no pre-classification — Claude plans on the fly)
3. Skills provide context and patterns
4. Claude executes with enhanced guidance
```

### Skill Triggers

| Trigger Type | Example |
|--------------|---------|
| **Missing resource** | `.claude/rules/` not present |
| **Task type** | Backend development, E2E testing |
| **Failure pattern** | 3 consecutive failures |
| **Session event** | Session start, session end |
| **Explicit invocation** | `/retro`, `/brand-dna <url>` |

---

## Quick Selection Guide

| If you need... | Skill activates |
|----------------|-----------------|
| Project rules generated | rules-generator |
| `CLAUDE.md` / `AGENTS.md` regenerated | claudemd-generator / agentsmd-generator |
| Code quality patterns | coding-standards |
| API design guidance | backend-patterns |
| React component patterns | frontend-patterns |
| TDD enforcement | tdd-workflow |
| Playwright E2E patterns | e2e-patterns |
| Recovery from failures | failure-recovery |
| UI/UX design guidance | frontend-design |
