# E2E Test Templates

## Table of Contents

- [Page Object Model Template](#page-object-model-template)
- [Test File Template](#test-file-template)
- [Authentication Patterns](#authentication-patterns)
- [Visual Testing Pattern](#visual-testing-pattern)

---

## Page Object Model Template

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

## Test File Template

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

---

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

---

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
