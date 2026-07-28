---
description: "Comprehensive code analysis across quality, security, performance, and architecture domains"
---

# /cdf:analyze - Code Analysis and Quality Assessment

> Multi-domain code analysis with systematic assessment and prioritized recommendations.

## Quick Start

```bash
# Analyze entire project
/cdf:analyze

# Security-focused analysis
/cdf:analyze src/auth --focus security

# Deep performance analysis
/cdf:analyze --focus performance --depth deep

# Quick quality check
/cdf:analyze src/components --focus quality --depth quick
```

## When to Use

Use `/cdf:analyze` when:
- Assessing code quality before a release or refactor
- Scanning for security vulnerabilities in sensitive components
- Identifying performance bottlenecks in slow areas
- Reviewing architecture and technical debt

**Don't use this command for**: Making code changes (use `/cdf:improve`), troubleshooting specific bugs (use `/cdf:troubleshoot`).

Diff and PR review belong to the `compound-engineering:ce-code-review` host skill; `/cdf:analyze` remains the whole-repo audit tool.

## Triggers
- Code quality assessment requests for projects or specific components
- Security vulnerability scanning and compliance validation needs
- Performance bottleneck identification and optimization planning
- Architecture review and technical debt assessment requirements

## Usage
```
/cdf:analyze [target] [--focus quality|security|performance|architecture] [--depth quick|deep] [--format text|json|report]
```

## Behavioral Flow
1. **Discover**: Categorize source files using language detection and project analysis
2. **Scan**: Apply domain-specific analysis techniques and pattern matching
3. **Evaluate**: Generate prioritized findings with severity ratings and impact assessment
4. **Recommend**: Create actionable recommendations with implementation guidance
5. **Report**: Present comprehensive analysis with metrics and improvement roadmap

Key behaviors:
- Multi-domain analysis combining static analysis and heuristic evaluation
- Intelligent file discovery and language-specific pattern recognition
- Severity-based prioritization of findings and recommendations
- Comprehensive reporting with metrics, trends, and actionable insights

## Examples

```
/cdf:analyze src/auth --focus security --depth deep
```

## Boundaries

**Will:**
- Perform comprehensive static code analysis across multiple domains
- Generate severity-rated findings with actionable recommendations
- Provide detailed reports with metrics and improvement guidance

**Will Not:**
- Execute dynamic analysis requiring code compilation or runtime
- Modify source code or apply fixes without explicit user consent
- Analyze external dependencies beyond import and usage patterns

## Agent Routing

| Focus Area | Approach | When to Use |
|-----------|----------|-------------|
| Code quality | quality-engineer (real agent, kept) | Code smells, complexity, test coverage gaps |
| Security | `/cdf:task` with security-focused role framing | Auth flows, injection risks, data exposure |
| Performance | `/cdf:task` with performance-focused role framing | Bottlenecks, memory leaks, slow queries |
| Architecture | `/cdf:task` with system-design role framing | Dependency analysis, coupling, component boundaries |

## Next Commands
- `/cdf:improve` — Apply fixes for issues found during analysis
- `/cdf:troubleshoot` — Deep-dive into specific problems identified
- `/cdf:test` — Verify fixes after improvements
