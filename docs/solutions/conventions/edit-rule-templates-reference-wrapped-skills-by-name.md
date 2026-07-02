---
title: Edit rule templates, not generated rules — and reference wrapped plugins by skill name only
date: 2026-07-02
category: docs/solutions/conventions
module: routing/rules-generation
problem_type: convention
component: development_workflow
severity: medium
applies_when:
  - "Editing a file under `.claude/rules/` that has a matching source under `rules-templates/`"
  - "One plugin wraps or delegates to another plugin's skills or commands"
  - "Adding component counts (skills, commands, agents) to marketplace or plugin descriptions"
tags: [rules-generation, rule-templates, wrapper-plugin, drift-check, health-check, marketplace-metadata]
---

# Edit rule templates, not generated rules — and reference wrapped plugins by skill name only

## Context

While turning CDF into a "wrapper++" over the `compound-engineering` plugin (routing `brainstorm`, `design`, `implement`, `troubleshoot`, `plan-review`, `git commit`, and `ship` through `ce-*` skills instead of duplicating native flows), two related mistakes were easy to make: editing the wrong file when changing routing rules, and copying the wrapped plugin's internals instead of referencing them. A third, adjacent lesson from the same change surfaced a recurring maintenance cost: literal component-count strings in marketplace descriptions.

## Guidance

**1. Edit the template, not the generated file.** `.claude/rules/workflow.md` and its siblings are regenerated **verbatim** from sources in `rules-templates/` (e.g. `rules-templates/workflow-template.md`) by `/cdf:rules generate`. A routing change made only to `.claude/rules/workflow.md` looks correct until the next `/cdf:rules generate` run clobbers it back to the stale template content. The template is the durable source of truth; the generated file is a build artifact. When a routing or convention change needs to land in `.claude/rules/`, land it in the matching `rules-templates/*.md` first, then regenerate (or hand-align the generated file only as an interim step before the next regen, never as the final state).

**2. Reference a wrapped plugin's skills by public name only.** When CDF delegates to `compound-engineering:ce-work`, `compound-engineering:ce-plan`, etc., CDF's own files (commands, rules, CLAUDE.md) name the skill (`compound-engineering:ce-compound`) and stop there — they do not copy the wrapped skill's prose, its YAML schema, its enum values, or its phase logic into CDF. `docs/solutions/README.md` is a concrete example: it states the searchable frontmatter fields exist and says "Reference the CE schema by skill name rather than copying its enums into CDF" instead of inlining the schema.

This is what lets upstream updates flow through with zero drift — if `ce-compound`'s schema gains a field, CDF's reference is still accurate because it never had a stale copy to go out of date. A warn-only drift check, `check_ce_skill_refs()` in `scripts/health-check.py`, enforces the referencing half of this: it scans `commands/*.md` for `compound-engineering:ce-*` references and warns if the named skill directory no longer exists under the newest installed CE plugin version in `~/.claude/plugins/cache/compound-engineering-plugin/`.

**3. De-count marketplace/plugin descriptions.** Literal strings like "21 commands, 12 agents, 24 skills" in `.claude-plugin/marketplace.json` or `plugin.json` descriptions silently go stale the moment a component is added or removed elsewhere, and nothing forces a sync unless a count-consistency check exists. This repo was bitten by this three times across releases (1.11.0, 1.13.0, 2.0.0) before the fix: drop the numbers from prose descriptions entirely and let structural facts (directory contents, `commands/README.md`, `agents/README.md`) be the source of truth for counts.

## Why This Matters

Routing rules and conventions in this repo have two representations — the human-edited template and the machine-generated rule file — and only one of them survives a regen. Treating the generated file as editable is a trap that looks fine locally and fails silently later, usually discovered only when a "fixed" routing rule reappears after `/cdf:rules generate` runs again.

Copying a wrapped plugin's schema or prose creates the same class of silent-drift bug at a larger scope: CDF would carry a frozen snapshot of CE's contract that quietly diverges from the real one on every CE upgrade, with no mechanism to catch it. Referencing by skill name plus a warn-only existence check (`check_ce_skill_refs`) converts an invisible drift risk into a visible, catchable one — the check can't verify semantic compatibility, but it can catch the far more common failure mode of a renamed or removed skill.

Component counts in prose are a maintenance tax for the same underlying reason: a number written once, changed by a later commit elsewhere, with nothing wiring them together.

## When to Apply

- Before editing anything under `.claude/rules/`, check whether a matching file exists under `rules-templates/` (same base name, `*-template.md` suffix) — if so, edit that instead, or edit both and note the generated file is provisional until the next `/cdf:rules generate`.
- When adding or changing a delegation to another plugin's skill, write the reference as `<plugin>:<skill-name>` and nothing else. Do not inline the target skill's field lists, enums, or phase descriptions — link to the concept ("Reference the CE schema by skill name") instead.
- When writing marketplace or plugin metadata descriptions, avoid embedding a count of any component category; describe capabilities qualitatively instead.
- After changing a wrapped-plugin reference, run `python3 scripts/health-check.py` — it runs `check_ce_skill_refs()` (warn-only) as part of its checks and will flag stale `compound-engineering:ce-*` references against the currently installed CE plugin cache.

## Examples

Correct reference pattern (from `docs/solutions/README.md`):
```markdown
Documents in this directory are written by the compound-engineering plugin's
`compound-engineering:ce-compound` skill. CDF does not maintain a separate
solution template or frontmatter schema here.
...
Reference the CE schema by skill name rather than copying its enums into CDF.
```

Drift check that enforces the reference-only convention (`scripts/health-check.py`):
```python
def check_ce_skill_refs(project_root: Path) -> list:
    """Warn when delegated CE skill references in commands are stale."""
    ...
    ref_pattern = re.compile(r"compound-engineering:ce-[a-z0-9-]+")
    for command_file in sorted(commands_dir.glob("*.md")):
        content = command_file.read_text(errors="ignore")
        for ref in sorted(set(ref_pattern.findall(content))):
            skill_name = ref.removeprefix("compound-engineering:")
            if not (newest_skills_dir / skill_name).is_dir():
                messages.append(f"WARNING: {rel} has stale CE skill reference {ref} ...")
```

Template-first editing pattern: `rules-templates/workflow-template.md` carries the header `> Template for generating .claude/rules/workflow.md`, signaling that the generated file downstream is not the edit target.

## Related

- `docs/solutions/README.md` — states the skill-name-reference convention for `docs/solutions/` specifically
- `rules-templates/workflow-template.md` — source template for `.claude/rules/workflow.md`
- `scripts/health-check.py` — `check_ce_skill_refs()` drift check
- `.claude-plugin/marketplace.json`, `.claude-plugin/plugin.json` — de-counted descriptions
