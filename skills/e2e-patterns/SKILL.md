---
description: "Activate for Playwright E2E test patterns, Page Object Model, locator strategies, and test reliability"
---

# E2E Patterns Skill

Provide best practices and patterns for end-to-end testing with Playwright.

## When to Activate

- During E2E test creation or modification
- When `/cdf:e2e` command is invoked
- When debugging flaky tests
- When setting up browser automation
- When user mentions "playwright", "e2e", "browser test"

## Core Patterns

### Page Object Model Template

```typescript
// pages/[PageName]Page.ts
import { Page, Locator, expect } from '@playwright/test';

export class [PageName]Page {
  readonly page: Page;

  // Locators - defined once, reused everywhere
  readonly [elementName]: Locator;

  constructor(page: Page) {
    this.page = page;
    // Initialize locators using reliable selectors
    this.[elementName] = page.getByRole('...', { name: '...' });
  }

  // Navigation
  async goto() {
    await this.page.goto('/[path]');
    await this.page.waitForLoadState('networkidle');
  }

  // Actions
  async [actionName]() {
    // Perform action
  }

  // Assertions
  async expect[StateName]() {
    await expect(this.[elementName]).toBeVisible();
  }
}
```

### Test File Template

```typescript
// tests/[feature].spec.ts
import { test, expect } from '@playwright/test';
import { [PageName]Page } from '../pages/[PageName]Page';

test.describe('[Feature Name]', () => {
  let [pageName]: [PageName]Page;

  test.beforeEach(async ({ page }) => {
    [pageName] = new [PageName]Page(page);
    await [pageName].goto();
  });

  test('should [expected behavior]', async () => {
    // Arrange
    // Act
    // Assert
  });
});
```

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

## Authentication Patterns

### Shared Auth State
```typescript
// global-setup.ts
import { chromium, FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto('/login');
  await page.fill('#email', process.env.TEST_USER_EMAIL!);
  await page.fill('#password', process.env.TEST_USER_PASSWORD!);
  await page.click('button[type="submit"]');
  await page.waitForURL('/dashboard');

  await page.context().storageState({ path: 'playwright/.auth/user.json' });
  await browser.close();
}

export default globalSetup;
```

### Using Auth State
```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: {
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});
```

## Visual Testing Pattern

```typescript
test('visual regression', async ({ page }) => {
  await page.goto('/dashboard');
  await page.waitForLoadState('networkidle');

  // Full page screenshot
  await expect(page).toHaveScreenshot('dashboard-full.png', {
    fullPage: true,
    maxDiffPixelRatio: 0.01
  });

  // Component screenshot
  await expect(page.getByTestId('chart')).toHaveScreenshot('chart.png');
});
```

## CI Configuration

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright Browsers
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npx playwright test

      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

## Debug Checklist

When a test fails:
1. [ ] Check the trace viewer: `npx playwright show-trace trace.zip`
2. [ ] Run with headed browser: `npx playwright test --headed`
3. [ ] Run with debug: `npx playwright test --debug`
4. [ ] Check for race conditions - add explicit waits
5. [ ] Verify locators in Playwright Inspector
6. [ ] Check for flakiness: `npx playwright test --repeat-each=5`

## Related Agents
- **e2e-specialist** — Primary consumer for Playwright test patterns and reliability

## Suggested Commands
- `/cdf:e2e` — Run E2E test workflows with pattern enforcement
- `/cdf:test` — Execute tests including E2E suite
- `/cdf:troubleshoot` — Debug flaky or failing E2E tests
