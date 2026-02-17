# Frontend Rules Template

> Template for generating rules in Frontend / React / Next.js projects.

## Architecture Additions

### Component Hierarchy
```
app/ (or pages/)
├── layout.tsx          — Root layout (server component)
├── page.tsx            — Home page
├── [route]/
│   ├── page.tsx        — Route page
│   └── loading.tsx     — Suspense boundary
components/
├── ui/                 — Generic reusable (Button, Modal, Input)
├── features/           — Feature-specific (UserCard, CartSummary)
└── layouts/            — Layout wrappers (Sidebar, Header)
lib/                    — Utilities, API clients, helpers
hooks/                  — Custom React hooks
types/                  — TypeScript type definitions
```

### Server vs Client Boundaries (App Router)
- **Server Components** (default): Data fetching, static content, no interactivity
- **Client Components** (`'use client'`): Event handlers, hooks, browser APIs
- Push `'use client'` as far down the tree as possible
- Server components can import client components, not vice versa

## Component Conventions (`component-conventions.md`)

### File Structure
```
ComponentName/
├── ComponentName.tsx       — Component implementation
├── ComponentName.test.tsx  — Tests
├── ComponentName.stories.tsx — Storybook (if used)
└── index.ts                — Re-export
```

### Props Interface
```typescript
// Props defined as interface, exported for reuse
export interface ComponentNameProps {
  /** Description of required prop */
  requiredProp: string;
  /** Description of optional prop */
  optionalProp?: number;
  /** Callback props prefixed with on */
  onAction?: (value: string) => void;
  /** Children when component is a wrapper */
  children?: React.ReactNode;
}
```

### Component Rules
- One component per file (plus small internal helpers)
- Components are pure — same props produce same output
- Side effects only in hooks or event handlers
- Prefer composition over prop drilling (Context or compound components)

## Accessibility (`accessibility.md`)

### Requirements
- All interactive elements have accessible names (label, aria-label, or aria-labelledby)
- Keyboard navigation works for all interactive flows (Tab, Enter, Escape, Arrow keys)
- Focus management on route changes and modal open/close
- Color contrast ratio: 4.5:1 for normal text, 3:1 for large text
- Images have descriptive `alt` text (decorative images use `alt=""`)
- Form inputs have associated labels
- Error messages are announced to screen readers (aria-live or role="alert")

### Testing
- Run axe-core or similar in CI
- Manual keyboard-only testing for new features
- Screen reader testing for complex interactive components

## Patterns

### State Management
- **Local state**: `useState` for component-scoped state
- **Shared state**: [Context / Zustand / Redux — detect from deps]
- **Server state**: [React Query / SWR / Server Components — detect from deps]
- **URL state**: Search params for shareable/bookmarkable state
- Avoid global state for data that belongs on the server

### Rendering Optimization
- Memoize expensive computations with `useMemo`
- Stabilize callback references with `useCallback` (only when passed to memoized children)
- Use `React.memo` for components that re-render with same props
- Virtualize long lists (>100 items)
- Lazy load routes and heavy components with `React.lazy` or `next/dynamic`

### Image Optimization
- Use `next/image` (Next.js) or responsive `<picture>` elements
- Always specify `width` and `height` to prevent layout shift
- Use `loading="lazy"` for below-fold images
- Serve WebP/AVIF with fallbacks

### Testing Philosophy (Testing Library)
- Test behavior, not implementation: query by role/label, not class/id
- User-centric queries: `getByRole`, `getByLabelText`, `getByText`
- Avoid testing internal state — test what the user sees
- Integration tests > unit tests for components

## Critical Rules

1. **No `any`** in TypeScript — use `unknown` and narrow, or define proper types
2. **No hardcoded API URLs** — use environment variables (`NEXT_PUBLIC_API_URL`)
3. **Images need `alt`, `width`, `height`** — no exceptions
4. **Test behavior, not implementation** — no testing internal state or CSS classes
5. **No direct DOM manipulation** — use refs only when React can't handle it
6. **No `// eslint-disable` without justification** in a comment
7. **Bundle size matters** — check impact of new dependencies (`bundlephobia`)
