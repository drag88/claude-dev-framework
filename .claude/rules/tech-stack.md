# Tech Stack

## Language

- **Python 3** — Hook scripts and utilities (`scripts/`, `scripts/hooks/`, `scripts/lib/`)
- **Bash** — Shell hooks and the cross-machine bootstrap (`scripts/*.sh`)
- **Markdown** — Command, agent, skill, and rule definitions
- **JSON** — Plugin manifests, hook configuration, marketplace metadata
- **YAML** — Frontmatter in markdown definitions

## Framework

- **Claude Code Plugin System** — Primary packaged adapter (`.claude-plugin/`)
- **Codex Plugin System** — Secondary packaged adapter (`.codex-plugin/`)
- **MCP (Model Context Protocol)** — External tool integration through `mcp-configs/` templates

## Key Libraries

| Library | Purpose |
|---------|---------|
| `json` | Hook I/O contract, manifest parsing |
| `os` | File system operations in hooks |
| `subprocess` | Git introspection and command execution in hooks |
| `pathlib` | Cross-platform path handling |
| `sys` | `stdin`/`stdout` for hook communication |
| `re` | Pattern matching in `comment-checker.py` and `console-log-detector.py` |

Only the Python standard library is allowed in hook scripts. No external runtime dependencies.

## Development Tools

- **No build step** — Plugin is loaded directly by the host (`claude --plugin-dir .` or `codex plugin marketplace add`).
- **Git** — Version control. Conventional commits, no AI attribution.
- **GitHub Actions** — CI validation (`.github/workflows/validate.yml`).
- **`scripts/health-check.py`** — Framework drift detector for count-bearing docs.
- **`scripts/adopt-skills.sh`** — Cross-machine bootstrap helper.

## MCP Server Integrations (Optional Templates)

| Server | Purpose |
|--------|---------|
| Context7 | Library documentation lookup |
| Playwright | Browser automation for E2E testing |
| GitHub | Repository management |
| Supabase | Database and auth |
| Vercel | Deployment |
| PostgreSQL | Database access |
| Redis | Cache and data store |
| Cloudflare | Infrastructure |

Templates live in `mcp-configs/` and are copied per machine into `.mcp/settings.json`.

## File Types

| Extension | Purpose |
|-----------|---------|
| `.md` | Commands, agents, skills, rules, documentation |
| `.json` | Manifests, hook configuration, marketplace metadata |
| `.py` | Hook scripts and utilities |
| `.sh` | Bootstrap and lifecycle shell scripts |

## Plugin Components

| Component | Count | Format |
|-----------|-------|--------|
| Commands | 21 | Markdown + YAML frontmatter |
| Agents | 12 | Markdown + YAML frontmatter |
| Skills | 22 | Directories with `SKILL.md` |
| Hooks | 7 | `hooks.json` entries → Python or Bash scripts |
| Rule Templates | 17 | Markdown |
| Host Adapters | 2 | `.claude-plugin/`, `.codex-plugin/` |

Update these counts in `README.md`, `.claude/rules/architecture.md`, `.claude-plugin/marketplace.json`, and `CLAUDE.md` whenever components are added or removed. Then run `python3 scripts/health-check.py` to catch drift.

## Versioning

- Plugin version lives in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` — keep them in sync.
- Third-party skills tracked in `skills-lock.json` with computed hashes (`npx skills update --frozen-lockfile`).
- Releases are cut on `main` via `/cdf:ship`.
