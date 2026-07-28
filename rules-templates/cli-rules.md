# CLI / Library Rules Template

> Template for generating rules in CLI tools and library/SDK projects.

## Architecture Additions

### Public API Surface Map
```
[package_name]/
├── __init__.py (or index.ts)  — Public exports (THIS IS THE API)
├── core/                       — Internal implementation
├── cli/                        — CLI entry points
│   ├── main.py                 — Argument parsing
│   └── commands/               — Subcommand handlers
├── types/                      — Public type definitions
└── utils/                      — Internal helpers (not exported)
```

### Plugin Architecture (if applicable)
- Plugin interface: `[detect from code — hooks, entry points, abstract classes]`
- Plugin discovery: `[detect — entry_points, directory scan, config file]`
- Plugin isolation: plugins cannot affect core or other plugins

## Public API (`public-api.md`)

### What's Exported
- Only symbols in `__init__.py` / `index.ts` are public API
- Internal modules prefixed with `_` or in `internal/` directory
- Type definitions are part of the public API

### Stability Guarantees
| Symbol | Stability | Can Change In |
|--------|-----------|--------------|
| Public functions/classes | Stable | Major version only |
| CLI flags and subcommands | Stable | Major version only |
| Config file format | Stable | Major version only |
| Internal `_` prefixed | Unstable | Any version |
| Experimental (if flagged) | Unstable | Minor version |

### Deprecation Policy
1. Add deprecation warning in minor version (with migration path)
2. Document in CHANGELOG
3. Remove in next major version
4. Minimum deprecation window: 1 major version cycle

## Versioning (`versioning.md`)

### Semver Rules
| Change | Version Bump | Examples |
|--------|-------------|----------|
| Breaking API change | **Major** | Remove function, change signature, rename CLI flag |
| New feature, backward compatible | **Minor** | New function, new CLI flag, new config option |
| Bug fix, no API change | **Patch** | Fix incorrect behavior, performance improvement |

### What Counts as Breaking
- Removing or renaming a public function/class/method
- Changing function signature (required params, return type)
- Removing or renaming CLI flags/subcommands
- Changing config file format incompatibly
- Changing default behavior in user-visible ways
- Dropping support for a runtime version

## Patterns

### Docstrings
Public symbols carry docstrings in the style already used in the module.

### Error Messages
- Actionable: tell the user what to do, not just what went wrong
- Include context: file path, line number, invalid value
- Suggest fixes when possible
```
# Bad:  "Invalid configuration"
# Good: "Invalid config at ~/.myapp/config.yml: 'timeout' must be a positive integer (got: -5). Set to a value > 0."
```

### stdin/stdout/piping
- Read from stdin when no file argument provided (support piping)
- Output data to stdout, messages/progress to stderr
- Structured output (JSON) available via `--json` or `--format json` flag
- No color/formatting when output is piped (detect TTY)
