---
description: "Activate for API design, repository pattern, caching, auth middleware, and error handling conventions in backend code"
---

# Backend Patterns Skill

Provide guidance on backend architecture patterns, API design, and server-side best practices.

## When to Activate

- During backend implementation tasks
- When designing APIs or services
- When working with databases and data layers
- When implementing authentication, authorization, or security features

---

## API Design Patterns

### RESTful Conventions

| Operation | HTTP Method | Path | Status Codes |
|-----------|-------------|------|--------------|
| List | GET | `/users` | 200 |
| Get | GET | `/users/:id` | 200, 404 |
| Create | POST | `/users` | 201, 400 |
| Update | PUT/PATCH | `/users/:id` | 200, 400, 404 |
| Delete | DELETE | `/users/:id` | 204, 404 |

### Response Format

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

### Pagination Pattern

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

---

## Repository Pattern

Separate data access logic from business logic.

```typescript
// Interface
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  findAll(options?: FindOptions): Promise<User[]>;
  create(data: CreateUserData): Promise<User>;
  update(id: string, data: UpdateUserData): Promise<User>;
  delete(id: string): Promise<void>;
}

// Implementation
class PrismaUserRepository implements UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { email } });
  }

  async create(data: CreateUserData): Promise<User> {
    return this.prisma.user.create({ data });
  }

  // ... other methods
}
```

---

## Service Layer Pattern

Encapsulate business logic in services.

```typescript
class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService,
    private eventBus: EventBus
  ) {}

  async createUser(data: CreateUserInput): Promise<User> {
    // Validate
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) {
      throw new ConflictError('Email already in use');
    }

    // Hash password
    const passwordHash = await hashPassword(data.password);

    // Create user
    const user = await this.userRepository.create({
      ...data,
      password: passwordHash,
      status: 'pending_verification'
    });

    // Side effects
    await this.emailService.sendVerificationEmail(user);
    this.eventBus.emit('user.created', { userId: user.id });

    return user;
  }

  async deactivateUser(id: string, reason: string): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new NotFoundError('User', id);
    }

    const updated = await this.userRepository.update(id, {
      status: 'inactive',
      deactivatedAt: new Date(),
      deactivationReason: reason
    });

    this.eventBus.emit('user.deactivated', { userId: id, reason });
    return updated;
  }
}
```

---

## Middleware Pattern

```typescript
// Authentication middleware
async function authenticate(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token) {
    return res.status(401).json({
      error: { code: 'UNAUTHORIZED', message: 'Missing token' }
    });
  }

  try {
    const payload = await verifyToken(token);
    req.user = payload;
    next();
  } catch (error) {
    return res.status(401).json({
      error: { code: 'INVALID_TOKEN', message: 'Invalid or expired token' }
    });
  }
}

// Authorization middleware
function authorize(...roles: Role[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({
        error: { code: 'UNAUTHORIZED', message: 'Not authenticated' }
      });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        error: { code: 'FORBIDDEN', message: 'Insufficient permissions' }
      });
    }

    next();
  };
}

// Usage
app.get('/admin/users', authenticate, authorize('admin'), listUsers);
```

---

## Database Patterns

### N+1 Query Prevention

```typescript
// BAD: N+1 queries
const orders = await db.orders.findMany();
for (const order of orders) {
  order.items = await db.orderItems.findMany({
    where: { orderId: order.id }
  });
}

// GOOD: Eager loading
const orders = await db.orders.findMany({
  include: { items: true }
});

// GOOD: Batch loading
const orders = await db.orders.findMany();
const orderIds = orders.map(o => o.id);
const allItems = await db.orderItems.findMany({
  where: { orderId: { in: orderIds } }
});
const itemsByOrder = groupBy(allItems, 'orderId');
orders.forEach(order => {
  order.items = itemsByOrder[order.id] || [];
});
```

### Transaction Pattern

```typescript
async function transferFunds(
  fromAccountId: string,
  toAccountId: string,
  amount: number
): Promise<void> {
  await db.$transaction(async (tx) => {
    // Lock source account
    const fromAccount = await tx.account.findUnique({
      where: { id: fromAccountId },
      select: { balance: true }
    });

    if (!fromAccount || fromAccount.balance < amount) {
      throw new InsufficientFundsError();
    }

    // Debit source
    await tx.account.update({
      where: { id: fromAccountId },
      data: { balance: { decrement: amount } }
    });

    // Credit destination
    await tx.account.update({
      where: { id: toAccountId },
      data: { balance: { increment: amount } }
    });

    // Create audit log
    await tx.transaction.create({
      data: {
        fromAccountId,
        toAccountId,
        amount,
        type: 'transfer'
      }
    });
  });
}
```

### Caching Pattern

