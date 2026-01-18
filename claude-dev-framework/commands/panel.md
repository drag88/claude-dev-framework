---
name: panel
description: |
  Multi-expert panel discussions for business strategy and software specification analysis.
  Use when you need expert perspectives on business decisions, specifications, or technical designs.
category: analysis
complexity: enhanced
mcp-servers:
  - sequential
  - context7
personas:
  - technical-writer
  - system-architect
  - quality-engineer
---

# /cdf:panel - Expert Panel Analysis System

> Multi-expert panel discussions with renowned business and software engineering thought leaders.

## Quick Start

```bash
# Business strategy analysis
/cdf:panel [document] --type business

# Specification review
/cdf:panel [document] --type spec

# Select specific experts
/cdf:panel [document] --type business --experts "porter,christensen"

# Socratic learning mode
/cdf:panel [document] --type spec --mode socratic
```

## When to Use

Use `/cdf:panel` when:
- Analyzing business strategy or market positioning
- Reviewing specifications for quality and completeness
- Getting expert perspectives on technical designs
- Learning through expert questioning and dialogue

**Don't use this command for**: Simple code analysis (use `/cdf:analyze`), implementation tasks (use `/cdf:implement`).

## Panel Types

### Business Panel (`--type business`)

AI-facilitated panel discussion between renowned business thought leaders analyzing documents through their distinct frameworks.

**Available Experts:**
| Expert | Domain | Methodology |
|--------|--------|-------------|
| **Clayton Christensen** | Disruption Theory | Jobs-to-be-Done, Innovation Patterns |
| **Michael Porter** | Competitive Strategy | Five Forces, Value Chain |
| **Peter Drucker** | Management Philosophy | MBO, Knowledge Work |
| **Seth Godin** | Marketing Innovation | Tribe Building, Permission Marketing |
| **W. Chan Kim & Renée Mauborgne** | Blue Ocean Strategy | Value Innovation |
| **Jim Collins** | Organizational Excellence | Good to Great, Flywheel |
| **Nassim Nicholas Taleb** | Risk Management | Antifragility, Black Swan |
| **Donella Meadows** | Systems Thinking | Leverage Points, Feedback Loops |
| **Jean-luc Doumont** | Communication | Structured Clarity |

### Specification Panel (`--type spec`)

Multi-expert specification review and improvement using renowned software engineering experts.

**Available Experts:**
| Expert | Domain | Focus |
|--------|--------|-------|
| **Karl Wiegers** | Requirements Engineering | SMART criteria, Testability |
| **Gojko Adzic** | Specification by Example | Given/When/Then, Living Docs |
| **Alistair Cockburn** | Use Cases | Goal-oriented Analysis |
| **Martin Fowler** | Software Architecture | Interface Design, Patterns |
| **Michael Nygard** | Production Systems | Failure Modes, Reliability |
| **Sam Newman** | Microservices | Service Boundaries, API Evolution |
| **Gregor Hohpe** | Enterprise Integration | Messaging Patterns |
| **Lisa Crispin** | Agile Testing | Test Strategy, Quality |
| **Janet Gregory** | Testing Advocate | Specification Workshops |
| **Kelsey Hightower** | Cloud Native | Kubernetes, Infrastructure |

## Usage

```bash
/cdf:panel [content|@file] [--type business|spec] [--mode discussion|debate|critique|socratic] [--experts "name1,name2"] [--focus area] [--iterations N] [--format standard|structured|detailed]
```

## Analysis Modes

### Discussion Mode (Default)
Collaborative analysis where experts build upon each other's insights.

```
KARL WIEGERS: "The requirement 'SHALL handle failures gracefully' lacks specificity."

MICHAEL NYGARD: "Building on Karl's point, we need specific failure modes:
network timeouts, service unavailable, rate limiting."

GOJKO ADZIC: "Let's make this concrete with examples:
  Given: Service timeout after 30 seconds
  When: Circuit breaker activates
  Then: Return cached response within 100ms"
```

### Debate Mode (Business only)
Adversarial analysis for controversial topics or when experts disagree.

### Critique Mode
Systematic review with specific improvement suggestions and priority rankings.

