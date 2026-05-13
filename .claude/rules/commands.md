# Commands

## Local Development

```bash
# Run Claude with plugin
claude --plugin-dir ./claude-dev-framework

# Verify installation
/cdf:rules generate
```

## Plugin Usage

```bash
# Core development
/cdf:implement "feature description"
/cdf:test
/cdf:tdd
/cdf:git commit
/cdf:ship

# Analysis
/cdf:analyze src/
/cdf:explain "concept"
/cdf:research "topic"
/cdf:troubleshoot "issue"

# Planning
/cdf:brainstorm "requirements"
/cdf:design "system"
/cdf:estimate "task"
/cdf:plan-review "plan or PRD"
/cdf:approve                          # After plan mode: persist + execute

# Orchestration
/cdf:task execute "complex task"
/cdf:task --breakdown "multi-step task"

# Quality
/cdf:verify --mode pre-pr
/cdf:e2e
/cdf:improve src/

# Documentation
/cdf:docs plan
/cdf:rules generate
/cdf:rules status

# Memory and learning
/cdf:learn status
```

## All 21 Commands

| Command | Purpose |
|---------|---------|
| `/cdf:analyze` | Code analysis (quality, security, performance, architecture) |
| `/cdf:approve` | Approve plan from plan mode, generate docs, recommend execution strategy |
| `/cdf:brainstorm` | Interactive requirements discovery |
| `/cdf:design` | System architecture and API design |
| `/cdf:docs` | Planning and documentation generation |
| `/cdf:e2e` | E2E testing with Playwright |
| `/cdf:estimate` | Development estimates |
| `/cdf:explain` | Code and concept explanations |
| `/cdf:git` | Git operations with smart commit messages |
| `/cdf:implement` | Feature implementation with agent activation |
| `/cdf:improve` | Code quality improvements |
| `/cdf:learn` | Universal skill learning: capture, view, remove, reset, consolidate preferences |
| `/cdf:plan-review` | Pre-implementation plan review gauntlet |
| `/cdf:research` | Deep web research |
| `/cdf:rules` | Project rules management |
| `/cdf:ship` | Automated release pipeline: merge, test, review, push, PR |
| `/cdf:task` | Complex task execution with delegation |
| `/cdf:tdd` | Test-Driven Development workflow |
| `/cdf:test` | Test execution with coverage analysis |
| `/cdf:troubleshoot` | Issue diagnosis and resolution |
| `/cdf:verify` | Pre-PR quality checks |

## Removed Orchestrators

`/cdf:flow` and `/cdf:workflow` were removed in the 1.13.0 leanness pass. For full lifecycle work, write a clear prompt with the requirements and let Opus 4.7 plan natively at `xhigh` effort, or use `/cdf:task` when you need explicit task breakdown and agent fan-out.

## Hook Scripts

```bash
# Run codebase analysis manually
python3 scripts/analyze-codebase.py

# Validate hooks.json syntax
python3 -m json.tool hooks/hooks.json

# Health check
python3 scripts/health-check.py
```

## Git Workflow

```bash
# Conventional commit format
git commit -m "feat: add new command"
git commit -m "fix: resolve hook timeout"
git commit -m "docs: update README"

# No Claude attribution in commits (handled by /cdf:git)
```
