# Architecture

## Bird's Eye View

CDF (Claude Dev Framework) is a host-adaptable plugin that turns coding agents into structured engineering assistants. It ships a Claude Code packaged adapter and a Codex packaged adapter on top of a single host-neutral core of commands, agents, skills, rules, and lifecycle hooks.

## Codemap

| Directory | Purpose |
|-----------|---------|
| `commands/` | 21 slash command definitions (markdown + YAML frontmatter). Each file is a complete behavioral spec. Loaded by host adapters as `/cdf:*` commands. |
| `agents/` | 12 real-expertise agent personas (codebase-navigator, library-researcher, deep-research-agent, quality-engineer, refactoring-expert, e2e-specialist, tdd-guide, requirements-analyst, socratic-mentor, business-research-strategist, business-panel-experts, media-interpreter). Symlinked into `~/.claude/agents/` on first session. |
| `skills/` | 26 auto-invoked skill directories (`skills/*/SKILL.md`). Trigger-based, no explicit invocation. |
| `hooks/` | Lifecycle hook configuration (`hooks.json`) — 7 hook entries across 4 event types. |
| `scripts/` | Hook implementation scripts (Python + Bash) and shared utilities in `scripts/lib/`. |
| `rules-templates/` | 17 templates: project-type, best-practice, workflow, the vendored `claudemd-4-7-rulebook.md`, the `agentsmd-codex-rulebook.md`, and the opt-in `extended-rules.md`. |
| `mcp-configs/` | MCP server configuration templates (GitHub, Supabase, Vercel, Cloudflare, PostgreSQL, Redis, Context7). |
| `.claude-plugin/` | Claude Code adapter — `plugin.json`, `marketplace.json` (v1.14.0). |
| `.codex-plugin/` | Codex adapter — `plugin.json` listing skills and command prompts. |
| `.claude/` | Project-local settings, permissions, rules, and runtime memory. |
| `docs/` | `HOSTS.md` (host adapter model), `QUICKSTART.md`, and `solutions/` (institutional knowledge). |

## Key Files

| File | Role |
|------|------|
| `.claude-plugin/plugin.json` | Claude Code plugin metadata, version (1.14.0) |
| `.claude-plugin/marketplace.json` | Marketplace metadata; version and count strings must stay in sync with actual components |
| `.codex-plugin/plugin.json` | Codex plugin metadata; lists every command prompt explicitly |
| `hooks/hooks.json` | Lifecycle hook definitions — single source of truth for hook configuration |
| `scripts/analyze-codebase.py` | SessionStart hook — project type detection and rule generation guidance |
| `scripts/hooks/session-context.py` | SessionStart hook — injects git history + auto-memory context |
| `scripts/lib/utils.py` | Shared utility functions used by all hook scripts |
| `scripts/health-check.py` | Framework drift detector — verifies count-bearing docs match reality |
| `rules-templates/claudemd-4-7-rulebook.md` | Authoritative rulebook for generating Opus 4.7 CLAUDE.md |
| `rules-templates/agentsmd-codex-rulebook.md` | Authoritative rulebook for generating Codex AGENTS.md |

## Component Relationships

```
User Request
    |
    v
Host Adapter (Claude Code or Codex)
    |
    +--> Command Definition (commands/*.md) -- loaded as /cdf:* slash command
    |       |
    |       +--> Real-expertise Agent (agents/*.md) -- spawned via host subagent tool
    |       +--> Auto-invoked Skill (skills/*/SKILL.md) -- triggered by context match
    |
    +--> Lifecycle Hook (Claude Code only) -- scripts/ or scripts/hooks/
    |
    +--> Rules (.claude/rules/*.md) -- always-loaded project context
    |
    +--> Host Instruction File (CLAUDE.md or AGENTS.md) -- always-loaded role + routing
```

## Data Flow

