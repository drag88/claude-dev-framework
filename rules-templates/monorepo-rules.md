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

### Workspace Map (`workspace-map.md`)

| Package | Path | Owner | Publish | Description |
|---------|------|-------|---------|-------------|
| [name] | `packages/[name]` | [team/person] | [npm/internal] | [purpose] |
| [name] | `apps/[name]` | [team/person] | [deploy target] | [purpose] |

### Build Order
- [Turborepo / Nx / Lerna / pnpm — detect from config]
- Build order determined by dependency graph
- Incremental builds cache based on file hash
- CI only builds/tests affected packages

### Ownership Matrix
| Area | Primary Owner | Reviewers |
|------|--------------|-----------|
| `packages/shared-*` | [team] | All consumers |
| `apps/web` | [team] | [team] |
| `apps/api` | [team] | [team] |
| CI/CD config | [team] | [platform team] |

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
```typescript
// Use package names, never relative cross-package paths
import { Button } from '@myorg/ui';        // correct
import { Button } from '../../packages/ui'; // WRONG

// Internal imports within a package use relative paths
import { helper } from '../utils/helper';   // correct within package
```

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

## Critical Rules

1. **No circular dependencies** — enforce with lint rule or build tool check
2. **Shared packages need stricter review** — changes affect multiple teams
3. **Check all consumers** before changing shared types or interfaces
4. **Package names in imports** — never relative paths across package boundaries
5. **Scope PRs to single package** when possible — easier to review and revert
6. **Run affected tests** — don't merge with only local tests passing
7. **Respect ownership** — get approval from package owners for changes
8. **Keep shared surface small** — export only what's needed, keep internals private
