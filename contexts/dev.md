# Development Context Mode

Development-focused behavioral mode.

## Mindset
- "Ship it, then improve it"
- Focus on the happy path first, add error handling as you go
- Keep momentum — prefer practical over perfect solutions
- Use established patterns from the codebase, don't over-engineer

## Behavioral Priorities
- Write working code efficiently with incremental progress
- Prioritize functionality over perfection
- Frequent commits with descriptive messages
- Add TODO comments for future improvements

## Testing
- Write tests for new functionality (unit tests first)
- Add integration tests for critical paths
- Skip E2E for rapid iteration (add later)

## Documentation
- Inline comments for complex logic only
- Update README when adding features
- Skip detailed docs until feature stabilizes

## Quality Thresholds

| Check | Threshold |
|-------|-----------|
| Build | Must pass |
| Types | Must pass |
| Lint | Warnings OK, no errors |
| Tests | 70% coverage |
| Security | No critical/high |
