---
description: "Diagnose and resolve issues in code, builds, deployments, and system behavior"
---

# /cdf:troubleshoot - Issue Diagnosis and Resolution

## Triggers
- Code defects and runtime error investigation requests
- Build failure analysis and resolution needs
- Performance issue diagnosis and optimization requirements
- Deployment problem analysis and system behavior debugging

## Context Trigger Pattern
```
/cdf:troubleshoot [issue] [--type bug|build|performance|deployment] [--trace] [--fix]
```

## Delegation: compound-engineering

This command delegates to the `compound-engineering:ce-debug` host skill.

**Requires**: the compound-engineering plugin. If it is not installed, stop and tell the user to install the compound-engineering plugin for their host (install commands are in the README) — do not improvise a replacement flow.

**Flow**: Invoke the `compound-engineering:ce-debug` host skill, passing the user's arguments and any flags as context.

**CDF constraints (bind on top of the skill)**:
- The fix must address root cause, not just symptoms.
- A regression test is required for the resolved failure mode.
- After a non-obvious fix, capture the learning with the `compound-engineering:ce-compound` host skill.
