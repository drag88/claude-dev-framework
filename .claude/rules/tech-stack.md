# Tech Stack

## Language

- **Python 3** - Hook scripts and utilities
- **Bash** - Shell scripts for hooks
- **Markdown** - Command, agent, skill definitions
- **JSON** - Configuration files
- **YAML** - Frontmatter in markdown files

## Framework

- **Claude Code Plugin System** - Base platform for plugin functionality
- **MCP (Model Context Protocol)** - Integration with external tools

## Key Libraries

| Library | Purpose |
|---------|---------|
| `json` | Configuration parsing |
| `os` | File system operations |
| `subprocess` | Command execution in hooks |
| `pathlib` | Cross-platform path handling |

## Development Tools

- **No build tools required** - Plugin is loaded directly by Claude Code
- **Git** - Version control

## MCP Server Integrations (Optional)

| Server | Purpose |
|--------|---------|
| Context7 | Library documentation lookup |
| Playwright | Browser automation for E2E testing |
| GitHub | Repository management |
| Supabase | Database and auth |
| Vercel | Deployment |
| PostgreSQL | Database access |
| Redis | Cache and data store |

## File Types

| Extension | Purpose |
|-----------|---------|
| `.md` | Commands, agents, skills, documentation |
| `.json` | Configuration (plugin.json, hooks.json) |
| `.py` | Hook scripts |
| `.sh` | Shell scripts |

## Plugin Components

| Component | Count | Format |
|-----------|-------|--------|
| Commands | 29 | Markdown + YAML |
| Agents | 21 | Markdown + YAML |
| Skills | 18 | Markdown + directories |
| Hooks | 16 | JSON + Python/Bash |
| Context Modes | 3 | Markdown |
| Rule Templates | 5 | Markdown |
