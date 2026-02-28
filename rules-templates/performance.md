# Performance Rules Template

Copy this template to `.claude/rules/performance.md` and customize for your project.

---

## Model Selection (Claude Code)

### Haiku (Quick Tasks)
Use for:
- Simple code fixes (< 20 lines)
- Straightforward questions
- File reads and searches
- Command execution

### Sonnet (Default)
Use for:
- Standard development tasks
- Code refactoring
- Bug fixes
- Documentation

### Opus (Complex Tasks)
Use for:
- Architectural decisions
- Complex debugging
- Multi-file refactoring
- System design

---

## Context Management

### Token Efficiency
- Keep prompts concise
- Don't repeat information already in context
- Use references instead of copying code
- Summarize long outputs

### File Reading
- Read only necessary files
- Use line ranges for large files
- Avoid reading generated files
- Skip node_modules, dist, etc.

### Strategic Compaction
- Compact after major task completion
- Save state before compaction
- Save state before compaction

---

## Code Performance

### Database Queries
```typescript
// GOOD: Single query with includes
const users = await prisma.user.findMany({
  include: { posts: true }
});

// BAD: N+1 queries
const users = await prisma.user.findMany();
for (const user of users) {
  user.posts = await prisma.post.findMany({
    where: { userId: user.id }
  });
}
```

### Pagination Required
```typescript
// All list endpoints must paginate
const users = await prisma.user.findMany({
  take: limit,
  skip: offset,
  orderBy: { createdAt: 'desc' }
});
```

### Caching Strategy
```typescript
// Cache expensive computations
const cached = await redis.get(`user:${id}`);
if (cached) return JSON.parse(cached);

const user = await db.user.findUnique({ where: { id } });
await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
return user;
```

---

## Frontend Performance

### Bundle Size
- Max initial bundle: 200KB (gzipped)
- Max chunk size: 100KB (gzipped)
- Use dynamic imports for routes

### Lazy Loading
```typescript
// Lazy load routes
const Dashboard = lazy(() => import('./pages/Dashboard'));

// Lazy load heavy components
const Chart = lazy(() => import('./components/Chart'));
```

### Memoization
```typescript
// Memoize expensive computations
const sortedData = useMemo(
  () => data.sort((a, b) => a.name.localeCompare(b.name)),
  [data]
);

// Memoize callbacks
const handleClick = useCallback((id) => {
  setSelected(id);
}, []);
```

### Virtualization
```typescript
// For lists > 100 items
import { useVirtualizer } from '@tanstack/react-virtual';
```

---

## API Performance

### Response Time Targets
| Endpoint Type | Target | Max |
|---------------|--------|-----|
| Health check | 10ms | 50ms |
| Simple read | 50ms | 200ms |
| Complex query | 200ms | 1000ms |
| Write operation | 100ms | 500ms |

### Response Size Limits
- Max response: 1MB
- Paginate large collections
- Compress responses > 1KB

---

## Async Operations

### Non-Blocking I/O
```typescript
// GOOD: Parallel operations
const [users, posts, comments] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
  fetchComments()
]);

// BAD: Sequential when parallel possible
const users = await fetchUsers();
const posts = await fetchPosts();
const comments = await fetchComments();
```

### Background Jobs
```typescript
// Don't block response for non-critical work
await response.json({ success: true });

// Queue background work
await queue.add('sendEmail', { userId, template });
```

---

## Monitoring Requirements

### Required Metrics
- Response time (p50, p95, p99)
- Error rate
- Request rate
- Active users

### Logging Performance
```typescript
// Include timing in logs
const start = Date.now();
const result = await expensiveOperation();
logger.info({
  operation: 'expensiveOperation',
  duration: Date.now() - start,
  result: result.status
});
```

---

## Build Performance

### Development
- Use incremental builds
- Enable hot module replacement
- Skip type checking in dev (separate process)

### Production
- Enable tree shaking
- Minify and compress
- Generate source maps (separate files)
- Optimize images

---

## Performance Review Checklist

Before merge:
- [ ] No N+1 query patterns
- [ ] Large lists are paginated
- [ ] Heavy operations are cached
- [ ] Async operations are parallelized
- [ ] Bundle size impact assessed
