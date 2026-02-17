# Commands

## Local Development

```bash
# Run Claude with plugin
claude --plugin-dir ./claude-dev-framework

# Verify installation
/cdf:help
```

## Plugin Usage

```bash
# Core development
/cdf:implement "feature description"
/cdf:build
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

# Orchestration
/cdf:task execute "complex task"
/cdf:spawn "multi-step task"
/cdf:panel "strategy discussion"

# Utilities
/cdf:rules generate
/cdf:rules soul-interview
/cdf:docs plan
/cdf:session load --mode dev
/cdf:verify --mode pre-pr
```

## Hook Scripts

```bash
# Run codebase analysis manually
python3 scripts/analyze-codebase.py

# Test utility functions
python3 -c "from scripts.lib.utils import get_project_root; print(get_project_root())"
```

## Validation

```bash
# Validate hooks.json syntax
python3 -m json.tool hooks/hooks.json

# Check script permissions
chmod +x scripts/*.sh scripts/**/*.py
```

## Git Workflow

```bash
# Conventional commit format
git commit -m "feat: add new command"
git commit -m "fix: resolve hook timeout"
git commit -m "docs: update README"

# No Claude attribution in commits (handled by /cdf:git)
```

## Testing

```bash
# Test plugin loading
claude --plugin-dir . -c "/cdf:help"
```
