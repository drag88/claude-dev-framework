# Coding Style Rules Template

Copy this template to `.claude/rules/coding-style.md` and customize for your project.

---

## File Organization

### File Size Limits
| Type | Max Lines |
|------|-----------|
| Component | 300 |
| Service | 400 |
| Utility | 200 |
| Test | 500 |
| Config | 100 |

### Directory Structure
```
src/
├── components/     # UI components
├── pages/          # Page components
├── hooks/          # Custom React hooks
├── services/       # Business logic
├── utils/          # Pure utility functions
├── types/          # TypeScript types
├── constants/      # App constants
├── api/            # API client/routes
└── config/         # Configuration
```

---

## Naming Conventions

### Files
| Type | Convention | Example |
|------|------------|---------|
| Component | PascalCase | `UserProfile.tsx` |
| Hook | camelCase with use | `useAuth.ts` |
| Utility | camelCase | `formatDate.ts` |
| Constant | camelCase | `apiEndpoints.ts` |
| Type | PascalCase | `User.types.ts` |
| Test | [name].test | `UserProfile.test.tsx` |

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
```typescript
// 1. Imports (external, then internal)
import React, { useState } from 'react';
import { Button } from '@/components/ui';

// 2. Types
interface Props {
  userId: string;
  onUpdate: (user: User) => void;
}

// 3. Component
export function UserProfile({ userId, onUpdate }: Props) {
  // 4. Hooks (in order)
  const [user, setUser] = useState<User | null>(null);
  const { data } = useUser(userId);

  // 5. Derived state
  const fullName = `${user?.firstName} ${user?.lastName}`;

  // 6. Effects
  useEffect(() => {
    // ...
  }, [userId]);

  // 7. Handlers
  const handleSubmit = () => {
    // ...
  };

  // 8. Render
  return (
    <div>
      {/* JSX */}
    </div>
  );
}
```

### Component Rules
- One component per file
- Export component, not default
- Props interface above component
- Handlers named `handle*`

---

## Immutability

### Arrays
```typescript
// Add item
const newItems = [...items, newItem];

// Remove item
const filtered = items.filter(item => item.id !== targetId);

// Update item
const updated = items.map(item =>
  item.id === targetId ? { ...item, name: 'New' } : item
);
```

### Objects
```typescript
// Update property
const updated = { ...user, name: 'New Name' };

// Nested update
const updated = {
  ...user,
  address: { ...user.address, city: 'New City' }
};
```

### Never Mutate
```typescript
// BAD
items.push(newItem);
user.name = 'New';
items.sort();

// GOOD
const newItems = [...items, newItem];
const newUser = { ...user, name: 'New' };
const sorted = [...items].sort();
```

---

## Error Handling

### Use Result Types
```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

async function fetchUser(id: string): Promise<Result<User>> {
  try {
    const user = await api.get(`/users/${id}`);
    return { success: true, data: user };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}
```

### Error Classes
```typescript
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} ${id} not found`, 'NOT_FOUND', 404);
  }
}
```

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

```typescript
// 1. React
import React, { useState, useEffect } from 'react';

// 2. External libraries (alphabetical)
import { useQuery } from '@tanstack/react-query';
import { z } from 'zod';

// 3. Internal absolute imports (by type)
import { Button } from '@/components/ui';
import { useAuth } from '@/hooks';
import { UserService } from '@/services';
import { User } from '@/types';
import { formatDate } from '@/utils';

// 4. Relative imports
import { UserAvatar } from './UserAvatar';
import styles from './UserProfile.module.css';
```
