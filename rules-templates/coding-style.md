# Coding Style Rules Template

Copy this template to `.claude/rules/coding-style.md` and customize for your project.

---

## File Organization

Split a file when it stops having one job.

---

## Naming Conventions

### Code
```typescript
// Constants: SCREAMING_SNAKE_CASE
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = 'https://api.example.com';

// Variables: camelCase
const userName = 'John';
const isActive = true;

// Functions: camelCase with verb
function getUserById(id: string) {}
function validateEmail(email: string) {}

// Classes: PascalCase
class UserService {}

// Types/Interfaces: PascalCase
interface UserProfile {}
type RequestStatus = 'pending' | 'success' | 'error';

// Enums: PascalCase with SCREAMING values
enum Status {
  ACTIVE = 'ACTIVE',
  INACTIVE = 'INACTIVE'
}
```

---

## TypeScript Standards

### Type Annotations
```typescript
// REQUIRED: Explicit return types for public functions
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// REQUIRED: Interface for object parameters
interface CreateUserOptions {
  email: string;
  name: string;
  role?: Role;
}

function createUser(options: CreateUserOptions): User {}
```

### Avoid These
```typescript
// NO: any type
function process(data: any) {}  // Use unknown

// NO: Type assertions without validation
const user = data as User;  // Use type guard

// NO: Non-null assertion
user!.name;  // Use optional chaining: user?.name
```

---

## React Standards

### Component Structure
Component files: types above the component, hooks before derived state, handlers named `handle*`.

### Component Rules
- One component per file
- Export component, not default

---

## Immutability

Treat state as immutable; if the project uses Immer, mutate inside `produce`.

---

## Error Handling

Errors: follow the project's existing convention (check how current services throw/return).

---

## Comments

### When to Comment
- Complex algorithms
- Non-obvious business logic
- Workarounds with explanation
- TODO with ticket reference

### When NOT to Comment
- Self-explanatory code
- Every function
- What the code does (code should be clear)

### Format
```typescript
// Single line for brief notes

/**
 * Multi-line for complex explanations.
 * Include context and reasoning.
 */

// TODO(PROJ-123): Refactor after API v2 release
// FIXME: Temporary workaround for race condition
// HACK: Required due to library bug
```

---

## Import Order

Import order is lint-enforced — run the lint fix script.