1. **SessionStart**: `analyze-codebase.py` analyzes project and prompts rule generation if missing; `session-context.py` injects recent git history and auto-memory (60s timeout each).
2. **Request Processing**: host loads command definition, selects real agent or role-framed `/cdf:task` prompt, and activates context-matching skills.
3. **PreToolUse** (Bash): `git-push-review.py` and `pre-push-checks.py` warn on risky git operations (5-10s timeout).
4. **PostToolUse** (Edit/Write/MultiEdit): `console-log-detector.py` (5s) and `comment-checker.py` (5s) validate code quality.
5. **Stop**: `task-completeness-check.sh` verifies the agent did not silently skip steps (10s timeout).

## Cross-Cutting Concerns

- **Session Context**: `session-context.py` injects recent git history and auto-memory at session start. CDF owns no semantic memory file — that belongs to Claude's auto-memory directory under `~/.claude/projects/<project>/memory/`.
- **Routing Discipline**: Deleted orchestrator commands (`/cdf:flow`, `/cdf:workflow`) stay deleted. Full lifecycle work uses a clear prompt at `xhigh` effort, or `/cdf:task` for explicit breakdown.
- **Quality Gates**: `comment-checker.py` (35% comment-density threshold), `console-log-detector.py` (debug statements), and `scripts/health-check.py` (count drift) catch framework regressions.
- **Error Recovery**: `failure-recovery` skill activates after 3 consecutive failures (STOP → REVERT → DOCUMENT → CONSULT).
- **Host Neutrality**: Core methodology under `commands/`, `agents/`, `skills/`, `rules-templates/`, `docs/` must not encode Claude-only or Codex-only assumptions unless the file is clearly adapter-specific.

## Architectural Invariants

- Hook scripts use only Python stdlib — no external dependencies. Reason: hooks run on every session start across user machines without an install step.
- Hook input arrives on `sys.stdin` as JSON with a `tool_input` key (not `sys.argv` and not `$TOOL_INPUT`). Hook output is JSON on `sys.stdout` — either `{"additionalContext": "..."}` to inject or `{"decision": "block", "reason": "..."}` to block.
- Commands, agents, and skills are pure markdown with YAML frontmatter — no executable code. All logic belongs in `scripts/`.
- `hooks/hooks.json` is the single source of truth for lifecycle hook configuration.
- Adapter-specific assumptions stay in `.claude-plugin/` or `.codex-plugin/`. Core files use neutral vocabulary (`subagent`, `host skill`, `command prompt`).

## Architectural Patterns

- **Metadata-Driven**: YAML frontmatter declares command and agent behavior.
- **Trigger-Based Skills**: Skills activate on matched context (missing files, thresholds, failures, keyword patterns).
- **Real-Expertise Agents**: Agent files represent concrete capabilities; generic roles (backend, frontend, devops) are handled through prompt framing on `/cdf:task`, not stub agents.
- **Hook Lifecycle**: Pre/Post hooks for validation, enhancement, and logging.
- **Convention over Configuration**: Sensible defaults require no setup.
- **One Core, Many Adapters**: Same `commands/`, `agents/`, `skills/`, `rules-templates/` feed both Claude Code and Codex adapters with host-tailored framing.

## Boundaries

- **Sacred files** (never modify without testing): `hooks/hooks.json`, `scripts/lib/utils.py`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`.
- **Never commit**: `.env`, transient task state, `*.local.json`, MCP credentials, `~/.cdf-logs/`.
- **Review-required**: command/agent/skill definition changes, public hook interface changes, host adapter manifests.

## Extension Points

- Add commands: `commands/*.md` (then update count-bearing docs and run `python3 scripts/health-check.py`).
- Add agents: `agents/*.md` (only for real expertise, never generic role stubs).
- Add skills: `skills/*/SKILL.md`.
- Add hooks: `hooks/hooks.json` → `scripts/` or `scripts/hooks/`.
- Add host adapters: new `.<host>-plugin/` directory with manifests + neutral references back into the core directories above.
