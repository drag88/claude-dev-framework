# Command Index

Quick reference for all available `/cdf` commands, organized by purpose.

---

## Core Development (6)

| Command | Description | Complexity |
|---------|-------------|------------|
| [/cdf:implement](implement.md) | Feature and code implementation; delegates to `compound-engineering:ce-work` | standard |
| [/cdf:test](test.md) | Execute tests with coverage analysis and automated quality reporting | enhanced |
| [/cdf:tdd](tdd.md) | Test-Driven Development with RED-GREEN-REFACTOR workflow | advanced |
| [/cdf:git](git.md) | Git operations; commit operations delegate to `compound-engineering:ce-commit` | basic |
| [/cdf:improve](improve.md) | Apply systematic improvements to code quality, performance, and cleanup | standard |
| [/cdf:ship](ship.md) | Automated release pipeline; review and PR delivery delegate to compound-engineering skills | advanced |

---

## Analysis & Understanding (5)

| Command | Description | Complexity |
|---------|-------------|------------|
| [/cdf:analyze](analyze.md) | Comprehensive code analysis across quality, security, performance, architecture | standard |
| [/cdf:explain](explain.md) | Clear explanations of code, concepts, and system behavior | standard |
| [/cdf:research](research.md) | Deep web research with adaptive planning and intelligent search | advanced |
| [/cdf:troubleshoot](troubleshoot.md) | Diagnose and resolve issues; delegates to `compound-engineering:ce-debug` | standard |
| [/cdf:e2e](e2e.md) | End-to-end testing with Playwright patterns and Page Object Model | advanced |

---

## Planning & Design (4)

| Command | Description | Complexity |
|---------|-------------|------------|
| [/cdf:brainstorm](brainstorm.md) | Requirements discovery; delegates to `compound-engineering:ce-brainstorm` | advanced |
| [/cdf:design](design.md) | System architecture and planning; delegates to `compound-engineering:ce-plan` | standard |
| [/cdf:estimate](estimate.md) | Development estimates for tasks, features, or projects | standard |
| [/cdf:plan-review](plan-review.md) | Plan review gate; delegates to `compound-engineering:ce-doc-review` | advanced |

---

## Orchestration (2)

| Command | Description | Complexity |
|---------|-------------|------------|
| [/cdf:task](task.md) | Execute complex tasks with breakdown, delegation, and workflow management | advanced |
| [/cdf:approve](approve.md) | Persist a plan from plan mode and recommend execution strategy | standard |

`/cdf:flow` and `/cdf:workflow` were removed in the 4.7 leanness pass. Opus 4.7 plans multi-step workflows natively when given a clear prompt and `xhigh` effort — the orchestrator wrappers added scaffolding the model already does well.

---

## Utilities (4)

| Command | Description | Complexity |
|---------|-------------|------------|
| [/cdf:docs](docs.md) | Documentation management and generation; `plan` delegates to `compound-engineering:ce-plan` | standard |
| [/cdf:learn](learn.md) | Capture, view, and consolidate learned skill preferences | standard |
| [/cdf:rules](rules.md) | Generate and manage project-specific rules | standard |
| [/cdf:verify](verify.md) | Pre-PR quality gates; review stage delegates to `compound-engineering:ce-code-review` | enhanced |

---

## Quick Selection Guide

| If you want to... | Use this command |
|-------------------|------------------|
| Write new code | `/cdf:implement` |
| Run tests | `/cdf:test` |
| Test-first development | `/cdf:tdd` |
| Commit changes | `/cdf:git` |
| Ship a PR | `/cdf:ship` |
| Refactor or clean up code | `/cdf:improve` |
| Understand code quality | `/cdf:analyze` |
| Learn how something works | `/cdf:explain` |
| Research a topic | `/cdf:research` |
| Fix a bug | `/cdf:troubleshoot` |
| E2E testing with Playwright | `/cdf:e2e` |
| Explore an idea | `/cdf:brainstorm` |
| Design a system | `/cdf:design` |
| Estimate effort | `/cdf:estimate` |
| Challenge or harden a plan | `/cdf:plan-review` |
| Plan implementation or run full development workflow | `/cdf:task` (or write a clear prompt and let 4.7 plan) |
| Execute or break down a complex task | `/cdf:task` |
| Persist a plan from plan mode | `/cdf:approve` |
| Manage documentation | `/cdf:docs` |
| Manage learned skill preferences | `/cdf:learn` |
| Generate rules | `/cdf:rules` |
| Pre-PR quality check | `/cdf:verify` |

---

## Complexity Levels

| Level | Meaning |
|-------|---------|
| **low/basic** | Simple, direct execution |
| **standard** | Normal complexity, single-domain |
| **enhanced** | Additional features, may use MCP servers |
| **advanced** | Multi-step, may activate personas |
