---
description: "Pre-PR comprehensive quality check coordinating build, types, lint, tests, and security"
---

## CRITICAL: READ-ONLY BY DEFAULT

**This command does NOT modify files unless `--fix` flag is explicitly provided.**

- Without `--fix`: Report issues only, suggest fixes
- With `--fix`: Apply automatic fixes where safe

DO NOT modify any files during verification unless user explicitly requests fixes.

## MANDATORY EXECUTION ORDER

Run checks in this exact sequence - DO NOT skip or reorder:

1. **Types** - TypeScript/type checking first
2. **Lint** - Code style and quality
3. **Tests** - Unit and integration tests
4. **Security** - Vulnerability scanning (for --mode pre-pr)
5. **Build** - Final compilation check

Each step must complete before the next begins. If a step fails:
- Report the failure with actionable fix suggestions
- Ask user whether to continue or abort
- DO NOT silently skip failed checks

# /cdf:verify - Comprehensive Quality Verification

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
  - `pre-pr`: Full + security scan + coverage
- `--fix`: Auto-fix fixable issues
- `--skip`: Skip specific checks (comma-separated)

## Verification Pipeline

### Quick Mode
```
Types → Lint
```

### Pre-commit Mode (Default)
```
Types → Lint → Affected Tests
```

### Full Mode
```
Build → Types → Lint → Unit Tests → Integration Tests → E2E Tests
```

### Pre-PR Mode
```
Build → Types → Lint → Unit Tests → Integration Tests → E2E Tests → Security → Coverage
```

## Behavioral Flow

### 1. Build Check
```bash
# Verify project builds without errors
npm run build
```

### 2. Type Check
```bash
# TypeScript compilation
npx tsc --noEmit

# Check for any type
npx tsc --noEmit | grep -c "any" || echo "0"
```

### 3. Lint Check
```bash
# ESLint with auto-fix option
npx eslint . --ext .ts,.tsx

# With fix flag
npx eslint . --ext .ts,.tsx --fix
```

### 4. Unit Tests
```bash
# Run unit tests with coverage
npm run test:unit -- --coverage
```

### 5. Integration Tests
```bash
# Run integration tests
npm run test:integration
```

### 6. E2E Tests
```bash
# Run e2e tests (full/pre-pr only)
npx playwright test
```

### 7. Security Scan
```bash
# Dependency vulnerabilities
npm audit --audit-level=high

# Secret detection
npx trufflehog filesystem . --json 2>/dev/null | head -20
```

### 8. Coverage Gate
```bash
# Verify coverage meets threshold
# Statements: 80%
# Branches: 80%
# Functions: 80%
# Lines: 80%
```

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

### Types Check
```markdown
## Type Check Results

**Status**: ✓ Passed

**Details**:
- Compiled 156 files
- No type errors found
- 0 implicit 'any' types
```

### Lint Check
```markdown
## Lint Check Results

**Status**: ✗ Failed

**Errors** (3):
- src/utils.ts:15:5 - 'unusedVar' is defined but never used
- src/api.ts:42:10 - Unexpected any. Specify a different type
- src/hooks.ts:8:1 - Missing return type on function

**Warnings** (2):
- src/config.ts:3:1 - Prefer const over let
- src/types.ts:20:5 - Use type instead of interface for function type

**Auto-fixable**: 2 issues
Run with --fix to resolve automatically.
```

### Test Check
```markdown
## Test Results

**Status**: ✓ Passed

**Summary**:
- Test Suites: 12 passed, 12 total
- Tests: 89 passed, 89 total
- Snapshots: 5 passed, 5 total
- Time: 3.2s

**Coverage**:
| Metric     | Covered | Total  | Percentage |
|------------|---------|--------|------------|
| Statements | 450     | 520    | 86.5%      |
| Branches   | 120     | 145    | 82.8%      |
| Functions  | 85      | 95     | 89.5%      |
| Lines      | 440     | 510    | 86.3%      |
```

### Security Check
```markdown
## Security Scan Results

**Status**: ✓ Passed

**Dependency Audit**:
- 0 critical vulnerabilities
- 0 high vulnerabilities
- 2 moderate vulnerabilities (in dev dependencies only)

**Secret Scan**:
- 0 secrets detected

**Recommendations**:
- Consider updating 'lodash' to fix moderate vulnerability
```

## MCP Integration
- **Quality Engineer Persona**: Activated for comprehensive analysis
- **Test Runner**: Executes test suites with coverage

## Tool Coordination
- **Bash**: Build, type check, lint, test, security commands
- **Glob**: File discovery for affected tests
- **Read**: Configuration file inspection

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
