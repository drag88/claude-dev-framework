---
name: enforcing-coding-standards
description: "Activates during code implementation and review for naming conventions, DRY/KISS/YAGNI, and code quality standards"
---

# Coding Standards Skill

Enforce consistent code quality principles and patterns across all implementation work.

## When to Activate

- During any code implementation task (`/cdf:implement`)
- When reviewing or refactoring code
- When writing new functions, classes, or modules
- When the user requests coding guidance or best practices

---

## Pattern Index

### Core Principles

| Principle | Rule |
|-----------|------|
| Readability First | Optimize for human understanding over cleverness |
| KISS | Simplest solution that works is usually best |
| DRY | Extract repeated logic, avoid premature abstraction |
| YAGNI | Don't build for hypothetical future requirements |

### Readability First

```typescript
// BAD: Clever but unclear
const r = a.filter(x => x.t === 'p' && x.s > 0).map(x => x.v);

// GOOD: Clear and intentional
const activeProducts = items
  .filter(item => item.type === 'product' && item.stock > 0)
  .map(item => item.value);
```

### KISS (Keep It Simple, Stupid)

```typescript
// BAD: Over-engineered
class UserNameFormatter {
  private strategies = new Map<string, FormatterStrategy>();
  constructor() {
    this.registerStrategy('default', new DefaultStrategy());
    // ... 50 more lines
  }
}

// GOOD: Simple function
function formatUserName(user: User): string {
  return `${user.firstName} ${user.lastName}`.trim();
}
```

### DRY (Don't Repeat Yourself)

```typescript
// BAD: Duplicated logic
function validateEmail(email: string) {
  return email.includes('@') && email.includes('.');
}
function validateUserEmail(user: User) {
  return user.email.includes('@') && user.email.includes('.');
}

// GOOD: Single source of truth
function isValidEmail(email: string): boolean {
  return email.includes('@') && email.includes('.');
}
function validateUserEmail(user: User): boolean {
  return isValidEmail(user.email);
}
```

### YAGNI (You Aren't Gonna Need It)

```typescript
// BAD: Building for imaginary requirements
interface User {
  id: string;
  name: string;
  futureField1?: string;  // "We might need this"
  extensionData?: Record<string, unknown>;  // "For flexibility"
}

// GOOD: Build what you need now
interface User {
  id: string;
  name: string;
}
```

> See `references/naming-conventions.md` for variable/function naming tables and examples.

> See `references/code-smells.md` for detection of long functions, too many parameters, deep nesting, and magic numbers.

> See `references/error-handling.md` for typed errors and boundary handling patterns.

---

## Immutability Pattern (CRITICAL)

Always prefer immutable operations. Mutating data leads to bugs.

### Arrays

```typescript
// BAD: Mutation
const users = [];
users.push(newUser);

// GOOD: Immutable
const users = [...existingUsers, newUser];
const updatedUsers = users.map(user =>
  user.id === targetId ? { ...user, name: 'Updated' } : user
);
```

### Objects

```typescript
// BAD: Mutation
user.name = 'New Name';

// GOOD: Immutable spread
const updatedUser = {
  ...user,
  name: 'New Name',
  address: { ...user.address, city: 'New City' }
};
```

### State Updates (React)

```typescript
// BAD: Direct mutation
items.push(newItem);  // WRONG!
setItems(items);      // Won't trigger re-render

// GOOD: New reference
setItems(prevItems => [...prevItems, newItem]);
setItems(prevItems => prevItems.filter(item => item.id !== targetId));
```

---

## Type Safety Checklist

- [ ] **No `any` types** - Use `unknown` if type is truly unknown
- [ ] **Explicit function return types** - Especially for public APIs
- [ ] **Null checks** - Use optional chaining (`?.`) and nullish coalescing (`??`)
- [ ] **Type guards** - For narrowing union types
- [ ] **Const assertions** - For literal types (`as const`)
- [ ] **Generics** - For reusable type-safe utilities

```typescript
// Type guard example
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value
  );
}

// Const assertion example
const STATUSES = ['pending', 'active', 'complete'] as const;
type Status = typeof STATUSES[number]; // 'pending' | 'active' | 'complete'
```

---

## File Organization Standards

### File Size Limits
- **Components**: < 300 lines
- **Utility files**: < 200 lines
- **Test files**: < 500 lines

### File Naming
| Type | Convention | Example |
|------|------------|---------|
| Component | PascalCase | `UserProfile.tsx` |
| Utility | camelCase | `dateUtils.ts` |
| Constant | SCREAMING_SNAKE | `constants.ts` (content) |
| Type | PascalCase | `types.ts` or `User.types.ts` |
| Test | Component.test | `UserProfile.test.tsx` |
| Hook | use prefix | `useAuth.ts` |

### Module Structure
```typescript
// 1. External imports (alphabetized)
// 2. Internal imports (by type)
// 3. Types/Interfaces
// 4. Constants
// 5. Component/Function
// 6. Helpers (if not extracted)
```

---

## Related Agents
- **quality-engineer** — Uses standards for code review and quality gates
- **refactoring-expert** — Applies standards during code improvement
- **tdd-guide** — Enforces standards in test-driven code
- **/cdf:task with language-specific role framing** — Applies language-specific coding standards
- **/cdf:docs with senior-writer framing** — Uses standards for documentation quality

## Suggested Commands
- `/cdf:implement` — Write code following standards
- `/cdf:improve` — Improve code to meet standards
- `/cdf:analyze --focus quality` — Audit code against standards

## Reference Files

| File | Contents |
|------|----------|
| `references/naming-conventions.md` | Variable/function naming tables, bad vs good examples |
| `references/code-smells.md` | Long functions, too many params, deep nesting, magic numbers |
| `references/error-handling.md` | Typed errors, boundary error handling patterns |
