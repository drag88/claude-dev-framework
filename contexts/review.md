# Review Context Mode

Active when `/cdf:session load --mode review` is used.

## Behavioral Priorities

### Primary Focus: Quality Assessment
- Evaluate code for correctness and maintainability
- Identify potential issues before they ship
- Ensure standards compliance
- Provide constructive feedback

### Mindset
- "Trust but verify"
- Look for edge cases and failure modes
- Consider long-term maintenance
- Balance thoroughness with pragmatism

## Adjusted Behaviors

### Code Analysis
- Review all changes systematically
- Check for security vulnerabilities
- Verify error handling completeness
- Assess code clarity and maintainability

### Testing Review
- Verify test coverage for new code
- Check test quality and assertions
- Look for missing edge cases
- Ensure tests are not brittle

### Documentation Review
- Check for accurate documentation
- Verify API documentation is updated
- Look for misleading comments
- Ensure examples are correct

### Architecture Review
- Assess design decisions
- Check for proper separation of concerns
- Look for potential performance issues
- Identify technical debt

## Quality Checklist

### Security (CRITICAL)
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection prevented
- [ ] XSS prevented
- [ ] Authentication verified

### Code Quality (HIGH)
- [ ] Functions < 50 lines
- [ ] Files < 500 lines
- [ ] No deep nesting (> 4 levels)
- [ ] Error handling complete
- [ ] No unused code

### Performance (MEDIUM)
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] No blocking operations
- [ ] Efficient algorithms

### Maintainability (MEDIUM)
- [ ] Clear naming
- [ ] Single responsibility
- [ ] Documented complex logic
- [ ] Tests present

## Quality Thresholds

| Check | Threshold |
|-------|-----------|
| Build | Must pass |
| Types | Must pass |
| Lint | Must pass |
| Tests | 80% coverage |
| Security | No issues |

## Commands Behavior

### `/cdf:analyze`
- Full comprehensive analysis
- Include all domains (quality, security, performance)
- Generate detailed report

### `/cdf:test`
- Run full test suite
- Include E2E tests
- Generate coverage report

### `/cdf:verify`
- Use --mode pre-pr
- No auto-fix (review changes manually)
- Full security scan

## Review Output Format

```markdown
## Code Review Summary

**Verdict**: ⚠️ REQUEST CHANGES

### Security (0 CRITICAL, 0 HIGH)
No security issues found.

### Code Quality
- [HIGH] `src/api/users.ts:45` - Function exceeds 50 lines
- [MEDIUM] `src/utils.ts:12` - Missing error handling

### Tests
- Coverage: 78% (below 80% threshold)
- Missing: `src/services/payment.ts`

### Recommendations
1. Split `processUser` function
2. Add try-catch to `fetchData`
3. Add tests for payment service
```

## Common Review Scenarios

### PR Review
```
1. Understand the change context
2. Review file by file
3. Check for security issues first
4. Verify test coverage
5. Assess code quality
6. Check documentation
7. Provide feedback
```

### Architecture Review
```
1. Understand system context
2. Review component boundaries
3. Check dependency directions
4. Assess scalability
5. Identify technical debt
6. Document findings
```

### Security Review
```
1. Check authentication/authorization
2. Review input validation
3. Look for injection vulnerabilities
4. Check data exposure
5. Review error messages
6. Verify sensitive data handling
```

## Tool Suggestions

When in review mode, prefer:
- Thorough analysis over quick checks
- Full test runs over affected only
- Detailed feedback over summary
- Explicit recommendations over hints
