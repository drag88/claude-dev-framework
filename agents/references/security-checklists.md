# Security Engineer Checklists & References

## OWASP Top 10 Systematic Checklist

### A01:2021 - Broken Access Control
- [ ] **Authorization checks on all protected endpoints**
- [ ] **Deny by default** - require explicit permission grants
- [ ] **CORS configuration** - restrict allowed origins
- [ ] **JWT validation** - signature, expiry, issuer verification
- [ ] **Directory traversal prevention** - validate file paths

### A02:2021 - Cryptographic Failures
- [ ] **No hardcoded secrets** - use environment variables
- [ ] **Strong encryption** - AES-256, RSA-2048+
- [ ] **HTTPS everywhere** - no mixed content
- [ ] **Password hashing** - bcrypt/argon2 with proper work factor
- [ ] **Secure random generation** - crypto.randomBytes, not Math.random

### A03:2021 - Injection
- [ ] **SQL injection** - parameterized queries only
- [ ] **Command injection** - avoid shell execution, use safe APIs
- [ ] **XSS prevention** - context-aware output encoding
- [ ] **Template injection** - sandbox template engines
- [ ] **LDAP/XML injection** - proper escaping and validation

### A04:2021 - Insecure Design
- [ ] **Threat modeling completed** - attack trees documented
- [ ] **Secure defaults** - fail closed, not open
- [ ] **Rate limiting** - on sensitive operations
- [ ] **Input validation** - allow-list, not deny-list
- [ ] **Business logic validation** - multi-step verification

### A05:2021 - Security Misconfiguration
- [ ] **Default credentials removed**
- [ ] **Error handling** - no stack traces in production
- [ ] **Security headers** - CSP, X-Frame-Options, HSTS
- [ ] **Unnecessary features disabled** - minimal attack surface
- [ ] **Cloud permissions** - principle of least privilege

### A06:2021 - Vulnerable Components
- [ ] **Dependency scanning** - npm audit, Snyk, Dependabot
- [ ] **No known CVEs** in production dependencies
- [ ] **Regular updates** - automated dependency updates
- [ ] **License compliance** - no problematic licenses
- [ ] **Minimal dependencies** - remove unused packages

### A07:2021 - Authentication Failures
- [ ] **Multi-factor authentication** - TOTP, WebAuthn support
- [ ] **Session management** - secure, httpOnly cookies
- [ ] **Brute force protection** - account lockout, CAPTCHA
- [ ] **Password requirements** - minimum complexity
- [ ] **Credential storage** - never log credentials

### A08:2021 - Data Integrity Failures
- [ ] **CI/CD pipeline security** - signed commits, protected branches
- [ ] **Dependency integrity** - lock files, hash verification
- [ ] **Auto-update verification** - signed packages only
- [ ] **Serialization safety** - no untrusted deserialization
- [ ] **Critical data checksums** - integrity verification

### A09:2021 - Security Logging & Monitoring
- [ ] **Comprehensive audit logging** - auth events, access patterns
- [ ] **Log integrity** - tamper-evident, centralized storage
- [ ] **Alerting configured** - anomaly detection
- [ ] **No sensitive data in logs** - PII scrubbing
- [ ] **Incident response plan** - documented procedures

### A10:2021 - Server-Side Request Forgery (SSRF)
- [ ] **URL validation** - allowlist of domains
- [ ] **No user-controlled redirects** to internal services
- [ ] **Network segmentation** - metadata endpoints blocked
- [ ] **Response validation** - expected content type checks
- [ ] **DNS rebinding protection** - resolved IP validation

---

## Vulnerability Pattern Examples

### Hardcoded Secrets

**INCORRECT:**
```javascript
const API_KEY = "sk-live-1234567890abcdef";
const DB_PASSWORD = "supersecretpassword";
```

**CORRECT:**
```javascript
const API_KEY = process.env.API_KEY;
const DB_PASSWORD = process.env.DB_PASSWORD;

// Validate at startup
if (!API_KEY || !DB_PASSWORD) {
  throw new Error("Required environment variables not set");
}
```

### SQL Injection

**INCORRECT:**
```javascript
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);
```

**CORRECT:**
```javascript
const query = "SELECT * FROM users WHERE id = $1";
db.query(query, [userId]);
```

### Command Injection

**INCORRECT:**
```javascript
const result = execSync(`ls ${userInput}`);
```

**CORRECT:**
```javascript
// Use safe APIs instead of shell execution
const files = fs.readdirSync(sanitizedPath);

// If shell is required, use explicit argument arrays
const result = spawnSync("ls", [sanitizedPath], { shell: false });
```

### Cross-Site Scripting (XSS)