```
=== REQUIREMENTS ANALYSIS ===

KARL WIEGERS - Requirements Quality Assessment:
❌ CRITICAL: Requirement R-001 lacks measurable acceptance criteria
📝 RECOMMENDATION: Replace "handle failures gracefully" with specific metrics
🎯 PRIORITY: High - Affects testability and validation
📊 QUALITY IMPACT: +40% testability, +60% clarity
```

### Socratic Mode
Question-driven exploration for deep learning and strategic thinking.

```
ALISTAIR COCKBURN: "What is the fundamental problem this specification is trying to solve?"
KARL WIEGERS: "Who are the primary stakeholders affected by these requirements?"
MICHAEL NYGARD: "What assumptions are you making about the deployment environment?"
```

## Focus Areas

### Business Focus Areas
- `--focus competitive-analysis` - Market positioning, Five Forces
- `--focus innovation` - Disruption, Blue Ocean Strategy
- `--focus risk` - Antifragility, Black Swan events
- `--focus systems` - Leverage points, Feedback loops

### Specification Focus Areas
- `--focus requirements` - Clarity, completeness, testability
- `--focus architecture` - Interface design, system boundaries
- `--focus testing` - Test strategy, quality attributes
- `--focus compliance` - Regulatory, security, operational

## MCP Integration

- **Sequential MCP**: Expert panel coordination, structured analysis
- **Context7 MCP**: Specification patterns, industry best practices
- **Persona Activation**: Technical Writer, System Architect, Quality Engineer

## Examples

### Business Strategy Review
```bash
# Analyze competitive positioning
/cdf:panel @business_plan.md --type business --experts "porter,christensen" --focus competitive-analysis

# Blue ocean strategy exploration
/cdf:panel "Our product idea..." --type business --mode debate --experts "kim,godin"
```

### Specification Review
```bash
# API specification critique
/cdf:panel @auth_api.spec.yml --type spec --mode critique --focus requirements,architecture

# Requirements workshop
/cdf:panel "user story content" --type spec --mode discussion --experts "wiegers,adzic,cockburn"

# Iterative improvement
/cdf:panel @complex_system.spec.yml --type spec --iterations 3 --format detailed
```

### Learning Mode
```bash
# Learn through expert questions
/cdf:panel @my_first_spec.yml --type spec --mode socratic

# Business thinking development
/cdf:panel @startup_pitch.md --type business --mode socratic --experts "drucker,meadows"
```

## Output Formats

### Standard Format
```yaml
panel_review:
  type: "spec"
  experts: ["wiegers", "adzic", "fowler"]
  mode: "critique"

quality_assessment:
  overall_score: 7.2/10
  requirements_quality: 8.1/10
  architecture_clarity: 6.8/10

critical_issues:
  - category: "requirements"
    severity: "high"
    expert: "wiegers"
    issue: "Authentication timeout not specified"
    recommendation: "Define session timeout with configurable values"

expert_consensus:
  - "Specification needs concrete failure handling definitions"
  - "Missing operational monitoring requirements"
```

### Structured Format
Token-efficient format using symbol system for concise communication.

### Detailed Format
Comprehensive analysis with full expert commentary and implementation guidance.

## Quality Metrics (Spec Panel)

- **Clarity Score**: Language precision and understandability (0-10)
- **Completeness Score**: Coverage of essential elements (0-10)
- **Testability Score**: Measurability and validation capability (0-10)
- **Consistency Score**: Internal coherence and contradiction detection (0-10)

## Boundaries

**Will:**
- Provide expert-level analysis through distinct frameworks and methodologies
- Generate specific, actionable recommendations with priority rankings
- Support multiple analysis modes for different use cases
- Enable learning through expert dialogue and questioning

**Will Not:**
- Replace human judgment in critical business or technical decisions
- Modify documents without explicit user consent
- Generate content from scratch without existing context
- Provide legal or regulatory compliance guarantees

## Related Commands

- `/cdf:analyze` - Code analysis (quality, security, performance)
- `/cdf:design` - System and component design
- `/cdf:brainstorm` - Requirements discovery and ideation
