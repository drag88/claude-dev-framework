# Project Soul Template

> Template for generating `.claude/rules/soul.md` — the identity and values of this project.

## Identity

- **Name**: [project name from package.json / pyproject.toml / Cargo.toml / go.mod]
- **Purpose**: [1-2 sentences from README or package description]
- **Audience**: [internal team / external developers / end users — detect from docs tone and publish config]
- **Maturity**: [early prototype / active development / stable / maintenance — detect from version, commit frequency]

## Values

Detect from code patterns and project signals:

- **Speed vs Correctness**: [extensive test suite + CI = correctness-first; minimal tests = speed-first]
- **Simplicity vs Features**: [small dep count + focused scope = simplicity; large deps + many modules = features]
- **Convention vs Configuration**: [linter/formatter configs present = convention; flexible patterns = configuration]
- **Stability vs Innovation**: [pinned deps + long release cycles = stability; frequent major bumps = innovation]

## Communication Style

Detect from existing docs, commits, and code:

- **Commit style**: [conventional commits / freeform / squash-merge — check `git log --oneline -20`]
- **Code comments**: [minimal / thorough — sample 5+ source files]
- **Documentation tone**: [formal / casual / technical — check README and docs/]
- **PR culture**: [templates present? required reviewers? linked issues?]

## Naming Conventions

Detect from source code analysis:

- **Variables**: [camelCase / snake_case / PascalCase]
- **Functions**: [camelCase / snake_case]
- **Files**: [kebab-case / camelCase / PascalCase / snake_case]
- **Classes/Types**: [PascalCase / other]
- **Constants**: [UPPER_SNAKE / other]
- **Database**: [snake_case tables, singular/plural naming]
- **API endpoints**: [kebab-case / camelCase / snake_case paths]

## Boundaries

### Sacred Files (never modify without explicit request)
- Lock files: [package-lock.json / yarn.lock / poetry.lock / Cargo.lock]
- Generated code: [*.generated.*, *.min.js, compiled output]
- Migrations: [migrations/, alembic/versions/]
- CI/CD config: [.github/workflows/, Jenkinsfile]

### Never Commit
- `.env`, `.env.local`, `.env.production`
- `*.pem`, `*.key`, credentials files
- Model artifacts, large datasets, checkpoints
- `node_modules/`, `__pycache__/`, `.venv/`

### Review-Required Changes
- Public API surface (exports, route definitions, SDK interfaces)
- Database schema changes
- Authentication / authorization logic
- CI/CD pipeline configuration
- Dependency additions or major version bumps

## Quality Gates

Detect from CI config and scripts:

- **Linting**: [tool and config — eslint, ruff, clippy]
- **Formatting**: [tool — prettier, black, rustfmt]
- **Testing**: [framework and minimum coverage threshold]
- **Type checking**: [tool — tsc, mypy, pyright]
- **Pre-commit hooks**: [present? what runs?]