**INCORRECT:**
```javascript
element.innerHTML = userInput;
res.send(`<div>${userInput}</div>`);
```

**CORRECT:**
```javascript
import DOMPurify from "dompurify";

element.textContent = userInput; // For text
element.innerHTML = DOMPurify.sanitize(userInput); // If HTML needed

// Server-side
import { escape } from "html-escaper";
res.send(`<div>${escape(userInput)}</div>`);
```

### Server-Side Request Forgery (SSRF)

**INCORRECT:**
```javascript
const response = await fetch(userProvidedUrl);
```

**CORRECT:**
```javascript
import { URL } from "url";

function validateUrl(urlString) {
  const url = new URL(urlString);
  const allowedHosts = ["api.example.com", "cdn.example.com"];

  if (!allowedHosts.includes(url.hostname)) {
    throw new Error("URL host not allowed");
  }

  // Block internal IPs
  const blockedPatterns = [/^10\./, /^172\.(1[6-9]|2|3[01])\./, /^192\.168\./];
  // Note: Resolve DNS and check resolved IP as well

  return url.toString();
}

const safeUrl = validateUrl(userProvidedUrl);
const response = await fetch(safeUrl);
```

### Race Conditions in Financial Operations

**INCORRECT:**
```javascript
async function transfer(fromId, toId, amount) {
  const from = await getAccount(fromId);
  const to = await getAccount(toId);

  if (from.balance >= amount) {
    await updateBalance(fromId, from.balance - amount);
    await updateBalance(toId, to.balance + amount);
  }
}
```

**CORRECT:**
```javascript
async function transfer(fromId, toId, amount) {
  return await db.transaction(async (trx) => {
    // Lock rows for update
    const from = await trx("accounts")
      .where({ id: fromId })
      .forUpdate()
      .first();

    if (from.balance < amount) {
      throw new Error("Insufficient funds");
    }

    await trx("accounts")
      .where({ id: fromId })
      .decrement("balance", amount);

    await trx("accounts")
      .where({ id: toId })
      .increment("balance", amount);

    // Log the transaction
    await trx("transactions").insert({
      from_id: fromId,
      to_id: toId,
      amount,
      timestamp: new Date()
    });
  });
}
```

### Rate Limiting

**INCORRECT:**
```javascript
app.post("/login", async (req, res) => {
  const { email, password } = req.body;
  // No rate limiting - vulnerable to brute force
  const user = await authenticate(email, password);
  res.json({ token: generateToken(user) });
});
```

**CORRECT:**
```javascript
import rateLimit from "express-rate-limit";
import RedisStore from "rate-limit-redis";

const loginLimiter = rateLimit({
  store: new RedisStore({ client: redisClient }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts per window
  keyGenerator: (req) => req.body.email, // Rate limit per email
  handler: (req, res) => {
    res.status(429).json({
      error: "Too many login attempts. Try again later."
    });
  }
});

app.post("/login", loginLimiter, async (req, res) => {
  // ... authentication logic
});
```

### Sensitive Data Logging

**INCORRECT:**
```javascript
console.log("Login attempt:", { email, password });
logger.info("User data:", user);
```

**CORRECT:**
```javascript
const sanitizeForLogging = (data) => {
  const sensitive = ["password", "token", "ssn", "credit_card"];
  return Object.keys(data).reduce((acc, key) => {
    acc[key] = sensitive.includes(key.toLowerCase())
      ? "[REDACTED]"
      : data[key];
    return acc;
  }, {});
};

logger.info("Login attempt:", sanitizeForLogging({ email, password }));
```

---

## Pre-Landing Review Patterns

Specific, actionable patterns for pre-landing code review. Each pattern includes what to grep for, why it matters, and the fix.

### CRITICAL Patterns

#### TOCTOU Races (Time-of-Check to Time-of-Use)

**What to look for**: Check-then-set patterns that are not atomic. `find_or_create_by` on columns without a unique DB index. Status transitions that read current status, then update separately.

**Why it matters**: Concurrent requests slip through the gap between check and set, creating duplicates or invalid state transitions.

**INCORRECT:**
```ruby
# Two concurrent calls both find nil, both create — duplicate record
user = User.find_by(email: params[:email])
user ||= User.create!(email: params[:email])

# Non-atomic status transition — two workers can both "claim" the job
job = Job.find(id)
if job.status == "pending"
  job.update!(status: "processing")
end
```

**CORRECT:**
```ruby
# Atomic upsert backed by a UNIQUE index on email
user = User.find_or_create_by!(email: params[:email])
# AND: add_index :users, :email, unique: true in migration

# Atomic WHERE-old-status UPDATE-new-status
updated = Job.where(id: id, status: "pending")
              .update_all(status: "processing")
raise StaleJobError if updated.zero?
```

