# Skills Index

Quick reference for all auto-invoked skills, organized by category.

---

## Core Skills (3)

| Skill | Trigger | Description |
|-------|---------|-------------|
| [rules-generator](rules-generator/SKILL.md) | Missing `.claude/rules/` | Auto-generates project documentation |
| [claudemd-generator](claudemd-generator/SKILL.md) | After rules generation | Creates `CLAUDE.generated.md` |
| [failure-recovery](failure-recovery/SKILL.md) | 3 consecutive failures | STOP → REVERT → DOCUMENT → CONSULT |

---

## Development Pattern Skills (5)

| Skill | Trigger | Description |
|-------|---------|-------------|
| [coding-standards](coding-standards/SKILL.md) | Code implementation | Enforces code quality, naming standards, immutability patterns |
| [backend-patterns](backend-patterns/SKILL.md) | Backend development | API design, database patterns, authentication, rate limiting |
| [frontend-patterns](frontend-patterns/SKILL.md) | Frontend development | React patterns, custom hooks, state management, performance |
| [tdd-workflow](tdd-workflow/SKILL.md) | TDD mode active | RED-GREEN-REFACTOR cycle enforcement, 80% coverage gate |
| [e2e-patterns](e2e-patterns/SKILL.md) | E2E testing | Playwright patterns, Page Object Model, flaky test handling |

---

## Specialized Skills (2)

| Skill | Trigger | Description |
|-------|---------|-------------|
| [frontend-design](frontend-design/SKILL.md) | UI/UX design tasks | Design system guidance and component patterns |
| [retro](retro/SKILL.md) | Retrospective requests | Git-history retrospective: velocity, quality signals, trends |

---

## How Skills Work

Skills are automatically invoked based on context triggers. They provide specialized behaviors without requiring explicit commands.

### Activation Flow

```
1. Request received
2. Relevant skills activate based on triggers (no pre-classification — Opus 4.7 plans on the fly)
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

---

## Quick Selection Guide

| If you need... | Skill activates |
|----------------|-----------------|
| Project rules generated | rules-generator |
| Code quality patterns | coding-standards |
| API design guidance | backend-patterns |
| React component patterns | frontend-patterns |
| TDD enforcement | tdd-workflow |
| Playwright E2E patterns | e2e-patterns |
| Recovery from failures | failure-recovery |
| UI/UX design guidance | frontend-design |
