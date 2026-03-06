# Error Handling Patterns

Error classes, middleware, and retry strategies.

---

## Error Classes

```typescript
abstract class AppError extends Error {
  abstract statusCode: number;
  abstract code: string;

  constructor(message: string) {
    super(message);
    this.name = this.constructor.name;
  }

  toJSON() {
    return {
      error: {
        code: this.code,
        message: this.message
      }
    };
  }
}

class NotFoundError extends AppError {
  statusCode = 404;
  code = 'NOT_FOUND';

  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`);
  }
}

class ValidationError extends AppError {
  statusCode = 400;
  code = 'VALIDATION_ERROR';

  constructor(
    message: string,
    public details: Array<{ field: string; message: string }>
  ) {
    super(message);
  }

  toJSON() {
    return {
      error: {
        code: this.code,
        message: this.message,
        details: this.details
      }
    };
  }
}
```

---

## Error Handling Middleware

```typescript
function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  logger.error({
    error: error.message,
    stack: error.stack,
    path: req.path,
    method: req.method
  });

  if (error instanceof AppError) {
    return res.status(error.statusCode).json(error.toJSON());
  }

  return res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: process.env.NODE_ENV === 'production'
        ? 'An unexpected error occurred'
        : error.message
    }
  });
}
```

---

## Retry with Exponential Backoff

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries?: number;
    baseDelay?: number;
    maxDelay?: number;
  } = {}
): Promise<T> {
  const { maxRetries = 3, baseDelay = 1000, maxDelay = 30000 } = options;

  let lastError: Error;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      if (attempt < maxRetries - 1) {
        const delay = Math.min(baseDelay * Math.pow(2, attempt), maxDelay);
        await sleep(delay);
      }
    }
  }

  throw lastError!;
}
```