#### LLM Output Trust Boundary

**What to look for**: LLM-generated values (emails, URLs, names) written to DB without format validation. Structured tool output (arrays, hashes) accepted without type or shape checks.

**Why it matters**: LLMs hallucinate syntactically invalid data. Persisting it corrupts downstream systems.

**INCORRECT:**
```ruby
# LLM returns {"email": "not-a-real-email", "url": "javascript:alert(1)"}
user.update!(email: llm_result["email"])
redirect_to llm_result["url"]
```

**CORRECT:**
```ruby
email = llm_result["email"].to_s.strip
raise InvalidLLMOutput unless email.match?(URI::MailTo::EMAIL_REGEXP)

url = URI.parse(llm_result["url"].to_s.strip)
raise InvalidLLMOutput unless url.is_a?(URI::HTTPS)

user.update!(email: email)
redirect_to url.to_s
```

#### html_safe on User Data

**What to look for**: Any `.html_safe`, `raw()`, or string interpolation into an `html_safe` output where the interpolated value is user-controlled.

**Why it matters**: Bypasses Rails auto-escaping, opening a direct XSS vector.

**INCORRECT:**
```erb
<%= "Welcome, #{user.name}".html_safe %>
<%= raw(comment.body) %>
```

**CORRECT:**
```erb
<%= "Welcome, #{ERB::Util.html_escape(user.name)}".html_safe %>
<%= sanitize(comment.body) %>
```

### INFORMATIONAL Patterns

#### Conditional Side Effects

**What to look for**: Code paths branching on a condition where one branch performs a side effect (write, enqueue, notify) and the other silently skips it.

**Why it matters**: The "happy path" works, but the alternative path has a missing side effect that surfaces as a subtle bug in production.

**INCORRECT:**
```ruby
if item.featured?
  item.update!(promoted: true)
  item.attach_promo_url(generate_url(item))  # only attached when featured
end
# Non-featured items promoted elsewhere never get a promo URL
```

**CORRECT:**
```ruby
item.update!(promoted: true)
item.attach_promo_url(generate_url(item))  # always attach when promoting
# OR: explicitly document why the side effect is conditional
```

#### LLM Prompt Issues

**What to look for**: 0-indexed lists in prompts (LLMs return 1-indexed). Prompt text listing tools/options that do not match what is actually wired up. Word or token limits stated in multiple places that could drift out of sync.

**Why it matters**: Off-by-one tool selection causes wrong actions. Stale prompt text silently degrades LLM accuracy.

**INCORRECT:**
```python
prompt = """Pick a tool (0=search, 1=calculate, 2=summarize)"""
# LLM returns "1" meaning "search" in its 1-indexed world

MAX_TOKENS = 500   # in prompts/system.txt
MAX_TOKENS = 1000  # in config/llm.yaml — which one wins?
```

**CORRECT:**
```python
prompt = """Pick a tool (1=search, 2=calculate, 3=summarize)"""
# Use 1-indexed lists in all LLM-facing text

# Single source of truth for limits
MAX_TOKENS = settings.LLM_MAX_TOKENS  # defined once in config
```

#### Crypto & Entropy

**What to look for**: Truncating tokens/hashes instead of hashing (reduces entropy). `rand()` or `Random.rand` for security-sensitive values. Non-constant-time comparisons on secrets.

**Why it matters**: Weak entropy makes tokens guessable. Timing side-channels leak secret values byte by byte.

**INCORRECT:**
```ruby
token = SecureRandom.hex(32)[0..7]        # 8 hex chars = 32 bits — brute-forceable
reset_code = rand(999999).to_s.rjust(6, '0')  # predictable PRNG
Rack::Utils.secure_compare(token, params[:token])  # correct, but...
params[:token] == stored_token                      # timing attack
```

**CORRECT:**
```ruby
token = SecureRandom.hex(32)                          # full 256-bit entropy
reset_code = SecureRandom.random_number(10**6).to_s.rjust(6, '0')
ActiveSupport::SecurityUtils.secure_compare(token, stored_token)
```

#### Time Window Safety

**What to look for**: Date-key lookups assuming "today" covers a full 24-hour window. Mismatched time windows between related features (e.g., rate limit resets at midnight but quota checks use rolling 24h).

**Why it matters**: Edge-of-day requests fall through cracks. Mismatched windows cause silent over- or under-counting.

**INCORRECT:**
```ruby
# "today" in server timezone — user in UTC+12 sees tomorrow's data
key = "usage:#{Date.today}"
cache.increment(key)

# Rate limit resets at midnight, but quota is "last 24 hours"
limit_key = "limit:#{Date.today}:#{user.id}"  # resets at midnight
quota_used = Usage.where("created_at > ?", 24.hours.ago).count  # rolling
```

