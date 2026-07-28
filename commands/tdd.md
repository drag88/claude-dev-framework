---
description: "Test-Driven Development workflow with RED-GREEN-REFACTOR cycle enforcement"
---

# /cdf:tdd — Test-Driven Development

## The TDD invariant
Write the failing test before any implementation code. Verify the test fails for the expected reason. Then write the minimum code to pass it.

This invariant is enforced because TDD's value comes from the RED phase — if you skip it, you have tests-after-code, not TDD.

## First actions (per feature)

1. **Create the TDD state file** at `dev/active/[feature-slug]/tdd-state.md`:

```yaml
---
feature: "[feature description]"
created: [ISO timestamp]
current_phase: red
cycle: 1
tests_written: 0
coverage_target: 80
---

# TDD: [Feature]

## Cycle 1
- [ ] RED: Write failing test
- [ ] RED: Verify test fails correctly
- [ ] GREEN: Write minimal implementation
- [ ] GREEN: Verify test passes
- [ ] REFACTOR: Improve code quality
- [ ] REFACTOR: Verify still green
```

2. **Write the test file first.** Create a failing test before any implementation exists.

3. **Verify RED.** Run the test and confirm it fails for the expected reason. Paste the failure output. Do not proceed to GREEN until the failure is documented.

## Anti-patterns
- Writing implementation before the test exists (no RED state to verify)
- Writing a test that passes immediately (no failing baseline)
- Skipping failure verification (the RED output is the contract)
- Proceeding to GREEN without a documented RED phase
- Refactoring without re-running the full test suite

---

## Triggers
- TDD workflow requests for new features or bug fixes
- Test-first development methodology needs
- Code quality improvement through testing discipline
- Coverage gate enforcement requirements

## Usage
```
/cdf:tdd [feature-description] [--coverage <percentage>] [--strict]
```

## Arguments
- `feature-description`: What you want to implement using TDD
- `--coverage <percentage>`: Minimum coverage required (default: 80%)
- `--strict`: Enforce strict TDD - fail if tests written after code

## Cycle Iteration

After completing RED → GREEN → REFACTOR:
1. Add next test case (edge cases, error conditions)
2. Repeat the cycle
3. Continue until feature is complete

```typescript
// Iteration 2: Add edge case
it('should return 0 for orders exactly $100', () => {
  expect(calculateDiscount(100)).toBe(0);
});

it('should handle negative amounts', () => {
  expect(calculateDiscount(-50)).toBe(0);
});
```

## Coverage Gate

Before completing a TDD session:

```bash
# Run coverage check
npm run test:coverage

# Verify minimum threshold
# Statements: 80%
# Branches: 80%
# Functions: 80%
# Lines: 80%
```

If coverage is below threshold:
1. Identify uncovered code paths
2. Add tests for missing scenarios
3. Re-run coverage until threshold met

## Examples

### New Feature TDD
```
/cdf:tdd "Add user password validation with minimum 8 chars, uppercase, and number"
```

### Bug Fix TDD
```
/cdf:tdd "Fix: Order total not including tax" --strict
```

### With Custom Coverage
```
/cdf:tdd "Implement shopping cart" --coverage 90
```

## Boundaries

**Will:**
- Enforce RED-GREEN-REFACTOR cycle discipline
- Verify coverage meets minimum thresholds
- Guide test-first implementation approach
- Suggest test cases and edge conditions

**Will Not:**
- Skip test phase and write code directly
- Accept coverage below specified threshold
- Allow tests to be written after implementation (in strict mode)
- Compromise test quality for speed
