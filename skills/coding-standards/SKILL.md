# Coding Standards Skill

Enforce consistent code quality principles and patterns across all implementation work.

## When to Activate

- During any code implementation task (`/cdf:implement`)
- When reviewing or refactoring code
- When writing new functions, classes, or modules
- When the user requests coding guidance or best practices

## Code Quality Principles

### Readability First
Code is read far more often than it's written. Optimize for human understanding.

```typescript
// BAD: Clever but unclear
const r = a.filter(x => x.t === 'p' && x.s > 0).map(x => x.v);

// GOOD: Clear and intentional
const activeProducts = items
  .filter(item => item.type === 'product' && item.stock > 0)
  .map(item => item.value);
```

### KISS (Keep It Simple, Stupid)
The simplest solution that works is usually the best.

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
Extract repeated logic, but avoid premature abstraction.

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
Don't build features for hypothetical future requirements.

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

---

## Variable and Function Naming Standards

### Variable Naming

| Type | Convention | Example |
|------|------------|---------|
| Boolean | is/has/should/can prefix | `isActive`, `hasPermission`, `shouldRefresh` |
| Array | Plural noun | `users`, `orderItems`, `selectedIds` |
| Object | Singular noun | `user`, `config`, `response` |
| Count | count/total suffix | `userCount`, `totalOrders` |
| Handler | handle prefix | `handleClick`, `handleSubmit` |
| Callback | on prefix | `onClick`, `onSubmit`, `onChange` |

### Function Naming

| Type | Convention | Example |
|------|------------|---------|
| Getter | get prefix | `getUser`, `getUserById` |
| Setter | set prefix | `setUser`, `setActiveState` |
| Checker | is/has/can prefix | `isValid`, `hasAccess`, `canEdit` |
| Transformer | to/from prefix | `toJSON`, `fromDTO` |
| Async fetcher | fetch/load prefix | `fetchUsers`, `loadData` |
| Event handler | handle prefix | `handleClick`, `handleError` |
| Factory | create prefix | `createUser`, `createConnection` |

### Bad vs Good Names

```typescript
// BAD
const d = new Date();
const temp = users.filter(u => u.a);
function proc(x) { /* ... */ }
const flag = true;

// GOOD
const currentDate = new Date();
const activeUsers = users.filter(user => user.isActive);
function processPayment(payment: Payment) { /* ... */ }
const isEmailVerified = true;
```

---

## Immutability Pattern (CRITICAL)

Always prefer immutable operations. Mutating data leads to bugs.

### Arrays

```typescript
// BAD: Mutation
const users = [];
users.push(newUser);
users[0].name = 'Updated';

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
user.address.city = 'New City';

// GOOD: Immutable spread
const updatedUser = {
  ...user,
  name: 'New Name',
  address: {
    ...user.address,
    city: 'New City'
  }
};
```

### State Updates (React)

```typescript
// BAD: Direct mutation
const [items, setItems] = useState([]);
items.push(newItem);  // WRONG!
setItems(items);      // Won't trigger re-render

// GOOD: New reference
setItems(prevItems => [...prevItems, newItem]);
setItems(prevItems => prevItems.filter(item => item.id !== targetId));
setItems(prevItems => prevItems.map(item =>
  item.id === targetId ? { ...item, completed: true } : item
));
```

---

## Error Handling Patterns

### Use Typed Errors

```typescript
// BAD: Generic errors
throw new Error('Something went wrong');

// GOOD: Specific error types
class ValidationError extends Error {
  constructor(public field: string, message: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

class NotFoundError extends Error {
  constructor(public resource: string, public id: string) {
    super(`${resource} with id ${id} not found`);
    this.name = 'NotFoundError';
  }
}
```

### Handle Errors at Boundaries

```typescript
// BAD: Catching everywhere
try {
  const user = await getUser(id);
  try {
    await updateUser(user);
  } catch (e) {
    console.log(e);
  }
} catch (e) {
  console.log(e);
}

// GOOD: Handle at appropriate boundary
async function handleUserUpdate(id: string) {
  try {
    const user = await getUser(id);
    await updateUser(user);
    return { success: true };
  } catch (error) {
    if (error instanceof NotFoundError) {
      return { success: false, code: 'NOT_FOUND' };
    }
    throw error; // Re-throw unexpected errors
  }
}
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
import React from 'react';
import { useQuery } from '@tanstack/react-query';

// 2. Internal imports (by type)
import { Button } from '@/components/ui';
import { useAuth } from '@/hooks';
import { User } from '@/types';
import { formatDate } from '@/utils';

// 3. Types/Interfaces
interface Props { /* ... */ }

// 4. Constants
const DEFAULT_PAGE_SIZE = 20;

// 5. Component/Function
export function UserList({ users }: Props) { /* ... */ }

// 6. Helpers (if not extracted)
function sortUsers(users: User[]) { /* ... */ }
```

---

## Code Smell Detection

### Function Too Long (> 50 lines)
Split into smaller, focused functions.

### Too Many Parameters (> 4)
Use an options object.

```typescript
// BAD
function createUser(name, email, age, role, department, manager) {}

// GOOD
interface CreateUserOptions {
  name: string;
  email: string;
  age?: number;
  role: Role;
  department: string;
  manager?: string;
}
function createUser(options: CreateUserOptions) {}
```

### Deep Nesting (> 3 levels)
Use early returns and extract functions.

```typescript
// BAD
function process(data) {
  if (data) {
    if (data.items) {
      data.items.forEach(item => {
        if (item.active) {
          if (item.value > 0) {
            // ...
          }
        }
      });
    }
  }
}

// GOOD
function process(data) {
  if (!data?.items) return;

  const activeItems = data.items.filter(item => item.active && item.value > 0);
  activeItems.forEach(processItem);
}
```

### Magic Numbers
Use named constants.

```typescript
// BAD
if (password.length < 8) {}
setTimeout(callback, 86400000);

// GOOD
const MIN_PASSWORD_LENGTH = 8;
const ONE_DAY_MS = 24 * 60 * 60 * 1000;

if (password.length < MIN_PASSWORD_LENGTH) {}
setTimeout(callback, ONE_DAY_MS);
```
