# Error Handling Patterns

## Use Typed Errors

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

## Handle Errors at Boundaries

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