**CORRECT:**
```ruby
# Use UTC consistently and include the full time boundary
key = "usage:#{Time.now.utc.strftime('%Y-%m-%d')}"
cache.increment(key)

# Align both to the same window type
window_start = Time.now.utc.beginning_of_day
quota_used = Usage.where("created_at >= ?", window_start).count
```

#### Type Coercion at Boundaries

**What to look for**: Values crossing language boundaries (Ruby to JSON to JS, Python to SQL) where type could change silently. Hash or digest inputs not calling `.to_s` before serialization.

**Why it matters**: `nil` becomes `"null"`, integers become strings, and your digest of `123` differs from your digest of `"123"`.

**INCORRECT:**
```ruby
# amount is BigDecimal in Ruby, becomes float in JSON — precision loss
render json: { amount: order.amount }

# Digest input might be nil, Integer, or String
digest = Digest::SHA256.hexdigest(record.external_id)  # TypeError if nil
```

**CORRECT:**
```ruby
render json: { amount: order.amount.to_s }  # preserve precision as string

# Always coerce to string before hashing
digest = Digest::SHA256.hexdigest(record.external_id.to_s)
```

---

## Security Testing Commands

### Dependency Scanning
```bash
# NPM audit for vulnerabilities
npm audit --audit-level=high

# More comprehensive with Snyk
npx snyk test

# Check for outdated packages
npm outdated
```

### Secret Detection
```bash
# TruffleHog for secrets in git history
npx trufflehog filesystem . --json

# Gitleaks for pre-commit
gitleaks detect --source=. --verbose

# Quick grep for common secrets
grep -rn "password\|secret\|api_key\|private_key" --include="*.js" --include="*.ts" .
```

### Static Analysis Security Testing (SAST)
```bash
# ESLint with security plugin
npx eslint . --plugin security --rule "security/*"

# Semgrep for security patterns
semgrep --config=p/security-audit .

# NodeJsScan for Node.js apps
nodejsscan --directory .
```

### Dynamic Analysis
```bash
# OWASP ZAP quick scan
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://localhost:3000

# Nuclei for vulnerability scanning
nuclei -u http://localhost:3000 -t cves/

# SQLMap for SQL injection testing (authorized testing only)
sqlmap -u "http://localhost:3000/api/user?id=1" --batch
```

---

## Security Review Report Template

```markdown
# Security Review Report

## Summary
- **Application**: [Name]
- **Version**: [Version]
- **Review Date**: [Date]
- **Reviewer**: [Name]
- **Scope**: [Files/components reviewed]

## Findings Overview
| Severity | Count |
|----------|-------|
| CRITICAL | 0     |
| HIGH     | 0     |
| MEDIUM   | 0     |
| LOW      | 0     |

## Detailed Findings

### [CRITICAL-001] Hardcoded API Key
**Location**: `src/services/payment.ts:42`
**Description**: Production API key is hardcoded in source code.
**Impact**: Credential exposure leading to unauthorized access.
**Remediation**: Move to environment variables. Rotate compromised key.
**References**: CWE-798, OWASP A02:2021

### [HIGH-001] SQL Injection Vulnerability
**Location**: `src/api/users.ts:128`
**Description**: User input directly concatenated into SQL query.
**Impact**: Database compromise, data exfiltration, privilege escalation.
**Remediation**: Use parameterized queries.
**References**: CWE-89, OWASP A03:2021

## Recommendations
1. Implement pre-commit secret scanning
2. Add SAST to CI/CD pipeline
3. Schedule quarterly security reviews
4. Enable dependency vulnerability alerts

## Sign-off
- [ ] All CRITICAL findings addressed
- [ ] All HIGH findings addressed or accepted with risk documentation
- [ ] Security team approval obtained
```

---

## Gate Classification

Which pre-landing review patterns block deployment vs. serve as advisory warnings.

```
CRITICAL (blocks deployment):
├─ SQL & Data Safety (A03 Injection, parameterized queries)
├─ TOCTOU Races & Concurrency (atomic check-and-set, unique indexes)
├─ LLM Output Trust Boundary (validate before persisting)
└─ html_safe on User Data (XSS via escaped output bypass)

INFORMATIONAL (advisory):
├─ Conditional Side Effects (missing side effect on alternate branch)
├─ LLM Prompt Issues (index mismatch, stale tool lists, drifting limits)
├─ Crypto & Entropy (truncation, weak PRNG, timing attacks)
├─ Time Window Safety (timezone assumptions, mismatched windows)
└─ Type Coercion at Boundaries (cross-language type drift, nil digests)
```
