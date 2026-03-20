---
name: testing-e2e-patterns
description: "Activates for Playwright E2E test patterns, Page Object Model, locator strategies, and test reliability"
---

# E2E Patterns Skill

Provide best practices and patterns for end-to-end testing with Playwright.

## When to Activate

- During E2E test creation or modification
- When `/cdf:e2e` command is invoked
- When debugging flaky tests
- When setting up browser automation
- When user mentions "playwright", "e2e", "browser test"

---

## Pattern Index

| Pattern | When to Use |
|---------|-------------|
| Page Object Model | Encapsulating page interactions for reuse |
| Test file structure | Organizing test suites with beforeEach setup |
| Auth state sharing | Avoiding repeated login across tests |
| Visual regression | Screenshot comparison testing |

> See `references/templates.md` for POM template, test file template, authentication patterns, and visual testing.

> See `references/ci-config.md` for GitHub Actions E2E workflow configuration.

---

## Locator Selection Guide

### Semantic Selectors (Preferred)
```typescript
// By role (best for accessibility)
page.getByRole('button', { name: 'Submit' })
page.getByRole('textbox', { name: 'Email' })
page.getByRole('heading', { name: 'Welcome', level: 1 })
page.getByRole('link', { name: 'Learn more' })
page.getByRole('checkbox', { name: 'Accept terms' })
page.getByRole('combobox', { name: 'Country' })

// By label (for form elements)
page.getByLabel('Email address')
page.getByLabel('Password')

// By placeholder
page.getByPlaceholder('Search...')

// By text content
page.getByText('Welcome back')
page.getByText(/total.*\$\d+/i)  // Regex for dynamic text
```

### Test IDs (When Semantic Fails)
```typescript
// For complex components without accessible names
page.getByTestId('user-avatar-dropdown')
page.getByTestId('chart-container')

// Add to component
<div data-testid="chart-container">...</div>
```

### Chained Locators (For Specificity)
```typescript
// Within a specific container
page.getByRole('dialog').getByRole('button', { name: 'Confirm' })

// Within a list item
page.getByRole('listitem').filter({ hasText: 'Product A' }).getByRole('button')
```

---

## Wait Strategies

### Auto-waiting (Default)
```typescript
// Playwright auto-waits for actionability
await page.click('button');  // Waits for button to be clickable
await page.fill('input', 'text');  // Waits for input to be editable
```

### Explicit Waits
```typescript
// Wait for element visibility
await expect(page.getByText('Success')).toBeVisible();

// Wait for URL change
await expect(page).toHaveURL('/dashboard');

// Wait for network idle
await page.waitForLoadState('networkidle');

// Wait for specific request
await page.waitForResponse(resp =>
  resp.url().includes('/api/users') && resp.status() === 200
);
```

### Custom Waits (Last Resort)
```typescript
// Wait for custom condition
await page.waitForFunction(() => {
  return document.querySelectorAll('.item').length >= 10;
});

// Polling wait
await expect(async () => {
  const count = await page.locator('.item').count();
  expect(count).toBeGreaterThanOrEqual(10);
}).toPass({ timeout: 5000 });
```

---

## Flaky Test Prevention

### Anti-patterns to Avoid
```typescript
// DON'T: Hard waits
await page.waitForTimeout(1000);

// DON'T: Fragile selectors
await page.click('.btn-primary');
await page.click('#submit');

// DON'T: Assume element position
await page.click({ x: 100, y: 200 });

// DON'T: Race with navigation
await page.click('a');
await page.fill('input', 'text');  // Page might not be loaded
```

### Patterns to Use
```typescript
// DO: Wait for expected state
await expect(page.getByText('Loaded')).toBeVisible();
await page.fill('input', 'text');

// DO: Use semantic selectors
await page.getByRole('button', { name: 'Submit' }).click();

// DO: Chain navigation and assertion
await Promise.all([
  page.waitForURL('/dashboard'),
  page.getByRole('link', { name: 'Dashboard' }).click()
]);

// DO: Retry unstable assertions
await expect(async () => {
  const text = await page.getByTestId('counter').textContent();
  expect(parseInt(text!)).toBeGreaterThan(0);
}).toPass();
```

---

## Debug Checklist

When a test fails:
1. [ ] Check the trace viewer: `npx playwright show-trace trace.zip`
2. [ ] Run with headed browser: `npx playwright test --headed`
3. [ ] Run with debug: `npx playwright test --debug`
4. [ ] Check for race conditions - add explicit waits
5. [ ] Verify locators in Playwright Inspector
6. [ ] Check for flakiness: `npx playwright test --repeat-each=5`

---

## Related Agents
- **e2e-specialist** — Primary consumer for Playwright test patterns and reliability

## Suggested Commands
- `/cdf:e2e` — Run E2E test workflows with pattern enforcement
- `/cdf:test` — Execute tests including E2E suite
- `/cdf:troubleshoot` — Debug flaky or failing E2E tests

## Reference Files

| File | Contents |
|------|----------|
| `references/templates.md` | POM template, test file template, auth patterns, visual testing |
| `references/ci-config.md` | GitHub Actions E2E workflow configuration |
