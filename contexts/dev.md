# Development Context Mode

Active when `/cdf:session load --mode dev` is used.

## Behavioral Priorities

### Primary Focus: Implementation
- Write working code efficiently
- Prioritize functionality over perfection
- Make incremental progress with frequent commits
- Use established patterns from the codebase

### Mindset
- "Ship it, then improve it"
- Focus on the happy path first
- Add error handling as you go
- Keep momentum

## Adjusted Behaviors

### Code Writing
- Prefer practical over perfect solutions
- Use existing patterns from the codebase
- Don't over-engineer for hypothetical requirements
- Add TODO comments for future improvements

### Testing
- Write tests for new functionality
- Focus on unit tests first
- Add integration tests for critical paths
- Skip E2E for rapid iteration (add later)

### Documentation
- Add inline comments for complex logic
- Update README when adding features
- Document API changes
- Skip detailed docs until feature stabilizes

### Error Handling
- Handle obvious error cases
- Log errors for debugging
- Add graceful degradation where easy
- Mark edge cases with TODOs

## Quality Thresholds

| Check | Threshold |
|-------|-----------|
| Build | Must pass |
| Types | Must pass |
| Lint | Warnings OK, no errors |
| Tests | 70% coverage |
| Security | No critical/high |

## Commands Behavior

### `/cdf:implement`
- Focus on core functionality
- Suggest minimal viable implementation
- Defer optimizations

### `/cdf:test`
- Run affected tests only
- Skip E2E by default
- Quick feedback loop

### `/cdf:verify`
- Use --mode quick by default
- Auto-fix lint issues
- Skip comprehensive checks

## Common Workflows

### Feature Development
```
1. Understand requirement
2. Find similar patterns in codebase
3. Implement core functionality
4. Add basic tests
5. Commit with descriptive message
6. Iterate based on feedback
```

### Bug Fixing
```
1. Reproduce the issue
2. Add failing test
3. Fix the bug
4. Verify test passes
5. Check for regressions
6. Commit fix
```

### Rapid Prototyping
```
1. Scaffold basic structure
2. Implement proof of concept
3. Get feedback quickly
4. Refine based on feedback
5. Clean up code
6. Add tests
```

## Tool Suggestions

When in dev mode, prefer:
- Quick iterations over thorough analysis
- Local testing over CI validation
- Pragmatic solutions over perfect ones
- Working code over complete code
