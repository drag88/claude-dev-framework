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

# Analysis
/cdf:analyze src/
/cdf:explain "concept"
/cdf:research "topic"
/cdf:troubleshoot "issue"

# Planning
/cdf:brainstorm "requirements"
/cdf:design "system"
/cdf:estimate "task"
/cdf:workflow "PRD or requirements"
/cdf:approve                          # After plan mode: persist + execute

# Orchestration
/cdf:flow "brainstorm → docs → implement → verify"
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
```

## All 22 Commands

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
| `/cdf:flow` | Unified workflow: brainstorm → docs → implement → verify |
| `/cdf:git` | Git operations with smart commit messages |
| `/cdf:implement` | Feature implementation with agent activation |
| `/cdf:improve` | Code quality improvements |
| `/cdf:learn` | Universal skill learning: capture, view, remove, reset, consolidate preferences |
| `/cdf:research` | Deep web research |
| `/cdf:rules` | Project rules management |
| `/cdf:ship` | Automated release pipeline: merge, test, review, push, PR |
| `/cdf:task` | Complex task execution with delegation |
| `/cdf:tdd` | Test-Driven Development workflow |
| `/cdf:test` | Test execution with coverage analysis |
| `/cdf:troubleshoot` | Issue diagnosis and resolution |
| `/cdf:verify` | Pre-PR quality checks |
| `/cdf:workflow` | Generate workflows from PRDs |

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
