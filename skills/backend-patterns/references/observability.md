# Observability Patterns

Rate limiting and structured logging.

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
