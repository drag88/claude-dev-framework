# Backend API Rules Template

> Template for generating rules in Backend / API projects.

## Architecture Additions

### Request Lifecycle
```
Request → Middleware → Auth → Validation → Handler → Service → Repository → DB
                                                        ↓
Response ← Serialization ← Error Handling ← Service Response
```

### Service Boundaries
| Layer | Responsibility | Can Call |
|-------|---------------|---------|
| Handler/Controller | Parse request, call service, format response | Service |
| Service | Business logic, orchestration | Repository, external services |
| Repository | Data access, query building | Database only |
| Middleware | Cross-cutting: logging, auth, rate limiting | Next middleware |

### DB Schema Reference
- Document tables, key relationships, and indexes in `[docs/schema.md or equivalent]`
- Update schema docs when migrations are added

## API Conventions (`api-conventions.md`)

### URL Design
- Resources are nouns, plural: `/users`, `/orders`, `/products`
- Nested resources for ownership: `/users/{id}/orders`
- Actions as sub-resources when CRUD doesn't fit: `/orders/{id}/cancel`
- Consistent casing: [kebab-case / camelCase — detect from existing routes]
- Version prefix: `/api/v1/` (or header-based)

### HTTP Methods
| Method | Purpose | Idempotent | Response |
|--------|---------|-----------|----------|
| GET | Read | Yes | 200 + body |
| POST | Create | No | 201 + body + Location |
| PUT | Full replace | Yes | 200 + body |
| PATCH | Partial update | Yes | 200 + body |
| DELETE | Remove | Yes | 204 no body |

### Pagination
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8
  }
}
```
- Default page size: 20, max: 100
- Cursor-based for large/real-time datasets

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      {"field": "email", "message": "Invalid email format"}
    ]
  }
}
```

## Database Rules (`database-rules.md`)

### Migration Discipline
- **Never modify existing migrations** — always create new ones
- Migrations are forward-only in production
- Name format: `[timestamp]_[descriptive_action].sql`
- Every migration has an `up` and `down` (rollback)
- Test rollbacks locally before merging

### Query Patterns
- Parameterized queries only — never string interpolation
- Use query builder or ORM for complex queries
- Raw SQL allowed for performance-critical paths (with comment explaining why)
- N+1 queries: use eager loading / joins / dataloaders

### Index Strategy
- Every foreign key has an index
- Columns in WHERE clauses of frequent queries are indexed
- Composite indexes match query column order
- Document why each index exists

### Connection Pooling
- Configure pool size based on environment (dev: 5, prod: 20-50)
- Set connection timeout and idle timeout
- Health check queries on connection checkout

## Patterns

### Authentication & Authorization
- Auth middleware validates tokens before handlers
- [RBAC / ABAC — detect from code] for authorization
- Permission checks in service layer, not handlers
- Never trust client-side role claims

### Error Handling
| Status | When | Example |
|--------|------|---------|
| 400 | Invalid input | Missing required field |
| 401 | Not authenticated | Missing/expired token |
| 403 | Not authorized | Insufficient permissions |
| 404 | Not found | Resource doesn't exist |
| 409 | Conflict | Duplicate unique value |
| 422 | Unprocessable | Valid syntax, invalid semantics |
| 500 | Server error | Never expose internals |

### Idempotency
- POST endpoints accept idempotency keys for safe retries
- PUT/DELETE are naturally idempotent
- Side effects (emails, webhooks) use outbox pattern or deduplication

### Backward Compatibility
- API versioning for breaking changes
- Additive changes (new fields) don't need new versions
- Deprecation headers before removal
- Minimum deprecation period: [detect or default 3 months]

## Critical Rules

1. **Never modify existing migrations** — create new ones to alter schema
2. **Parameterized queries only** — never interpolate user input into SQL
3. **Never return internal errors** to clients — log internally, return generic 500
4. **Validate all input** at the boundary — never trust client data
5. **Auth on every endpoint** — no endpoint should be accidentally public
6. **Rate limiting** on public and auth endpoints
7. **Log structured data** — JSON logs with request ID for traceability
