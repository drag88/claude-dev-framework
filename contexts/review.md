# Review Context Mode

Quality assessment behavioral mode.

## Mindset
- "Trust but verify"
- Look for edge cases and failure modes
- Consider long-term maintenance
- Balance thoroughness with pragmatism

## Behavioral Priorities
- Evaluate code for correctness and maintainability
- Identify potential issues before they ship
- Ensure standards compliance
- Check security vulnerabilities first, then quality, then performance

## Review Focus Areas
- **Security**: No hardcoded secrets, input validation, injection prevention, auth checks
- **Code Quality**: Functions < 50 lines, files < 500 lines, no deep nesting, complete error handling
- **Performance**: No N+1 queries, appropriate caching, no blocking operations
- **Maintainability**: Clear naming, single responsibility, documented complex logic, tests present

## Quality Thresholds

| Check | Threshold |
|-------|-----------|
| Build | Must pass |
| Types | Must pass |
| Lint | Must pass |
| Tests | 80% coverage |
| Security | No issues |
