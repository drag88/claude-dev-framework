# Monorepo Rules Template

> Template for generating rules in monorepo projects.

## Architecture Additions

### Package Dependency Graph
```
[shared/types] ← [shared/utils] ← [pkg-a] ← [app-web]
                                 ← [pkg-b] ← [app-api]
                                            ← [app-mobile]
```
- Arrows show "depends on" direction
- Shared packages at the bottom, apps at the top
- No circular dependencies allowed

### Workspace Map and Ownership

Generate the workspace map from `pnpm-workspace.yaml` and ownership from `CODEOWNERS` — do not hand-maintain tables here.

### Build Order
- [Turborepo / Nx / Lerna / pnpm — detect from config]
- Build order determined by dependency graph
- Incremental builds cache based on file hash
- CI only builds/tests affected packages

## Change Impact (`change-impact.md`)

### Blast Radius Assessment
Before merging changes to shared packages:
1. List all direct consumers: `[tool command to show dependents]`
2. Run tests for all affected packages
3. Check for type compatibility across consumers
4. Verify no runtime behavior changes leak to consumers

### Impact Levels
| Changed Package | Impact | Required Testing |
|----------------|--------|-----------------|
| `shared/types` | All packages | Full CI |
| `shared/utils` | Direct consumers | Consumer tests |
| `apps/web` | Web only | Web tests + E2E |
| `apps/api` | API only | API tests + integration |

## Patterns

### Import Conventions
Cross-package imports use package names; lint-enforced.

### Workspace Protocol for Internal Deps
```json
{
  "dependencies": {
    "@myorg/shared-types": "workspace:*",
    "@myorg/utils": "workspace:^1.0.0"
  }
}
```
- Use `workspace:*` for always-latest internal deps
- Use `workspace:^version` for version-constrained internal deps
- Never use file: or link: protocols in committed config

### PR Scope
- Prefer single-package PRs for clear review and rollback
- Cross-package PRs acceptable when: adding a shared type + consuming it, or coordinated breaking change
- Never mix unrelated package changes in one PR
- Label PRs with affected packages

### Shared Package Discipline
- Shared packages have stricter review requirements
- Breaking changes in shared packages need RFC or team discussion
- Shared packages must have comprehensive tests (higher coverage threshold)
- Document public API of shared packages

### Version Management
- [Fixed versioning / independent versioning — detect from config]
- Fixed: all packages share one version, released together
- Independent: each package has own version, released separately
- Changesets or conventional commits for automated version bumps
