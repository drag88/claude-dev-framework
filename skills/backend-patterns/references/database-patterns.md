# Database Patterns

N+1 prevention, transactions, and caching strategies.

---

## N+1 Query Prevention

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

---

## Transaction Pattern

```typescript
async function transferFunds(
  fromAccountId: string,
  toAccountId: string,
  amount: number
): Promise<void> {
  await db.$transaction(async (tx) => {
    const fromAccount = await tx.account.findUnique({
      where: { id: fromAccountId },
      select: { balance: true }
    });

    if (!fromAccount || fromAccount.balance < amount) {
      throw new InsufficientFundsError();
    }

    await tx.account.update({
      where: { id: fromAccountId },
      data: { balance: { decrement: amount } }
    });

    await tx.account.update({
      where: { id: toAccountId },
      data: { balance: { increment: amount } }
    });

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

---

## Caching Pattern

```typescript
class CachedUserRepository implements UserRepository {
  constructor(
    private repository: UserRepository,
    private cache: RedisClient
  ) {}

  async findById(id: string): Promise<User | null> {
    const cacheKey = `user:${id}`;

    const cached = await this.cache.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    const user = await this.repository.findById(id);

    if (user) {
      await this.cache.setex(cacheKey, 300, JSON.stringify(user));
    }

    return user;
  }

  async update(id: string, data: UpdateUserData): Promise<User> {
    const user = await this.repository.update(id, data);
    await this.cache.del(`user:${id}`);
    return user;
  }
}
```
