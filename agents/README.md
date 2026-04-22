# Agent Index

Quick reference for all available agent personas, organized by category.

For role-based work (backend / frontend / devops / system design / security / performance / docs / Python), invoke `/cdf:task` directly. The Role line in `CLAUDE.md` plus Opus 4.7's `xhigh` effort handles persona work without dedicated stub agents — these were removed in the 4.7 leanness pass.

---

## Analysis & Research (5)

| Agent | Description |
|-------|-------------|
| [deep-research-agent](deep-research-agent.md) | Comprehensive research with adaptive strategies and intelligent exploration |
| [codebase-navigator](codebase-navigator.md) | Find code, patterns, and dependencies across large codebases using parallel search strategies |
| [library-researcher](library-researcher.md) | Research open-source libraries with evidence-backed analysis using GitHub permalinks |
| [media-interpreter](media-interpreter.md) | Interpret and extract information from PDFs, images, diagrams, and other media files |
| [business-research-strategist](business-research-strategist.md) | Deep business research with Socratic interview, parallel sub-agent teams, and strategic frameworks |

---

## Quality & Refactoring (2)

| Agent | Description |
|-------|-------------|
| [quality-engineer](quality-engineer.md) | Ensure software quality through comprehensive testing strategies and edge case detection |
| [refactoring-expert](refactoring-expert.md) | Improve code quality and reduce technical debt through systematic refactoring |

---

## Testing Specialists (2)

| Agent | Description |
|-------|-------------|
| [tdd-guide](tdd-guide.md) | Test-Driven Development enforcement with RED-GREEN-REFACTOR workflow |
| [e2e-specialist](e2e-specialist.md) | End-to-end testing expert with Playwright patterns and Page Object Model |

---

## Discovery & Education (2)

| Agent | Description |
|-------|-------------|
| [requirements-analyst](requirements-analyst.md) | Transform ambiguous project ideas into concrete specifications through systematic discovery |
| [socratic-mentor](socratic-mentor.md) | Educational guide using Socratic method for discovery learning through strategic questioning |

---

## Business Strategy (1)

| Agent | Description |
|-------|-------------|
| [business-panel-experts](business-panel-experts.md) | Multi-expert business strategy panel (Christensen, Porter, Drucker, Godin, etc.) |

---

## Quick Selection Guide

| If you need to... | Use this agent (or fall back to `/cdf:task` with role) |
|-------------------|------------------------------|
| Research a topic | deep-research-agent |
| Find code in a large codebase | codebase-navigator |
| Evaluate a library | library-researcher |
| Understand an image/PDF | media-interpreter |
| Write tests | quality-engineer |
| Clean up code | refactoring-expert |
| Test-Driven Development | tdd-guide |
| E2E testing with Playwright | e2e-specialist |
| Gather requirements | requirements-analyst |
| Guided learning (Socratic) | socratic-mentor |
| Business strategy panel | business-panel-experts |
| Business research & market analysis | business-research-strategist |
| Backend / API / database design | `/cdf:task` (4.7 plays this role from CLAUDE.md) |
| Frontend / UI work | `/cdf:task` |
| DevOps / CI / CD | `/cdf:task` |
| System design | `/cdf:task` |
| Security audit | `/cdf:analyze` (security mode) |
| Performance optimization | `/cdf:analyze` (perf mode) |
| Documentation | `/cdf:docs` |
| Debug a complex issue | `/cdf:troubleshoot` |
| Python-specific help | `/cdf:task` |