```typescript
class CachedUserRepository implements UserRepository {
  constructor(
    private repository: UserRepository,
    private cache: RedisClient
  ) {}

  async findById(id: string): Promise<User | null> {
    const cacheKey = `user:${id}`;

    // Try cache first
    const cached = await this.cache.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    // Fallback to database
    const user = await this.repository.findById(id);

    // Cache for 5 minutes
    if (user) {
      await this.cache.setex(cacheKey, 300, JSON.stringify(user));
    }

    return user;
  }

  async update(id: string, data: UpdateUserData): Promise<User> {
    const user = await this.repository.update(id, data);

    // Invalidate cache
    await this.cache.del(`user:${id}`);

    return user;
  }
}
```

---

## Error Handling

### Error Classes

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

### Error Handling Middleware

```typescript
function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log error
  logger.error({
    error: error.message,
    stack: error.stack,
    path: req.path,
    method: req.method
  });

  // Handle known errors
  if (error instanceof AppError) {
    return res.status(error.statusCode).json(error.toJSON());
  }

  // Handle unknown errors
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

### Retry with Exponential Backoff

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

---

## Authentication & Authorization

### JWT Token Pattern

```typescript
interface TokenPayload {
  userId: string;
  role: Role;
  iat: number;
  exp: number;
}

function generateTokens(user: User): { accessToken: string; refreshToken: string } {
  const accessToken = jwt.sign(
    { userId: user.id, role: user.role },
    process.env.JWT_SECRET!,
    { expiresIn: '15m' }
  );

  const refreshToken = jwt.sign(
    { userId: user.id, type: 'refresh' },
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: '7d' }
  );

  return { accessToken, refreshToken };
}

async function refreshAccessToken(refreshToken: string): Promise<string> {
  const payload = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET!);

  // Check if refresh token is revoked
  const isRevoked = await isTokenRevoked(refreshToken);
  if (isRevoked) {
    throw new UnauthorizedError('Token revoked');
  }

  const user = await userRepository.findById(payload.userId);
  if (!user) {
    throw new UnauthorizedError('User not found');
  }

  return jwt.sign(
    { userId: user.id, role: user.role },
    process.env.JWT_SECRET!,
    { expiresIn: '15m' }
  );
}
```

### RBAC Pattern

```typescript
const permissions = {
  admin: ['users:read', 'users:write', 'users:delete', 'orders:*'],
  manager: ['users:read', 'orders:read', 'orders:write'],
  user: ['orders:read:own', 'orders:write:own']
} as const;

function hasPermission(
  role: Role,
  action: string,
  resource: string,
  ownerId?: string,
  userId?: string
): boolean {
  const rolePermissions = permissions[role];

  // Check for exact match
  if (rolePermissions.includes(`${action}:${resource}`)) {
    return true;
  }

  // Check for wildcard
  if (rolePermissions.includes(`${action}:*`)) {
    return true;
  }

  // Check for own resource permission
  if (rolePermissions.includes(`${action}:${resource}:own`)) {
    return ownerId === userId;
  }

  return false;
}
```

---

## Rate Limiting

```typescript
import { rateLimit } from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';

// General API rate limit
const apiLimiter = rateLimit({
  store: new RedisStore({ client: redisClient }),
  windowMs: 60 * 1000, // 1 minute
  max: 100, // 100 requests per minute
  standardHeaders: true,
  legacyHeaders: false
});

// Stricter limit for auth endpoints
const authLimiter = rateLimit({
  store: new RedisStore({ client: redisClient }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  keyGenerator: (req) => req.body.email || req.ip,
  handler: (req, res) => {
    res.status(429).json({
      error: {
        code: 'RATE_LIMIT_EXCEEDED',
        message: 'Too many attempts. Please try again later.'
      }
    });
  }
});

app.use('/api', apiLimiter);
app.use('/api/auth/login', authLimiter);
```

---

## Structured Logging

```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label })
  },
  base: {
    service: 'api',
    version: process.env.APP_VERSION
  }
});

// Request logging middleware
function requestLogger(req: Request, res: Response, next: NextFunction) {
  const startTime = Date.now();

  res.on('finish', () => {
    logger.info({
      type: 'request',
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration: Date.now() - startTime,
      userId: req.user?.id
    });
  });

  next();
}

// Usage in services
class OrderService {
  async createOrder(userId: string, items: OrderItem[]) {
    logger.info({ userId, itemCount: items.length }, 'Creating order');

    try {
      const order = await this.orderRepository.create({ userId, items });
      logger.info({ orderId: order.id, userId }, 'Order created successfully');
      return order;
    } catch (error) {
      logger.error({ userId, error: error.message }, 'Failed to create order');
      throw error;
    }
  }
}
```

## Related Agents
- **backend-architect** — Primary consumer for API and service layer design
- **security-engineer** — Uses backend patterns for secure auth and middleware
- **performance-engineer** — Applies patterns for query optimization and caching

## Suggested Commands
- `/cdf:implement` — Implement backend features using these patterns
- `/cdf:design` — Design backend architecture with pattern guidance
- `/cdf:analyze --focus security` — Audit backend code against pattern standards
