---
description: "Execute tests with coverage analysis and automated quality reporting"
---

# /cdf:test - Testing and Quality Assurance

## Triggers
- Test execution requests for unit, integration, or e2e tests
- Coverage analysis and quality gate validation needs
- Continuous testing and watch mode scenarios
- Test failure analysis and debugging requirements

## Usage
```
/cdf:test [target] [--type unit|integration|e2e|all] [--coverage] [--watch] [--fix]
```

## Behavioral Flow
1. **Discover**: Categorize available tests using runner patterns and conventions
2. **Configure**: Set up appropriate test environment and execution parameters
3. **Execute**: Run tests with monitoring and real-time progress tracking
4. **Analyze**: Generate coverage reports and failure diagnostics
5. **Report**: Provide actionable recommendations and quality metrics

Key behaviors:
- Auto-detect test framework and configuration
- Generate comprehensive coverage reports with metrics
- Provide intelligent test failure analysis
- Support continuous watch mode for development
- Use judgement on conventions already in the repo; delegate via `/cdf:task` with role framing only when multi-file fan-out is warranted.

## Examples

```
/cdf:test src/components --type unit --coverage
```

## Boundaries

**Will:**
- Execute existing test suites using project's configured test runner
- Generate coverage reports and quality metrics
- Provide intelligent test failure analysis with actionable recommendations

**Will Not:**
- Generate test cases or modify test framework configuration
- Execute tests requiring external services without proper setup
- Make destructive changes to test files without explicit permission