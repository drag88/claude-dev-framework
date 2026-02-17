# Skills Index

Quick reference for all auto-invoked skills, organized by category.

---

## Core Skills (7)

| Skill | Trigger | Description |
|-------|---------|-------------|
| [rules-generator](rules-generator/SKILL.md) | Missing `.claude/rules/` | Auto-generates project documentation |
| [claudemd-generator](claudemd-generator/SKILL.md) | After rules generation | Creates `CLAUDE.generated.md` |
| [context-saver](context-saver/SKILL.md) | Context 75%+ or 50+ tool calls | Saves session progress with strategic compaction |
| [external-memory](external-memory/SKILL.md) | Complex tasks (50+ tool calls) | File-based working memory in `dev/memory/` |
| [project-memory](project-memory/SKILL.md) | SessionStart, SessionEnd, file changes | Persistent project-scoped memory with daily logs |
| [intent-gate](intent-gate/SKILL.md) | Every request | Classifies request type for optimal handling |
| [failure-recovery](failure-recovery/SKILL.md) | 3 consecutive failures | STOP → REVERT → DOCUMENT → CONSULT |

---

## Development Pattern Skills (6)

| Skill | Trigger | Description |
|-------|---------|-------------|
| [coding-standards](coding-standards/SKILL.md) | Code implementation | Enforces code quality, naming standards, immutability patterns |
| [backend-patterns](backend-patterns/SKILL.md) | Backend development | API design, database patterns, authentication, rate limiting |
| [frontend-patterns](frontend-patterns/SKILL.md) | Frontend development | React patterns, custom hooks, state management, performance |
| [tdd-workflow](tdd-workflow/SKILL.md) | TDD mode active | RED-GREEN-REFACTOR cycle enforcement, 80% coverage gate |
| [e2e-patterns](e2e-patterns/SKILL.md) | E2E testing | Playwright patterns, Page Object Model, flaky test handling |
| [continuous-learning](continuous-learning/SKILL.md) | Session end | Pattern extraction and skill generation |

---

## Specialized Skills (5)

| Skill | Trigger | Description |
|-------|---------|-------------|
| [frontend-slides](frontend-slides/SKILL.md) | HTML presentation tasks | Zero-dependency HTML presentations with style presets and PPT conversion |
| [pptx](pptx/SKILL.md) | Presentation tasks | PowerPoint creation, editing, and analysis |
| [skill-creator](skill-creator/SKILL.md) | Creating new skills | Guide for building effective skills |
| [social-writing](social-writing/SKILL.md) | LinkedIn/Twitter posts | Authentic, human-centered social content |
| [starhub-presentation](starhub-presentation/SKILL.md) | StarHub decks | Executive presentations with official templates |

---

## How Skills Work

Skills are automatically invoked based on context triggers. They provide specialized behaviors without requiring explicit commands.

### Activation Flow

```
1. Request received
2. Intent-gate classifies request type
3. Relevant skills activate based on triggers
4. Skills provide context and patterns
5. Claude executes with enhanced guidance
```

### Skill Triggers

| Trigger Type | Example |
|--------------|---------|
| **Missing resource** | `.claude/rules/` not present |
| **Context threshold** | 75%+ context usage |
| **Tool call count** | 50+ tool calls in session |
| **Task type** | Backend development, E2E testing |
| **Failure pattern** | 3 consecutive failures |
| **Session event** | Session start, session end |

---

## Quick Selection Guide

| If you need... | Skill activates |
|----------------|-----------------|
| Project rules generated | rules-generator |
| Session context saved | context-saver |
| Working memory for complex task | external-memory |
| Persistent project memory | project-memory |
| Code quality patterns | coding-standards |
| API design guidance | backend-patterns |
| React component patterns | frontend-patterns |
| TDD enforcement | tdd-workflow |
| Playwright E2E patterns | e2e-patterns |
| Pattern extraction | continuous-learning |
| Recovery from failures | failure-recovery |
