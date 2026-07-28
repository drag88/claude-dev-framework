---
description: "Deep web research with adaptive planning and intelligent search"
---

# /cdf:research - Deep Research Command

## Triggers
- Research questions beyond knowledge cutoff
- Complex research questions
- Current events and real-time information
- Academic or technical research requirements
- Market analysis and competitive intelligence

## Context Trigger Pattern
```
/cdf:research "[query]" [--depth quick|standard|deep|exhaustive] [--strategy planning|intent|unified]
```

## Behavioral Flow

Scope the question, decide how many hops of research it needs, search in parallel batches, and synthesize with sources cited — deeper or more ambiguous questions warrant more hops.

## Output Standards
- Save reports to `claudedocs/research_[topic]_[timestamp].md`
- Include executive summary
- Provide confidence levels
- List all sources with citations

## Examples
```
/cdf:research "latest developments in quantum computing 2024"
/cdf:research "competitive analysis of AI coding assistants" --depth deep
/cdf:research "best practices for distributed systems" --strategy unified
```

## Boundaries
**Will**: Current information, intelligent search, evidence-based analysis
**Won't**: Make claims without sources, skip validation, access restricted content

## Agent Routing

| Research Context | Primary Agent | When to Use |
|-----------------|---------------|-------------|
| Technical topics | deep-research-agent | Architecture patterns, algorithms, best practices |
| Market/business | business-research-strategist | Market sizing, competitive analysis, business models |
| Library selection | library-researcher | Package comparison, maintenance health, migration risk |

## Next Commands
- `/cdf:design` — Design systems based on research findings
- `/cdf:brainstorm` — Explore requirements informed by research