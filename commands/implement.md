---
description: "Feature and code implementation with intelligent persona activation and MCP integration"
---

# /cdf:implement - Feature Implementation

## Triggers
- Feature development requests for components, APIs, or complete functionality
- Code implementation needs with framework-specific requirements
- Multi-domain development requiring coordinated expertise
- Implementation projects requiring testing and validation integration

## Context Trigger Pattern
```
/cdf:implement [feature-description] [--type component|api|service|feature] [--framework react|vue|express] [--safe] [--with-tests]
```
**Usage**: Type this in the host conversation to activate implementation through the delegated host skill.

## Delegation: compound-engineering

This command delegates to the `compound-engineering:ce-work` host skill.

**Requires**: the compound-engineering plugin. If it is not installed, stop and tell the user to install the compound-engineering plugin for their host (install commands are in the README) — do not improvise a replacement flow.

**Flow**: Invoke the `compound-engineering:ce-work` host skill, passing the user's arguments and any flags as context.

**CDF constraints (bind on top of the skill)**:
- Tests are required before a feature is complete.
- Verification-before-done from `.claude/rules/workflow.md` still applies.
- For large multi-module work, prefer `/cdf:task` first for subagent fan-out.
- After a non-obvious implementation lands, capture the learning with the `compound-engineering:ce-compound` host skill.
