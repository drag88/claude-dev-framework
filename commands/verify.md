---
description: "Pre-PR comprehensive quality check coordinating build, types, lint, tests, and security"
---

# /cdf:verify — Comprehensive Quality Verification

## Read-only by default
This command does not modify files unless `--fix` is explicitly provided. Without `--fix`, report issues and suggest fixes. With `--fix`, apply automatic fixes where safe.

## Execution order

Run checks in this sequence:

1. **Types** — TypeScript / type checking first
2. **Lint** — Code style and quality
3. **Tests** — Unit and integration tests
4. **Security** — Vulnerability scanning (for `--mode pre-pr`)
5. **Build** — Final compilation check

Each step completes before the next begins. If a step fails, report the failure with actionable fix suggestions and ask the user whether to continue or abort. Skipped checks are reported, never silent.

## Triggers
- Pre-PR quality validation needs
- Pre-commit verification requirements
- CI/CD pipeline quality checks
- Release candidate validation

## Usage
```
/cdf:verify [--mode quick|full|pre-commit|pre-pr] [--fix] [--skip <checks>]
```

## Arguments
- `--mode`: Verification depth (default: pre-commit)
  - `quick`: Types and lint only
  - `pre-commit`: Types, lint, affected tests
  - `full`: All checks including e2e
  - `pre-pr`: Full + security scan + coverage + review
- `--fix`: Auto-fix fixable issues
- `--skip`: Skip specific checks (comma-separated)

## Checks

Detect the project's actual toolchain from config files (package.json scripts, pyproject.toml, Gemfile, etc.) and run the equivalent check — do not assume npm/eslint/jest.

### Build
```bash
npm run build
```

### Types
```bash
npx tsc --noEmit
```

### Lint
```bash
npx eslint . --ext .ts,.tsx

# With --fix
npx eslint . --ext .ts,.tsx --fix
```

### Unit tests
```bash
npm run test:unit -- --coverage
```

### Integration tests
```bash
npm run test:integration
```

### E2E tests
```bash
npx playwright test
```

### Security scan
```bash
# Dependency vulnerabilities
npm audit --audit-level=high

# Secret detection
npx trufflehog filesystem . --json 2>/dev/null | head -20
```

### Coverage gate
Statements, branches, functions, and lines must each meet the configured threshold (default 80%).

### 9. Review Stage (`--mode pre-pr` only)

**Requires**: the compound-engineering plugin. If it is not installed, report the mechanical gate results and note the review stage was skipped — do not improvise a replacement review.

Delegate diff review to the `compound-engineering:ce-code-review` host skill with the literal token `mode:agent`. This stage is report-only: CDF applies findings after the skill returns and does not let the review skill mutate the working tree directly.

## Output Format

### Success
```
✅ /cdf:verify --mode pre-commit PASSED

📊 Results:
  ✓ Types:     No errors
  ✓ Lint:      No warnings
  ✓ Tests:     42 passed (0.8s)
  ✓ Coverage:  85% (above 80% threshold)

Ready for commit!
```

### Failure
```
❌ /cdf:verify --mode pre-commit FAILED

📊 Results:
  ✓ Types:     No errors
  ✗ Lint:      3 errors, 2 warnings
  ✓ Tests:     42 passed
  ✗ Coverage:  72% (below 80% threshold)

Issues to fix:
  1. [LINT] src/utils.ts:15 - no-unused-vars
  2. [LINT] src/api.ts:42 - @typescript-eslint/no-explicit-any
  3. [COVERAGE] Missing tests for src/services/auth.ts

Run '/cdf:verify --fix' to auto-fix lint issues.
```

## Check Details

Report each check in this shape:

```markdown
## <Check>
Status: pass/fail
Details: <n> errors
```

## Configuration

### Project Config (.cdf.json)
```json
{
  "verify": {
    "thresholds": {
      "coverage": 80,
      "lint_errors": 0,
      "type_errors": 0
    },
    "skip": ["e2e"],
    "timeout": 300
  }
}
```

### Custom Checks
Add custom checks to the pipeline:
```json
{
  "verify": {
    "custom": [
      {
        "name": "bundle-size",
        "command": "npm run analyze",
        "threshold": "500kb"
      }
    ]
  }
}
```

## Examples

### Quick Check Before Commit
```
/cdf:verify --mode quick
```

### Full Verification with Fixes
```
/cdf:verify --mode full --fix
```

### Pre-PR Check Skipping E2E
```
/cdf:verify --mode pre-pr --skip e2e
```

## Boundaries

**Will:**
- Run comprehensive quality checks based on mode
- Report issues with actionable details
- Auto-fix when --fix flag is provided
- Gate on configurable thresholds

**Will Not:**
- Deploy or release code
- Modify code without --fix flag
- Skip security checks in pre-pr mode
- Lower thresholds without explicit configuration
