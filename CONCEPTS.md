# Concepts

Shared domain vocabulary for this project — entities, named processes, and status concepts with project-specific meaning. Seeded with core domain vocabulary, then accretes as ce-compound and ce-compound-refresh process learnings; direct edits are fine. Glossary only, not a spec or catch-all.

## Rules Generation

### Rule Template
The human-edited source of truth for a project rule document. A Rule Template lives separately from the rule files it produces and is the only place routing and convention changes should be made for rules that get regenerated.

### Generated Rule
A project rule document produced verbatim from a Rule Template by the rules-generation process. Treated as a build artifact, not an edit target — a direct edit to a Generated Rule is overwritten the next time generation runs, unless the matching Rule Template is updated too.

## Wrapper Plugin

### Wrapped Plugin
A plugin whose skills another plugin (the wrapper) delegates work to instead of reimplementing equivalent behavior natively. A wrapper references a Wrapped Plugin's skills by public skill name only — it does not copy the wrapped skill's schema, prose, or internal logic, so the wrapped plugin can evolve without the wrapper going stale.

### Skill Reference
A pointer from the wrapper's own files (commands, rules, project instructions) to a specific skill in a Wrapped Plugin, written as `<plugin-name>:<skill-name>` and nothing else. A Skill Reference is the unit a Drift Check validates.

### Drift Check
An automated, warn-only validation that a Skill Reference still resolves to an existing skill in the currently installed version of the Wrapped Plugin. A Drift Check confirms the reference target still exists; it does not verify that the wrapped skill's behavior or contract is still compatible.

## Flagged ambiguities

- Component counts (skill/command/agent totals) embedded as literal numbers in marketplace or plugin description text are a known recurring source of drift — they go stale independently of the components they describe. The resolved convention is to state capabilities qualitatively in descriptions and let directory contents be the source of truth for counts, not to maintain a synced number in prose.
