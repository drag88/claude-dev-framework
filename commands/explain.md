---
description: "Provide clear explanations of code, concepts, and system behavior with educational clarity"
---

# /cdf:explain - Code and Concept Explanation

## Triggers
- Code understanding and documentation requests for complex functionality
- System behavior explanation needs for architectural components
- Educational content generation for knowledge transfer
- Framework-specific concept clarification requirements

## Usage
```
/cdf:explain [target] [--level basic|intermediate|advanced] [--format text|examples|interactive] [--context domain]
```

## Behavioral Flow
1. **Analyze**: Examine target code, concept, or system for comprehensive understanding
2. **Assess**: Determine audience level and appropriate explanation depth and format
3. **Structure**: Plan explanation sequence with progressive complexity and logical flow
4. **Generate**: Create clear explanations with examples, diagrams, and interactive elements
5. **Validate**: Verify explanation accuracy and educational effectiveness

Key behaviors:
- Adaptive explanation depth based on audience and complexity
- Use judgement on conventions already in the repo; delegate via `/cdf:task` with role framing only when multi-file fan-out is warranted.

## Examples

```
/cdf:explain react-hooks --level intermediate --context react
```

## Boundaries

**Will:**
- Provide clear, comprehensive explanations with educational clarity
- Generate framework-specific explanations grounded in official documentation

**Will Not:**
- Generate explanations without thorough analysis and accuracy verification
- Override project-specific documentation standards or reveal sensitive details
- Bypass established explanation validation or educational quality requirements