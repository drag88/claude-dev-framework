# Solutions Directory

Durable repo knowledge captured from solved, non-obvious problems.

## Ownership

Documents in this directory are written by the compound-engineering plugin's `compound-engineering:ce-compound` skill. CDF does not maintain a separate solution template or frontmatter schema here.

During reviews, `compound-engineering:ce-learnings-researcher` reads these documents to surface relevant prior learnings.

## Schema

Solution documents follow the `ce-compound` schema. The searchable frontmatter fields include `module`, `date`, `problem_type`, `component`, and `tags`; `category` is mapped from `problem_type`.

Reference the CE schema by skill name rather than copying its enums into CDF.

## Searching Solutions

```bash
# By error or symptom text
grep -r "TokenExpiredError" docs/solutions/

# By tag
grep -l "tags:.*oauth" docs/solutions/**/*.md

# By problem type
grep -l "problem_type:" docs/solutions/**/*.md

# By component
grep -l "component:.*auth" docs/solutions/**/*.md
```

## Creating Solutions

Run `compound-engineering:ce-compound` after solving a non-obvious problem whose diagnosis, fix, or prevention path should be reused.

Do not create solution documents manually unless you are repairing output from the CE skill.
