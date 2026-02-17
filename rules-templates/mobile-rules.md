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

## Platform Rules (`platform-rules.md`)

### Platform-Specific Code
- Isolate in `*.ios.ts` / `*.android.ts` or `platform/[ios|android]/`
- Shared logic stays in common modules — only UI/native APIs diverge
- Test on both platforms before merging

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
```
1. Check permission status
2. If not determined → request permission
3. If denied → show rationale and link to settings
4. Never block app usage on non-critical permissions
5. Request permissions contextually (at point of use, not on launch)
```

### Memory Management
- Dispose listeners and subscriptions in cleanup/unmount
- Cancel network requests on screen exit
- Release image/media resources when off-screen
- Monitor memory usage in development (Xcode Instruments / Android Profiler)
- Avoid storing large objects in state

### Performance
- Measure and optimize startup time (cold + warm)
- Flatten component trees — deep nesting hurts render performance
- Use `FlatList` / `ListView` with proper key extraction for lists
- Minimize bridge calls in React Native (batch when possible)
- Profile animations — target 60fps

## Critical Rules

1. **Never block the UI thread** — heavy work goes to background threads/isolates
2. **Handle all permissions gracefully** — never crash on denial
3. **Support multiple screen sizes** — test on small phones and tablets
4. **Test on real devices** — simulators miss performance and permission issues
5. **Secure storage for secrets** — Keychain/Keystore, never plain AsyncStorage
6. **Graceful degradation offline** — app should function with cached data
7. **App store compliance** — follow platform guidelines for privacy, permissions, content
