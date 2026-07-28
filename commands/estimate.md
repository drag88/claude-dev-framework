---
description: "Provide development estimates for tasks, features, or projects with intelligent analysis"
---

# /cdf:estimate - Development Estimation

## Triggers
- Development planning requiring time, effort, or complexity estimates
- Project scoping and resource allocation decisions
- Feature breakdown needing systematic estimation methodology
- Risk assessment and confidence interval analysis requirements

## Usage
```
/cdf:estimate [target] [--type time|effort|complexity] [--unit hours|days|weeks] [--breakdown]
```

## Behavioral Flow
1. **Analyze**: Examine scope, complexity factors, dependencies, and framework patterns
2. **Calculate**: Apply estimation methodology with historical benchmarks and complexity scoring
3. **Validate**: Cross-reference estimates with project patterns and domain expertise
4. **Present**: Provide detailed breakdown with confidence intervals and risk assessment
5. **Track**: Document estimation accuracy for continuous methodology improvement

Key behaviors:
- Intelligent breakdown analysis with confidence intervals and risk factors
- Use judgement on conventions already in the repo; delegate via `/cdf:task` with role framing only when multi-file fan-out is warranted.

## Examples

```
/cdf:estimate "user authentication system" --type time --unit days --breakdown
```

## Boundaries

**Will:**
- Provide systematic development estimates with confidence intervals and risk assessment
- Generate detailed breakdown analysis with historical benchmark comparisons

**Will Not:**
- Guarantee estimate accuracy without proper scope analysis and validation
- Provide estimates without appropriate domain expertise and complexity assessment
- Override historical benchmarks without clear justification and analysis

