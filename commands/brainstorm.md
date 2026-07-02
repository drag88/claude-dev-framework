---
description: "Interactive requirements discovery through Socratic dialogue and systematic exploration"
---

# /cdf:brainstorm - Interactive Requirements Discovery

## Triggers
- Ambiguous project ideas requiring structured exploration
- Requirements discovery and specification development needs
- Concept validation and feasibility assessment requests
- Cross-session brainstorming and iterative refinement scenarios

## Context Trigger Pattern
```
/cdf:brainstorm [topic/idea] [--strategy systematic|agile|enterprise] [--depth shallow|normal|deep] [--parallel]
```
**Usage**: Type this pattern in the host conversation to activate brainstorming through the delegated host skill.

## Delegation: compound-engineering

This command delegates to the `compound-engineering:ce-brainstorm` host skill.

**Requires**: the compound-engineering plugin. If it is not installed, stop and tell the user to install the compound-engineering plugin for their host (install commands are in the README) — do not improvise a replacement flow.

**Flow**: Invoke the `compound-engineering:ce-brainstorm` host skill, passing the user's arguments and any flags as context.

**CDF constraints (bind on top of the skill)**:
- Requirements documentation lands in `docs/brainstorms/`.
- When the idea is ready for execution planning, hand off to `/cdf:design`, which delegates to `compound-engineering:ce-plan`.
