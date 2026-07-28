# Mobile Rules Template

> Template for generating rules in Mobile (React Native / Flutter / Native) projects.

## Architecture Additions

### Screen Flow
```
App Entry → Auth Flow → Main Navigator
                           ├── Tab 1 → Screen A → Screen B (push)
                           ├── Tab 2 → Screen C
                           └── Tab 3 → Screen D → Modal E (present)
```

### Native Bridge Architecture
- Platform-specific code isolated in `[platform/]` directories
- Bridge interfaces defined with clear TypeScript/Dart types
- Native modules have matching JS/Dart wrappers
- Feature detection over platform checks where possible

### Data Persistence Layer
| Storage | Use Case | Example |
|---------|----------|---------|
| In-memory | Session state, UI state | Auth token, form drafts |
| AsyncStorage / SharedPrefs | Small key-value | User preferences, feature flags |
| SQLite / Realm / Hive | Structured data | Offline cache, local DB |
| Keychain / Keystore | Secrets | Auth tokens, API keys |
| File system | Large blobs | Downloaded media, exports |

Secrets go in Keychain/Keystore, never in plain AsyncStorage or SharedPrefs.

## Platform Rules (`platform-rules.md`)

### Platform-Specific Code
- Isolate in `*.ios.ts` / `*.android.ts` or `platform/[ios|android]/`
- Shared logic stays in common modules — only UI/native APIs diverge
- Test on both platforms before merging, on real devices — simulators miss performance and permission issues
- Follow platform guidelines for privacy, permissions, and content — app store review depends on it

### Native Module Bridging
- Bridge methods return Promises (async by default)
- Error types map to platform-native exceptions
- Null safety across the bridge boundary — validate both sides
- Version-check native module availability at runtime

## Navigation (`navigation.md`)

### Screen Hierarchy
- Document all screens and their navigation relationships
- Deep link routes map 1:1 to screen names
- Navigation state serializable for state restoration

### Deep Linking
- URL scheme: `[app]://[path]` for native, universal links for web
- Every screen reachable via deep link has standalone data loading
- Deep link handling validates auth state before navigation

### Navigation State
- Persist navigation state for app restore (optional, detect from code)
- Reset navigation stack on logout
- Modals and sheets don't affect back stack unless intended

## Patterns

### Offline-First
- Cache API responses for offline access
- Queue mutations when offline, sync when online
- Show cached data with staleness indicator
- Conflict resolution strategy: [last-write-wins / merge / user-choice]
- Network state detection and UI feedback

### Permission Handling
Request permissions at point of use, show a rationale on denial, never hard-fail on a non-critical grant.

### Memory Management
- Dispose listeners and subscriptions in cleanup/unmount
- Cancel network requests on screen exit
- Release image/media resources when off-screen
- Monitor memory usage in development (Xcode Instruments / Android Profiler)
- Avoid storing large objects in state
