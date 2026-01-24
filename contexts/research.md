# Research Context Mode

Active when `/cdf:session load --mode research` is used.

## Behavioral Priorities

### Primary Focus: Exploration and Understanding
- Gather comprehensive information
- Explore multiple options
- Understand trade-offs deeply
- Document findings thoroughly

### Mindset
- "Understand before acting"
- Explore widely before diving deep
- Question assumptions
- Value thoroughness over speed

## Adjusted Behaviors

### Codebase Exploration
- Read extensively before suggesting changes
- Understand existing patterns first
- Map dependencies and relationships
- Document architecture discoveries

### Technology Research
- Compare multiple solutions
- Evaluate pros and cons
- Consider long-term implications
- Provide evidence-based recommendations

### Problem Investigation
- Gather all relevant context
- Consider multiple hypotheses
- Trace issues to root causes
- Document investigation steps

### Documentation
- Create comprehensive notes
- Capture decision rationale
- Document alternatives considered
- Preserve context for future

## Research Outputs

### Codebase Analysis
```markdown
## Codebase Analysis: [Topic]

### Current State
- [Description of how things work now]

### Key Components
- `path/to/file.ts` - [Purpose]
- `path/to/other.ts` - [Purpose]

### Dependencies
- External: [Libraries used]
- Internal: [Component relationships]

### Patterns Observed
- [Pattern 1] - used in [locations]
- [Pattern 2] - used in [locations]

### Areas of Interest
- [Observation 1]
- [Observation 2]
```

### Technology Comparison
```markdown
## Technology Comparison: [Topic]

### Options Evaluated
1. **Option A**
   - Pros: [list]
   - Cons: [list]
   - Use when: [context]

2. **Option B**
   - Pros: [list]
   - Cons: [list]
   - Use when: [context]

### Recommendation
[Option] because [reasoning]

### References
- [Link 1]
- [Link 2]
```

### Investigation Report
```markdown
## Investigation: [Issue]

### Summary
[Brief description of finding]

### Investigation Steps
1. [Step 1] - [finding]
2. [Step 2] - [finding]
3. [Step 3] - [finding]

### Root Cause
[Description of underlying cause]

### Evidence
- [Log/code/data point 1]
- [Log/code/data point 2]

### Recommendations
- [Action 1]
- [Action 2]
```

## Commands Behavior

### `/cdf:research`
- Deep investigation mode
- Explore multiple sources
- Generate comprehensive report

### `/cdf:explain`
- Detailed explanations
- Include context and rationale
- Reference source code

### `/cdf:analyze`
- Full analysis across all dimensions
- Document everything found
- Note uncertainties

## Research Strategies

### Understanding a Codebase
```
1. Read README and documentation
2. Identify entry points
3. Trace key flows
4. Map component relationships
5. Note patterns and conventions
6. Document architecture
```

### Evaluating a Library
```
1. Check documentation quality
2. Review GitHub activity
3. Look at issue resolution
4. Test with sample code
5. Evaluate bundle size
6. Check security advisories
```

### Investigating a Bug
```
1. Reproduce the issue
2. Gather error details
3. Check recent changes
4. Add logging/debugging
5. Form hypotheses
6. Test each hypothesis
7. Document findings
```

### Researching Best Practices
```
1. Search official documentation
2. Find authoritative sources
3. Look at open source examples
4. Check community discussions
5. Synthesize findings
6. Adapt to project context
```

## Quality Thresholds

In research mode, quality checks are informational only:

| Check | Behavior |
|-------|----------|
| Build | Report status |
| Types | Report status |
| Lint | Report issues |
| Tests | Report coverage |
| Security | Report findings |

## Tool Suggestions

When in research mode, prefer:
- Reading over writing code
- Exploration over implementation
- Documentation over action
- Understanding over fixing

## Research Session Best Practices

### Start with Questions
- What are we trying to learn?
- What decisions need to be made?
- What constraints exist?

### Document as You Go
- Take notes on findings
- Capture code references
- Note uncertainties

### Synthesize Findings
- Summarize key insights
- Make recommendations
- Identify next steps

### Preserve Context
- Save research notes
- Create ADRs for decisions
- Update documentation
