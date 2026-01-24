# Security Rules Template

Copy this template to `.claude/rules/security.md` and customize for your project.

---

## OWASP Top 10 Prevention

### Injection Prevention
- **SQL**: Use parameterized queries exclusively
- **Command**: Avoid shell execution; use safe APIs
- **XSS**: Sanitize all user input before rendering

```typescript
// REQUIRED: Use parameterized queries
const user = await db.query("SELECT * FROM users WHERE id = $1", [userId]);

// FORBIDDEN: String concatenation in queries
// const user = await db.query(`SELECT * FROM users WHERE id = ${userId}`);
```

### Authentication Requirements
- Passwords must be hashed with bcrypt (work factor 12+)
- JWT tokens must expire within 15 minutes
- Refresh tokens must be stored server-side
- Failed login attempts must be rate-limited

### Authorization Rules
- All API endpoints must verify user authorization
- Use role-based access control (RBAC)
- Deny by default, require explicit permission

---

## Secrets Management

### Never Commit
The following must NEVER be in source code:
- API keys (production or staging)
- Database passwords
- JWT secrets
- Private keys
- OAuth client secrets

### Required Environment Variables
```bash
# All secrets must come from environment
DATABASE_URL=
JWT_SECRET=
API_KEY=
```

### Detection
```bash
# Run before commit
npx trufflehog filesystem . --json
gitleaks detect --source=.
```

---

## Input Validation

### All User Input Must Be Validated
```typescript
// Use Zod or similar for validation
const UserInput = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150)
});
```

### File Upload Validation
- Verify file type by content (magic bytes), not just extension
- Limit file size (max 10MB default)
- Scan for malware before storage
- Never execute uploaded files

---

## Data Protection

### Sensitive Data Handling
- PII must be encrypted at rest (AES-256)
- Sensitive fields must be excluded from logs
- API responses must not expose internal errors

### HTTPS Enforcement
- All communications must use HTTPS
- HSTS header required in production
- No mixed content allowed

---

## Security Headers

### Required Headers
```typescript
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
    }
  },
  referrerPolicy: { policy: "strict-origin-when-cross-origin" }
}));
```

---

## Enforcement

### Pre-commit Checks
- [ ] npm audit passes (no high/critical)
- [ ] No secrets in code
- [ ] All inputs validated

### Pre-merge Checks
- [ ] Security review completed
- [ ] OWASP checklist verified
- [ ] Dependency vulnerabilities addressed
