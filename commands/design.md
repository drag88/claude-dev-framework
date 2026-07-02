---
description: "Design system architecture, APIs, and component interfaces with comprehensive specifications"
---

# /cdf:design - System and Component Design

## Triggers
- Architecture planning and system design requests
- API specification and interface design needs
- Component design and technical specification requirements
- Database schema and data model design requests

## Context Trigger Pattern
```
/cdf:design [target] [--type architecture|api|component|database] [--format diagram|spec|code]
```

## Delegation: compound-engineering

This command delegates to the `compound-engineering:ce-plan` host skill.

**Requires**: the compound-engineering plugin. If it is not installed, stop and tell the user to install the compound-engineering plugin for their host (install commands are in the README) — do not improvise a replacement flow.

**Flow**: Invoke the `compound-engineering:ce-plan` host skill, passing the user's arguments and any flags as context.

**CDF constraints (bind on top of the skill)**:
- Plan documentation lands in `docs/plans/`.
- When the request is a pure architecture or API specification, include that framing in the context passed to the skill.
