---
name: applying-backend-patterns
description: "Activates for API design, repository pattern, caching, auth middleware, and error handling conventions in backend code"
---

# Backend Patterns Skill

Provide guidance on backend architecture patterns, API design, and server-side best practices.

## When to Activate

- During backend implementation tasks
- When designing APIs or services
- When working with databases and data layers
- When implementing authentication, authorization, or security features

---

## Pattern Index

### API Design

| Pattern | When to Use |
|---------|-------------|
| RESTful conventions | Standard CRUD operations on resources |
| Response format | Consistent success/error JSON structure |
| Pagination | List endpoints returning multiple items |

> See `references/api-design.md` for REST conventions table, response formats, and pagination implementation.

### Service Architecture

| Pattern | When to Use |
|---------|-------------|
| Repository | Separate data access from business logic |
| Service Layer | Encapsulate business logic, coordinate side effects |

> See `references/service-patterns.md` for repository interface and service layer implementations.

### Authentication & Authorization

| Pattern | When to Use |
|---------|-------------|
| Auth middleware | Protecting routes with Bearer token verification |
| Authorization middleware | Role-based route protection |
| JWT tokens | Access + refresh token generation and rotation |
| RBAC | Permission checks with wildcard and ownership support |

> See `references/auth-middleware.md` for middleware, JWT, and RBAC implementations.

### Database

| Pattern | When to Use |
|---------|-------------|
| N+1 prevention | Loading related data (eager load or batch) |
| Transactions | Multi-step operations requiring atomicity |
| Caching (decorator) | Frequently read, rarely written data |

> See `references/database-patterns.md` for N+1 fixes, transaction pattern, and cache-aside implementation.

### Error Handling

| Pattern | When to Use |
|---------|-------------|
| Error class hierarchy | Typed errors with status codes (NotFound, Validation, etc.) |
| Error middleware | Global Express error handler |
| Retry with backoff | Transient failures (network, rate limits) |

> See `references/error-handling.md` for error classes, middleware, and retry implementation.

### Observability

| Pattern | When to Use |
|---------|-------------|
| Rate limiting | API abuse prevention (general + auth-specific) |
| Structured logging | Request logging, service-level audit trail |

> See `references/observability.md` for rate limiting config and Pino logging setup.

---

## Key Principles

- **Separation of concerns** -- Controllers handle HTTP, services handle logic, repositories handle data
- **Fail fast** -- Validate at boundaries, throw typed errors early
- **Idempotency** -- PUT/DELETE operations should be safely repeatable
- **Defense in depth** -- Auth middleware + authorization + input validation

## Related Agents
- **backend-architect** -- Primary consumer for API and service layer design
- **security-engineer** -- Uses backend patterns for secure auth and middleware
- **performance-engineer** -- Applies patterns for query optimization and caching

## Suggested Commands
- `/cdf:implement` -- Implement backend features using these patterns
- `/cdf:design` -- Design backend architecture with pattern guidance
- `/cdf:analyze --focus security` -- Audit backend code against pattern standards

## Reference Files

| File | Contents |
|------|----------|
| `references/api-design.md` | REST conventions, response format, pagination |
| `references/service-patterns.md` | Repository pattern, service layer |
| `references/auth-middleware.md` | Auth/authz middleware, JWT tokens, RBAC |
| `references/database-patterns.md` | N+1 prevention, transactions, caching |
| `references/error-handling.md` | Error classes, error middleware, retry with backoff |
| `references/observability.md` | Rate limiting, structured logging |
