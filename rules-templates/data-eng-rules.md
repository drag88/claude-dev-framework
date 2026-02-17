# Data Engineering Rules Template

> Template for generating rules in Data Engineering / ETL / dbt projects.

## Architecture Additions

### Data Lineage
```
Sources → Staging → Intermediate → Marts → Dashboards/APIs
  ↓          ↓           ↓            ↓          ↓
[raw DB]  [stg_*]    [int_*]      [fct_/dim_]  [BI tool]
```

### Pipeline DAG Structure
- [Airflow / Dagster / Prefect / dbt — detect from project]
- DAGs organized by domain: `[domain]_[frequency]_[action]`
- Task dependencies are explicit — no implicit ordering
- Sensors/triggers for event-driven pipelines

## Pipeline Conventions (`pipeline-conventions.md`)

### DAG/Job Naming
- DAG: `[domain]_[frequency]_[action]` (e.g., `sales_daily_load`, `users_hourly_sync`)
- Task: `[action]_[target]` (e.g., `extract_orders`, `transform_revenue`, `load_dim_customer`)
- dbt model: `[layer]_[source]__[entity]` (e.g., `stg_stripe__payments`, `fct_orders`)

### Dependency Rules
- Tasks declare explicit upstream dependencies
- No circular dependencies — DAG must be acyclic
- Cross-DAG dependencies use sensors or event triggers, not direct references
- Shared resources (connections, pools) are configured centrally

### Scheduling
- Idempotent tasks — safe to re-run for any date range
- Backfill-friendly — parameterized by execution date
- SLAs defined for critical pipelines
- Alerting on task failure and SLA breach

## Data Quality (`data-quality.md`)

### Testing Requirements
Every model/table must have:
- **Unique key test** — primary key is unique and not null
- **Not-null tests** on required columns
- **Accepted values** for categorical/enum columns
- **Referential integrity** — foreign keys point to existing records
- **Freshness checks** — source data is not stale

### Schema Enforcement
- Schema defined in [YAML / JSON Schema / Great Expectations suite]
- Schema validation runs before downstream processing
- Schema changes require migration plan and downstream impact review

### Null Handling
- Document expected null behavior for every column
- Use `COALESCE` with explicit defaults, not silent null propagation
- Null in a non-nullable column fails the pipeline (not silently ignored)

## Patterns

### Layered Model Architecture (dbt-style)
| Layer | Prefix | Purpose | Rules |
|-------|--------|---------|-------|
| Staging | `stg_` | 1:1 with source, rename + type cast | No joins, no aggregations |
| Intermediate | `int_` | Business logic, joins, filtering | Reusable building blocks |
| Marts | `fct_` / `dim_` | Final business entities | One grain per model, documented |

### SQL Style
- Explicit column lists — never `SELECT *`
- CTEs over subqueries for readability
- Meaningful aliases (`orders AS o` is fine, `t1` is not)
- One CTE per logical step, named descriptively
- Leading commas for easy column addition/removal
- Lowercase SQL keywords (or uppercase — detect from existing code)

### Incremental Patterns
```sql
-- Incremental load pattern
{% if is_incremental() %}
  WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}
```
- Incremental models define merge key and strategy (append / merge / delete+insert)
- Full refresh scheduled periodically as safety net

### Idempotency
- Every task produces the same result for the same input date
- Use `MERGE` or `DELETE + INSERT` for reprocessable loads
- No `INSERT` without deduplication logic
- Partition-based overwrites for large tables

## Critical Rules

1. **Never use `SELECT *`** — explicit columns prevent silent schema drift
2. **Every model needs tests** — unique key + not-null at minimum
3. **Tasks must be idempotent** — safe to re-run without duplicating data
4. **Source freshness checks** — alert when source data is stale
5. **No hardcoded dates or values** — parameterize everything
6. **Document grain** — every mart model states its grain explicitly
7. **Review downstream impact** before changing any shared model
8. **Credentials in secrets manager** — never in DAG code or config files
