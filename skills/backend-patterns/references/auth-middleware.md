# Authentication & Authorization Patterns

Middleware, JWT tokens, and RBAC implementations.

---

## Authentication Middleware

```typescript
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

## JWT Token Pattern

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

---

## RBAC Pattern

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

  if (rolePermissions.includes(`${action}:${resource}`)) {
    return true;
  }

  if (rolePermissions.includes(`${action}:*`)) {
    return true;
  }

  if (rolePermissions.includes(`${action}:${resource}:own`)) {
    return ownerId === userId;
  }

  return false;
}
```
