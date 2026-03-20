# Code Smell Detection

## Table of Contents

- [Function Too Long](#function-too-long--50-lines)
- [Too Many Parameters](#too-many-parameters--4)
- [Deep Nesting](#deep-nesting--3-levels)
- [Magic Numbers](#magic-numbers)

---

## Function Too Long (> 50 lines)
Split into smaller, focused functions.

## Too Many Parameters (> 4)
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

## Deep Nesting (> 3 levels)
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

## Magic Numbers
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
