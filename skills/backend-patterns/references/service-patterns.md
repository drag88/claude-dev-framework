# Repository & Service Layer Patterns

Data access separation and business logic encapsulation.

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
