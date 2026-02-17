# Infrastructure / DevOps Rules Template

> Template for generating rules in Infrastructure-as-Code and DevOps projects.

## Architecture Additions

### Infrastructure Topology
```
[Cloud Provider]
├── Networking: VPC → Subnets (public/private) → Security Groups → NAT/IGW
├── Compute: [ECS/EKS/Lambda/EC2] → Auto Scaling → Load Balancer
├── Data: [RDS/DynamoDB] → [ElastiCache/Redis] → [S3]
├── Messaging: [SQS/SNS/EventBridge]
└── Observability: [CloudWatch/Datadog] → Alerts → PagerDuty
```

### Terraform Module Tree
```
terraform/
├── modules/
│   ├── networking/    — VPC, subnets, security groups
│   ├── compute/       — ECS/EKS/Lambda definitions
│   ├── database/      — RDS, DynamoDB, ElastiCache
│   └── monitoring/    — Alarms, dashboards, log groups
├── environments/
│   ├── dev/           — Dev variable values
│   ├── staging/       — Staging variable values
│   └── prod/          — Prod variable values
└── main.tf            — Module composition
```

### Deployment Pipeline
```
Code Push → Lint/Validate → Plan → Review → Apply (staging) → Test → Apply (prod)
```

## IaC Conventions (`iac-conventions.md`)

### Module Structure
```hcl
# Every module contains:
# main.tf      — Resource definitions
# variables.tf — Input variables with descriptions and types
# outputs.tf   — Output values
# versions.tf  — Provider and terraform version constraints
# README.md    — Module documentation (auto-generated)
```

### Naming Convention
- Resources: `[project]-[environment]-[component]-[resource]`
- Example: `myapp-prod-api-ecs-service`
- Use consistent separators (hyphens for names, underscores for Terraform identifiers)

### Tagging Standard
Every resource must have:
```hcl
tags = {
  Project     = var.project_name
  Environment = var.environment
  ManagedBy   = "terraform"
  Owner       = var.team_name
  CostCenter  = var.cost_center
}
```

### State Management
- Remote state in [S3 + DynamoDB / Terraform Cloud / GCS]
- State locking enabled — never disable
- One state file per environment per component
- Never manually edit state files — use `terraform state` commands

## Security Baseline (`security-baseline.md`)

### Network Policies
- Default deny — explicitly allow required traffic
- No `0.0.0.0/0` ingress except load balancers on 80/443
- Private subnets for databases and internal services
- VPC endpoints for AWS service access (no public internet)

### IAM / Least Privilege
- Service roles scoped to exact resources needed
- No `*` in resource ARNs for production
- No inline policies — use managed policies attached to roles
- Regular access review and unused permission removal

### Secrets Management
- Secrets in [AWS Secrets Manager / Vault / SSM Parameter Store]
- Never in Terraform variables, tfvars files, or environment variables in code
- Rotate secrets on schedule
- Application reads secrets at runtime, not baked into images

### Encryption
- Encryption at rest enabled for all data stores
- TLS 1.2+ for all transit (no exceptions)
- KMS keys with proper key policies and rotation

## Patterns

### Plan Before Apply
1. `terraform plan -out=plan.tfplan` — always save plan
2. Review plan output — check for unexpected destroys or replacements
3. `terraform apply plan.tfplan` — apply exact reviewed plan
4. Never `terraform apply` without reviewing the plan first

### Variables Over Hardcoded Values
```hcl
# Bad
cidr_block = "10.0.0.0/16"

# Good
cidr_block = var.vpc_cidr
```
- All environment-specific values come from variables
- Defaults only for non-environment-specific values

### Resource Tagging
- Enforce tagging via [AWS Config / Terraform validation / policy-as-code]
- Missing tags = failed CI check
- Tags enable cost allocation, ownership, and automation

### Docker Best Practices
```dockerfile
# Use specific version tags, never :latest
FROM python:3.11-slim AS builder

# Multi-stage builds to minimize image size
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11

# Run as non-root
RUN useradd -r appuser
USER appuser

COPY . .
CMD ["python", "app.py"]
```

### Change Management
- Small, incremental changes — one resource type or concern per PR
- Blast radius assessment before apply
- Rollback plan documented for every production change
- Change windows for production (unless emergency)

## Critical Rules

1. **Never apply without plan review** — `terraform plan` output must be reviewed
2. **Never hardcode IPs, ARNs, or account IDs** — use variables and data sources
3. **Every resource needs tags** — enforced in CI
4. **Secrets in vault, never in code** — no credentials in Terraform, Docker, or scripts
5. **Small incremental changes** — one concern per PR, minimize blast radius
6. **No `:latest` tags** — pin all image and module versions explicitly
7. **State locking always on** — prevent concurrent modifications
8. **Least privilege always** — no `*` resources in production IAM policies
