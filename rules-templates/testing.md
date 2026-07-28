# Testing Rules Template

Copy this template to `.claude/rules/testing.md` and customize for your project.

---

## Coverage Requirements

### Minimum Thresholds
Coverage gates live in the test config (jest.config/vitest.config) — run the coverage script rather than assuming a number.

### Critical Paths
The following must have 100% coverage:
- Authentication and authorization logic
- Payment processing
- Data validation
- Security utilities

---

## Test Structure

### File Naming
- Unit tests: `*.test.ts` or `*.spec.ts`
- Integration tests: `*.integration.test.ts`
- E2E tests: `*.e2e.spec.ts`

### File Location
```
src/
├── components/
│   ├── Button.tsx
│   └── Button.test.tsx      # Co-located
├── services/
│   ├── UserService.ts
│   └── UserService.test.ts  # Co-located
tests/
├── integration/             # Integration tests
└── e2e/                     # E2E tests
```

---

## Test Quality Standards

### Every Test Must Have
1. **Clear description**: "should [expected behavior] when [condition]"
2. **Arrange-Act-Assert**: Clear separation of setup, action, verification
3. **Named by behavior**: assert the thing the test is named for

### Test Template
```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // Arrange
      const userData = createTestUserData();

      // Act
      const result = await userService.createUser(userData);

      // Assert
      expect(result).toHaveProperty('id');
      expect(result.email).toBe(userData.email);
    });

    it('should throw ValidationError for invalid email', async () => {
      // Arrange
      const invalidData = { ...createTestUserData(), email: 'invalid' };

      // Act & Assert
      await expect(userService.createUser(invalidData))
        .rejects.toThrow(ValidationError);
    });
  });
});
```

---

## What to Test

### Always Test
- Public API functions
- Business logic
- Error handling paths
- Edge cases and boundaries
- Input validation

### Don't Test
- Private implementation details
- Framework/library code
- Simple getters/setters
- Third-party integrations (mock them)

---

## Mocking Standards

### When to Mock
- External services (APIs, databases)
- Time-dependent operations
- Random number generation
- File system operations

### When NOT to Mock
- Internal utility functions
- Domain logic
- The function under test

```typescript
// Good: Mock external dependency
const mockEmailService = {
  send: jest.fn().mockResolvedValue({ messageId: '123' })
};

// Bad: Don't mock what you're testing
// jest.spyOn(userService, 'createUser');
```

---

## TDD Requirements

For behavior changes with a clear contract, write the failing test first — /cdf:tdd runs the full cycle.

---

## CI/CD Integration

### Pre-commit
- Run affected tests only
- Coverage check on changed files

### Pre-merge
- Run full test suite
- Coverage gate enforcement

### Nightly
- Full E2E suite
- Performance benchmarks
- Security scans

---

## Test Maintenance

### Test Data
- Use factories for test data
- Never use production data
- Clean up after tests
