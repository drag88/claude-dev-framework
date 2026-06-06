# Commands

## Local Development

```bash
# Run with the local plugin checkout
claude --plugin-dir .

# Verify installation
/cdf:rules generate

# Codex equivalent
codex plugin marketplace add /path/to/claude-dev-framework
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
/cdf:plan "idea, bug, or error"       # Front door: ground, structure, persist, hand off
/cdf:brainstorm "requirements"
/cdf:design "system"
/cdf:estimate "task"
/cdf:plan-review "plan or PRD"         # Optional gauntlet for high-stakes plans

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
/cdf:rules claudemd
/cdf:rules agentsmd
/cdf:rules status

# Memory and learning
/cdf:learn status
```

## All 21 Commands

| Command | Purpose |
|---------|---------|
| `/cdf:analyze` | Code analysis (quality, security, performance, architecture) |
| `/cdf:brainstorm` | Interactive requirements discovery |
| `/cdf:design` | System architecture and API design |
| `/cdf:docs` | Planning and documentation generation |
| `/cdf:e2e` | E2E testing with Playwright |
| `/cdf:estimate` | Development estimates |
| `/cdf:explain` | Code and concept explanations |
| `/cdf:git` | Git operations with conventional commit messages |
| `/cdf:implement` | Feature implementation with agent activation |
| `/cdf:improve` | Code quality improvements |
| `/cdf:learn` | Universal skill learning: capture, view, remove, reset, consolidate preferences |
| `/cdf:plan` | Front door: turn a raw idea, bug, or error into a grounded, structured, durable plan |
| `/cdf:plan-review` | Pre-implementation plan review gauntlet |
| `/cdf:research` | Deep web research |
| `/cdf:rules` | Project rules management: `.claude/rules/`, `CLAUDE.md`, `AGENTS.md` |
| `/cdf:ship` | Automated release pipeline: merge, test, review, push, PR |
| `/cdf:task` | Complex task execution with delegation |
| `/cdf:tdd` | Test-Driven Development workflow |
| `/cdf:test` | Test execution with coverage analysis |
| `/cdf:troubleshoot` | Issue diagnosis and resolution |
| `/cdf:verify` | Pre-PR quality checks |

## Removed Orchestrators

`/cdf:flow` and `/cdf:workflow` were removed in the 1.13.0 leanness pass. Do not reintroduce them. For full lifecycle work, write a clear prompt at `xhigh` effort, or use `/cdf:task` for explicit breakdown and agent fan-out.

## Hook Scripts

```bash
# Run codebase analysis manually
python3 scripts/analyze-codebase.py

# Validate hooks.json syntax
python3 -m json.tool hooks/hooks.json

# Detect framework drift (counts in docs vs reality)
python3 scripts/health-check.py

# Cross-machine setup
./scripts/adopt-skills.sh
```

## Hook Inventory

| Event | Script | Timeout | Purpose |
|-------|--------|---------|---------|
| SessionStart | `scripts/analyze-codebase.py` | 60s | Project type detection, rule generation prompt |
| SessionStart | `scripts/hooks/session-context.py` | 60s | Inject git history + auto-memory |
| PreToolUse (Bash) | `scripts/hooks/git-push-review.py` | 5s | Warn before risky pushes |
| PreToolUse (Bash) | `scripts/hooks/pre-push-checks.py` | 10s | Run pre-push validations |
| PostToolUse (Edit/Write) | `scripts/hooks/console-log-detector.py` | 5s | Flag stray debug statements |
| PostToolUse (Edit/Write/MultiEdit) | `scripts/comment-checker.py` | 5s | Comment-density check (35% threshold) |
| Stop | `scripts/task-completeness-check.sh` | 10s | Verify the agent didn't silently skip steps |

## Git Workflow

```bash
# Conventional commit format
git commit -m "feat: add new command"
git commit -m "fix: resolve hook timeout"
git commit -m "docs: update README"

# No AI attribution in commits (handled by /cdf:git)
```
