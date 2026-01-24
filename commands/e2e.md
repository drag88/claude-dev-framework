---
description: "Specialized E2E testing workflow with Playwright patterns and flaky test handling"
---

# /cdf:e2e - End-to-End Testing

## Triggers
- E2E test creation and execution requests
- Browser automation testing needs
- Cross-browser compatibility testing
- Visual regression and screenshot testing

## Usage
```
/cdf:e2e [action] [target] [--browser chromium|firefox|webkit|all] [--headed] [--debug]
```

## Arguments
- `action`: run | create | debug | report
- `target`: Test file, directory, or pattern
- `--browser`: Browser to use (default: chromium)
- `--headed`: Run with visible browser
- `--debug`: Enable Playwright inspector

## Behavioral Flow

### Running Tests
```bash
/cdf:e2e run
# Runs all e2e tests in headless mode

/cdf:e2e run tests/checkout.spec.ts --headed
# Run specific test with visible browser

/cdf:e2e run --browser all
# Cross-browser testing
```

### Creating Tests
```bash
/cdf:e2e create "user login flow"
# Creates new test file with Page Object Model structure
```

### Debugging Tests
```bash
/cdf:e2e debug tests/failing.spec.ts
# Opens Playwright inspector for step-through debugging
```

## Page Object Model Pattern

All E2E tests should use Page Object Model for maintainability.

### Page Object Structure
```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getErrorMessage() {
    return this.errorMessage.textContent();
  }
}
```

### Test Using Page Object
```typescript
// tests/login.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('Login Flow', () => {
  test('should login successfully with valid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'password123');

    await expect(page).toHaveURL('/dashboard');
  });

  test('should show error for invalid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@example.com', 'wrongpassword');

    await expect(loginPage.errorMessage).toBeVisible();
    await expect(loginPage.errorMessage).toContainText('Invalid credentials');
  });
});
```

## Flaky Test Handling

### Detecting Flaky Tests
```bash
# Run tests multiple times to detect flakiness
npx playwright test --repeat-each=5

# Use retries in CI
npx playwright test --retries=2
```

### Fixing Common Flakiness

#### 1. Wait for Network Idle
```typescript
// BAD: Clicking before page is ready
await page.click('button');

// GOOD: Wait for network
await page.waitForLoadState('networkidle');
await page.click('button');
```

#### 2. Use Proper Assertions
```typescript
// BAD: Hard wait
await page.waitForTimeout(1000);

// GOOD: Wait for expected state
await expect(page.getByText('Success')).toBeVisible();
```

#### 3. Handle Animations
```typescript
// Wait for animations to complete
await page.getByRole('button').click();
await page.waitForFunction(() => {
  return !document.querySelector('.animating');
});
```

#### 4. Retry Unstable Actions
```typescript
// Use test.retry for known flaky tests
test('sometimes flaky test', async ({ page }) => {
  test.retry(2);
  // test code
});
```

## MCP Integration
- **Playwright MCP**: Auto-activated for browser automation
- **Enhanced Capabilities**: Cross-browser testing, visual comparison

## Tool Coordination
- **Bash**: Playwright CLI execution
- **Read/Write**: Page object and test file management
- **Glob**: Test discovery

## Test Organization

```
tests/
├── e2e/
│   ├── pages/              # Page objects
│   │   ├── BasePage.ts
│   │   ├── LoginPage.ts
│   │   └── DashboardPage.ts
│   ├── fixtures/           # Test fixtures
│   │   └── auth.ts
│   ├── auth.spec.ts        # Auth flow tests
│   ├── checkout.spec.ts    # Checkout flow tests
│   └── user.spec.ts        # User management tests
├── playwright.config.ts
└── global-setup.ts
```

## Best Practices

### Use Reliable Locators
```typescript
// Priority order (most to least reliable)
page.getByRole('button', { name: 'Submit' })  // Best: semantic
page.getByLabel('Email')                       // Good: accessible
page.getByTestId('submit-btn')                 // OK: stable
page.locator('.btn-primary')                   // Avoid: fragile
```

### Handle Authentication
```typescript
// global-setup.ts - Login once, reuse state
import { chromium } from '@playwright/test';

async function globalSetup() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto('/login');
  await page.fill('#email', 'test@example.com');
  await page.fill('#password', 'password');
  await page.click('button[type="submit"]');

  // Save authentication state
  await page.context().storageState({ path: 'auth.json' });
  await browser.close();
}

export default globalSetup;
```

### Visual Testing
```typescript
test('should match visual snapshot', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixels: 100
  });
});
```

## Boundaries

**Will:**
- Create and run E2E tests using Playwright
- Enforce Page Object Model patterns
- Identify and fix flaky tests
- Provide cross-browser testing

**Will Not:**
- Replace unit or integration tests
- Test external third-party services
- Run tests against production without explicit permission
