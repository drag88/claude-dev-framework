---
description: "Activate for test-driven development with RED-GREEN-REFACTOR cycle enforcement"
---

# TDD Workflow Skill

Automatically enforce Test-Driven Development practices during implementation.

## When to Activate

- When `/cdf:tdd` command is invoked
- During feature implementation when user mentions "TDD", "test-first", or "test-driven"
- When implementing bug fixes that should start with a failing test
- During any implementation where high code quality is required

## Core Principles

### RED-GREEN-REFACTOR Cycle
```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   ┌─────┐    ┌───────┐    ┌──────────┐             │
│   │ RED │───▶│ GREEN │───▶│ REFACTOR │─┐           │
│   └─────┘    └───────┘    └──────────┘ │           │
│      ▲                                  │           │
│      └──────────────────────────────────┘           │
│                                                     │
└─────────────────────────────────────────────────────┘

RED:      Write a failing test
GREEN:    Make it pass with minimal code
REFACTOR: Improve the code, keep tests green
```

## Workflow Steps

### 1. Understand the Requirement
Before writing any code:
- Clarify what behavior needs to be implemented
- Identify inputs and expected outputs
- Break down into small, testable units

### 2. Write the Failing Test (RED)
```typescript
// Start with the test
describe('calculateShippingCost', () => {
  it('should return free shipping for orders over $100', () => {
    const order = { total: 150, items: [] };
    const result = calculateShippingCost(order);
    expect(result).toBe(0);
  });
});
```

### 3. Run and See It Fail
```bash
npm test -- --testPathPattern="shipping"

# Expected output:
# FAIL  src/shipping.test.ts
# ● calculateShippingCost › should return free shipping for orders over $100
#   ReferenceError: calculateShippingCost is not defined
```

### 4. Write Minimal Implementation (GREEN)
```typescript
// Minimal code to pass
function calculateShippingCost(order: Order): number {
  if (order.total > 100) {
    return 0;
  }
  return 10;
}
```

### 5. Run and See It Pass
```bash
npm test -- --testPathPattern="shipping"

# Expected output:
# PASS  src/shipping.test.ts
# ✓ calculateShippingCost › should return free shipping for orders over $100
```

### 6. Refactor If Needed (REFACTOR)
```typescript
// Improved version with constants
const FREE_SHIPPING_THRESHOLD = 100;
const STANDARD_SHIPPING_COST = 10;

function calculateShippingCost(order: Order): number {
  return order.total > FREE_SHIPPING_THRESHOLD
    ? 0
    : STANDARD_SHIPPING_COST;
}
```

### 7. Add Next Test Case
```typescript
it('should return $10 for orders at exactly $100', () => {
  const order = { total: 100, items: [] };
  expect(calculateShippingCost(order)).toBe(10);
});

it('should return $10 for orders under $100', () => {
  const order = { total: 50, items: [] };
  expect(calculateShippingCost(order)).toBe(10);
});
```

### 8. Repeat Until Complete

## Test Case Categories

For comprehensive coverage, consider:

| Category | Example |
|----------|---------|
| Happy path | Normal valid input |
| Edge cases | Boundary values (0, 1, -1, max) |
| Empty input | null, undefined, empty string/array |
| Invalid input | Wrong type, out of range |
| Error conditions | Network failure, timeout |
| State transitions | Before/after operations |

## Coverage Requirements

| Metric | Minimum |
|--------|---------|
| Statements | 80% |
| Branches | 80% |
| Functions | 80% |
| Lines | 80% |

## Anti-Patterns to Avoid

### 1. Writing Code Before Tests
```
❌ BAD: "Let me just write the function first, then add tests"
✅ GOOD: "Let me write a failing test first"
```

### 2. Testing Implementation Details
```typescript
// ❌ BAD: Testing internal state
expect(calculator._internalBuffer).toBe([1, 2, 3]);

// ✅ GOOD: Testing behavior
expect(calculator.getResult()).toBe(6);
```

### 3. Large Test Cycles
```
❌ BAD: Writing 10 tests before any implementation
✅ GOOD: One test → implementation → next test
```

### 4. Skipping Refactor Phase
```
❌ BAD: "It works, ship it"
✅ GOOD: "It works, now let me clean it up"
```

## Common Testing Patterns

### Arrange-Act-Assert
```typescript
it('should calculate order total', () => {
  // Arrange
  const items = [{ price: 10 }, { price: 20 }];

  // Act
  const total = calculateTotal(items);

  // Assert
  expect(total).toBe(30);
});
```

### Given-When-Then (BDD)
```typescript
describe('given a premium user', () => {
  describe('when they apply a coupon', () => {
    it('then they should get 20% discount', () => {
      const user = createPremiumUser();
      const discount = applyCoupon(user, 'SAVE20');
      expect(discount).toBe(0.20);
    });
  });
});
```

## Integration with /cdf:test

After TDD implementation:
```bash
# Run all tests with coverage
/cdf:test --coverage

# Verify coverage meets threshold
# If below 80%, add more test cases
```

## Reporting Progress

During TDD session, report:
1. Current phase (RED/GREEN/REFACTOR)
2. Test being worked on
3. Coverage status
4. Next step

Example:
```
🔴 RED: Writing test for email validation
📝 Test: "should reject emails without @ symbol"
📊 Coverage: 75% → Need 5% more
⏭️ Next: Implement minimal validation
```

## Related Agents
- **tdd-guide** — Primary consumer enforcing RED-GREEN-REFACTOR cycle
- **quality-engineer** — Uses TDD workflow for test strategy and coverage

## Suggested Commands
- `/cdf:tdd` — Run full TDD workflow
- `/cdf:test` — Execute test suite
- `/cdf:implement` — Implement features with TDD approach
