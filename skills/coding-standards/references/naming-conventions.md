# Naming Conventions

## Table of Contents

- [Variable Naming](#variable-naming)
- [Function Naming](#function-naming)
- [Bad vs Good Names](#bad-vs-good-names)

---

## Variable Naming

| Type | Convention | Example |
|------|------------|---------|
| Boolean | is/has/should/can prefix | `isActive`, `hasPermission`, `shouldRefresh` |
| Array | Plural noun | `users`, `orderItems`, `selectedIds` |
| Object | Singular noun | `user`, `config`, `response` |
| Count | count/total suffix | `userCount`, `totalOrders` |
| Handler | handle prefix | `handleClick`, `handleSubmit` |
| Callback | on prefix | `onClick`, `onSubmit`, `onChange` |

## Function Naming

| Type | Convention | Example |
|------|------------|---------|
| Getter | get prefix | `getUser`, `getUserById` |
| Setter | set prefix | `setUser`, `setActiveState` |
| Checker | is/has/can prefix | `isValid`, `hasAccess`, `canEdit` |
| Transformer | to/from prefix | `toJSON`, `fromDTO` |
| Async fetcher | fetch/load prefix | `fetchUsers`, `loadData` |
| Event handler | handle prefix | `handleClick`, `handleError` |
| Factory | create prefix | `createUser`, `createConnection` |

## Bad vs Good Names

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
