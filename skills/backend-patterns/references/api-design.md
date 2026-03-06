# API Design Patterns

RESTful conventions, response formats, and pagination patterns.

---

## RESTful Conventions

| Operation | HTTP Method | Path | Status Codes |
|-----------|-------------|------|--------------|
| List | GET | `/users` | 200 |
| Get | GET | `/users/:id` | 200, 404 |
| Create | POST | `/users` | 201, 400 |
| Update | PUT/PATCH | `/users/:id` | 200, 400, 404 |
| Delete | DELETE | `/users/:id` | 204, 404 |

---

## Response Format

```typescript
// Success response
{
  "data": { /* resource or array */ },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 150
  }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

---

## Pagination Pattern

```typescript
interface PaginationParams {
  page?: number;      // 1-indexed
  limit?: number;     // Items per page
  sort?: string;      // Field to sort by
  order?: 'asc' | 'desc';
}

interface PaginatedResponse<T> {
  data: T[];
  meta: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
    hasNext: boolean;
    hasPrev: boolean;
  };
}

// Implementation
async function listUsers(params: PaginationParams): Promise<PaginatedResponse<User>> {
  const page = params.page ?? 1;
  const limit = Math.min(params.limit ?? 20, 100); // Max 100
  const offset = (page - 1) * limit;

  const [users, total] = await Promise.all([
    db.users.findMany({ skip: offset, take: limit }),
    db.users.count()
  ]);

  return {
    data: users,
    meta: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
      hasNext: page * limit < total,
      hasPrev: page > 1
    }
  };
}
```
