---
description: "Test-Driven Development workflow with RED-GREEN-REFACTOR cycle enforcement"
---

## MANDATORY FIRST ACTIONS (DO NOT SKIP)

**THE INVIOLABLE TDD RULE**: NEVER write implementation code before a failing test exists.

### Step 1: Create TDD State File
```bash
mkdir -p dev/active/[feature-slug]
```

Write `dev/active/[feature-slug]/tdd-state.md`:
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

### Step 2: Write Test File FIRST
Before ANY implementation code exists, create the test file with a failing test.

### Step 3: Verify RED State
Run the test and CONFIRM it fails before proceeding to GREEN.

**CRITICAL ANTI-PATTERNS - DO NOT:**
- Write ANY implementation before test exists
- Write a test that passes immediately
- Skip failure verification (must see RED output)
- Proceed to GREEN without documented RED phase
- Refactor without re-running ALL tests

---

# /cdf:tdd - Test-Driven Development

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

## Behavioral Flow

### RED Phase - Write Failing Test
1. **Understand Requirement**: Clarify what behavior needs to be implemented
2. **Write Test First**: Create a test that describes the expected behavior
3. **Verify Test Fails**: Run test to confirm it fails for the right reason
4. **No Implementation Yet**: Resist writing any implementation code

```typescript
// Example: RED Phase
describe('calculateDiscount', () => {
  it('should apply 10% discount for orders over $100', () => {
    const result = calculateDiscount(150);
    expect(result).toBe(15); // This will fail - function doesn't exist
  });
});
```

### GREEN Phase - Make Test Pass
1. **Write Minimal Code**: Implement just enough to make the test pass
2. **No Over-Engineering**: Don't add features not covered by tests
3. **Verify Test Passes**: Run test to confirm green status
4. **Check Coverage**: Ensure new code is covered

```typescript
// Example: GREEN Phase - Minimal implementation
function calculateDiscount(orderTotal: number): number {
  if (orderTotal > 100) {
    return orderTotal * 0.1;
  }
  return 0;
}
```

### REFACTOR Phase - Improve Code
1. **Clean Up Code**: Improve structure while keeping tests green
2. **Remove Duplication**: Extract common patterns
3. **Improve Names**: Clarify intent through better naming
4. **Verify Still Green**: Run all tests after each change

```typescript
// Example: REFACTOR Phase
const DISCOUNT_THRESHOLD = 100;
const DISCOUNT_RATE = 0.1;

function calculateDiscount(orderTotal: number): number {
  const qualifiesForDiscount = orderTotal > DISCOUNT_THRESHOLD;
  return qualifiesForDiscount ? orderTotal * DISCOUNT_RATE : 0;
}
```

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

## MCP Integration
- **Quality Engineer Persona**: Activated for test design and coverage analysis
- **Enhanced Capabilities**: Test pattern suggestions, edge case detection

## Tool Coordination
- **Bash**: Test runner execution and coverage analysis
- **Read/Edit**: Test file creation and modification
- **Grep**: Find existing tests and patterns

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

## TDD Checklist

Before each cycle:
- [ ] Requirement is clear and specific
- [ ] Test describes expected behavior
- [ ] Test is readable and maintainable

During RED phase:
- [ ] Test compiles/runs
- [ ] Test fails for the expected reason
- [ ] Error message is informative

During GREEN phase:
- [ ] Only enough code to pass the test
- [ ] No additional features added
- [ ] Test passes consistently

During REFACTOR phase:
- [ ] All tests still pass
- [ ] Code is cleaner than before
- [ ] No behavior changes

## Anti-Patterns to Avoid

1. **Writing tests after code** - Defeats purpose of TDD
2. **Testing implementation details** - Makes refactoring hard
3. **Skipping RED phase** - Missing failing test verification
4. **Large steps** - Should be small, incremental changes
5. **Ignoring refactoring** - Technical debt accumulates

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
