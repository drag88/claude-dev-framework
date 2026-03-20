---
name: applying-frontend-patterns
description: "Activates for React component patterns, state management, hooks, and frontend performance optimization"
---

# Frontend Patterns Skill

Provide guidance on frontend architecture patterns, React best practices, and UI development.

## When to Activate

- During frontend implementation tasks
- When building React components
- When implementing state management
- When working on performance optimization
- When handling forms, animations, or accessibility

---

## Pattern Index

### Component Patterns

| Pattern | When to Use |
|---------|-------------|
| Composition over Props | Component has 5+ props controlling layout/content |
| Compound Components | Related components share implicit state (Select/Option, Tabs/Tab) |
| Render Props | Component needs to share behavior while letting consumer control rendering |
| Error Boundary | Catching and recovering from render errors |
| Form Handling (RHF + Zod) | Any form with validation requirements |

> See `references/react-patterns.md` for full code examples.

### Custom Hooks

| Hook | Purpose |
|------|---------|
| `useToggle` | Boolean state with toggle/setTrue/setFalse |
| `useAsync` | Async operation with loading/error/data states |
| `useDebounce` | Debounce rapidly changing values |
| `useLocalStorage` | Persist state to localStorage with type safety |

> See `references/custom-hooks.md` for implementations.

### State Management

| Pattern | When to Use |
|---------|-------------|
| Context + Reducer | Shared state across component tree with complex updates |
| Local state | State used by single component or parent-child |
| URL state | Filters, pagination, search -- anything bookmarkable |

> See `references/state-management.md` for Context + Reducer implementation.

### Performance

| Technique | When to Use |
|-----------|-------------|
| `useMemo` | Expensive computations that depend on specific inputs |
| `useCallback` | Callbacks passed to memoized children |
| `React.memo` | Components that re-render with same props |
| `lazy` + `Suspense` | Route-based or component-based code splitting |
| Virtualization | Lists with 100+ items |

> See `references/performance-patterns.md` for code splitting and virtualization examples.

### Animation (Framer Motion)

| Pattern | When to Use |
|---------|-------------|
| Fade in/out | Page transitions, modal appearance |
| List animations | Adding/removing items from lists |
| Shared layout | Expanding cards, tab transitions |

> See `references/animation-patterns.md` for Framer Motion examples.

### Accessibility

| Pattern | When to Use |
|---------|-------------|
| Focus management | Modals, drawers, any overlay |
| ARIA labels | Loading states, form errors, navigation |
| Skip links | Any page with navigation before main content |

> See `references/accessibility-patterns.md` for focus trapping, ARIA patterns, and skip links.

---

## Key Principles

- **Composition over configuration** -- Prefer composable components over prop-heavy ones
- **Colocation** -- Keep state as close to where it's used as possible
- **Derived state** -- Compute from existing state rather than syncing with `useEffect`
- **Progressive enhancement** -- Start with semantic HTML, layer interactivity

## Related Agents
- **frontend-architect** -- Primary consumer for React component and state patterns
- **performance-engineer** -- Uses patterns for frontend performance optimization

## Suggested Commands
- `/cdf:implement` -- Build frontend features using these patterns
- `/cdf:design` -- Design component architecture with pattern guidance
- `/cdf:analyze --focus performance` -- Check frontend performance against standards

## Reference Files

| File | Contents |
|------|----------|
| `references/react-patterns.md` | Composition, compound components, render props, error boundaries, forms |
| `references/custom-hooks.md` | useToggle, useAsync, useDebounce, useLocalStorage |
| `references/state-management.md` | Context + Reducer pattern |
| `references/performance-patterns.md` | Memoization, code splitting, virtualization |
| `references/animation-patterns.md` | Framer Motion fade, list, shared layout animations |
| `references/accessibility-patterns.md` | Focus management, ARIA labels, skip links |
