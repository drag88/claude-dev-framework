---
name: starhub-presentations
description: Create executive presentations using StarHub's official templates and formatting standards. This skill should be used when building Board updates, CLT presentations, BPR decks, or any executive-level PowerPoint for StarHub. Includes the official CX Board template with proper slide layouts and styling.
---

# StarHub Executive Presentations

This skill creates professional presentations aligned with StarHub's corporate standards and executive communication patterns.

## When to Use This Skill

- Creating Board update presentations
- Building CLT (Corporate Leadership Team) decks
- Preparing BPR (Business Performance Review) slides
- Developing CX/NPS/Journey performance reports
- Creating strategic initiative proposals

## Template Asset

**Location**: `assets/starhub_cx_template.pptx`

This template contains StarHub's official slide layouts. Use it as the base for all executive presentations.

## Integration with PPTX Skill

This skill works together with the `pptx` skill for technical operations. Use:
- **pptx skill** for: thumbnail generation, text inventory extraction, slide rearrangement, text replacement
- **This skill** for: content guidelines, StarHub terminology, narrative templates, slide structure patterns

### Workflow for Creating StarHub Presentations

1. **Analyze template**: Use pptx skill's `thumbnail.py` to visualize layouts
   ```bash
   python skills/pptx/scripts/thumbnail.py assets/starhub_cx_template.pptx thumbnails --cols 4
   ```

2. **Extract inventory**: Use pptx skill's `inventory.py` for text positions
   ```bash
   python skills/pptx/scripts/inventory.py working.pptx text-inventory.json
   ```

3. **Rearrange slides**: Use pptx skill's `rearrange.py` for slide ordering
   ```bash
   python skills/pptx/scripts/rearrange.py assets/starhub_cx_template.pptx working.pptx 0,3,3,5,7
   ```

4. **Replace content**: Use pptx skill's `replace.py` with StarHub narratives
   ```bash
   python skills/pptx/scripts/replace.py working.pptx replacement.json output.pptx
   ```

## Slide Layout Reference

The template includes these official layouts:

### 1. Divider Page 1
**Purpose**: Major section separators
**Use for**: Opening new topics (e.g., "Customer Experience", "Network Experience")
**Content**: Single centered title, no body text
**Example**: "Customer Experience" divider between sections

### 2. 2_Front Cover 2
**Purpose**: Sub-section headers
**Use for**: Introducing specific topics within a section
**Content**: Clean section title
**Example**: "2025 Customer Experience Performance", "Customer Journey Dashboards"

### 3. Text Heavy Page
**Purpose**: Strategic overviews and frameworks
**Use for**:
- Multi-pillar strategies
- Process flows
- Framework presentations
- Approach + Actions + Status matrices
**Content structure**:
- Main title (insight headline)
- Multiple columns or sections
- Numbered elements (1, 2, 3, 4, 5)
- Status indicators

### 4. Title Slide
**Purpose**: Data-rich report slides
**Use for**:
- Journey performance reports
- KPI dashboards
- Metric summaries with tables
**Content structure**:
- Title with insight headline
- Key narrative paragraphs
- Data tables (metrics grid)
- Visual elements (journey steps, KPI cards)
- Slide number in corner

### 5. Heavy text page w/ bullets
**Purpose**: Detailed content with multiple sections
**Use for**:
- Program overviews (e.g., Platinum Experience)
- Initiative descriptions
- Detailed explanations with bullets
**Content structure**:
- Main title
- Multiple subsections with headers
- Bullet points under each section
- Call-out metrics (e.g., "2.2x", "3.1x")

## Presentation Structure Patterns

### Board Update Structure
```
1. Overview slide (Text Heavy Page)
   - Integrated approach summary
   - Strategic pillars
   - Status indicators

2. Section Divider (Divider Page 1)
   - "Customer Experience"

3. Sub-section Header (2_Front Cover 2)
   - "2025 Customer Experience Performance"

4. Performance Summary (Title Slide)
   - Key metrics narrative
   - Data table
   - Highlights

5. Repeat for each topic...

6. Strategy & Roadmap (Title Slide)
   - Timeline table
   - Milestones
   - Completion indicators
```

### Journey Report Structure
Each journey (Buy, Activate, Use, Get Help, Pay, Renew) follows:
```
- Journey name in title
- Performance narrative (2-3 sentences)
- KPI table with metrics
- Journey step visualization
- Top 3 Pain Points from VOC
- Experience dimensions (User Centricity, Delight, Consistency, Efficiency)
- Journey Owner attribution
```

## Content Writing Guidelines

### Title Slide Headlines
Transform descriptive to insight-driven:

| Avoid | Use |
|-------|-----|
| "NPS Performance" | "Over the past 6 quarters overall NPS has improved by 21%" |
| "Call Volume Trends" | "Total monthly call volumes are consistently trending down" |
| "Journey Status" | "The Buy, Activate and Renew journeys perform well above benchmarks" |

### Narrative Paragraphs
Each data slide should have 3-4 insight paragraphs:
1. **Trend statement** - What's happening (with specific numbers)
2. **Driver explanation** - Why it's happening
3. **Benchmark context** - How it compares
4. **Implication/Next step** - What it means

**Example**:
```
"Over the past 6 quarters overall NPS has improved by 21% and has
plateau-ed at 30pts. Early signs show a positive Customer Experience
for Supernova plans. This positive impact is expected to accelerate
with launch of new propositions and CX improvement initiatives."
```

### Metrics Presentation
Standard metrics table format:
- Rows: Time periods or categories
- Columns: Metric types
- Include trend indicators (↑ ↓)
- Add benchmark comparisons ("0.3 above benchmark")

### Status Indicators
Use consistent status language:
- "Operational, continuous improvement in-progress"
- "Planning and execution in-progress"
- "MVP launched 3 months early"
- "Completion"

## StarHub-Specific Elements

### Journey Framework
Six iconic journeys to reference:
1. **Buy** - Initial contact to purchase
2. **Activate** - Delivery, install, activation
3. **Use** - Product usage and engagement
4. **Get Help** - Support and issue resolution
5. **Pay** - Billing and payments
6. **Renew** - Retention and disconnection

### Experience Dimensions
Four standard CX pillars:
- **User Centricity** - Customer-focused design
- **Delight** - Exceeding expectations
- **Consistency** - Reliable experience
- **Efficiency** - Fast, easy processes

### Design Thinking Phases
Five-phase model for journey improvements:
1. **See** - Develop empathy, analyze data
2. **Think** - Problem definition, "How Might We"
3. **Act** - Prototype, experiment, pilot
4. **Review** - Capture feedback, benchmark
5. **Thank** - Celebrate wins, recognize excellence

### Program References
- **VOC** - Voice of Customer program
- **Supernova** - New mobile plan portfolio
- **Platinum** - Premium customer program
- **Home+** - Broadband product family
- **Fixify** - Service automation tool
- **COPs Service Agent** - AI service agent

## Creating Presentations

### Using the Template
1. Copy `assets/starhub_cx_template.pptx` to working directory
2. Use pptx skill's `thumbnail.py` to visualize available layouts
3. Identify which slide layouts match your content
4. Use pptx skill's `rearrange.py` to create working file with desired slides
5. Use pptx skill's `inventory.py` to extract text positions
6. Generate replacement content following this skill's guidelines
7. Use pptx skill's `replace.py` to apply content

### Slide Count Guidelines
- **Board Update**: 15-25 slides
- **BPR Section**: 5-10 slides
- **Initiative Proposal**: 8-12 slides

### Quality Checklist
Before finalizing:
- [ ] Insight headlines (not descriptive titles)
- [ ] Specific numbers in narratives
- [ ] Benchmark comparisons where applicable
- [ ] Status indicators on roadmap items
- [ ] Journey owners attributed
- [ ] Slide numbers present
- [ ] Consistent terminology

## Slide Title Formulas

### Performance Summary Titles
```
"[Metric] has [improved/declined] by [X]% over [time period]"
"[Area] is performing [above/below] industry benchmarks"
"[Initiative] showing positive early signs with [specific result]"
```

### Journey Report Titles
```
"[Journey] Journey Performance Report"
"The [Journey] journey has seen [trend description] across [period]"
"[Journey] journey is [status] - [key insight]"
```

### Strategic Titles
```
"[Year] [Area] strategy and roadmap"
"Uplifting [Area] - Overall approach"
"[Program] Customer Experience and performance"
```

## Narrative Paragraph Templates

### Performance Narrative
```
Over the past [X] quarters, [metric] has [improved/declined] by [Y]%
and has [stabilized/continued trending] at [value]. [Driver explanation].
This [positive/negative] impact is expected to [accelerate/continue]
with [upcoming initiative].
```

### Journey Performance Narrative
```
The [journey name] journey is seeing its [best/worst] quarter in [Q#].
[Primary metric] is at [status], [secondary metric] is [trend].
A key driver [is/are] [root cause]. [Recommendation or next step].
```

### Benchmark Narrative
```
The [area] journeys [perform/are performing] [well above/at/below]
industry benchmarks. [Specific journey] shows [X] above benchmark,
while [other journey] requires attention at [Y] below benchmark.
```

## Data Table Structures

### Quarterly Performance Table
| Metric | Q1 | Q2 | Q3 | Q4 | Trend |
|--------|----|----|----|----|-------|
| NPS | 28 | 29 | 30 | 30 | → |
| CSAT | 4.2 | 4.3 | 4.5 | 4.6 | ↑ |
| Call Vol | 52K | 48K | 45K | 42K | ↓ |

### Journey Metrics Table
| Journey | CSAT | Benchmark | Gap | Call Vol | % of Total |
|---------|------|-----------|-----|----------|------------|
| Buy | 4.57 | 4.27 | +0.3 | 3,752 | 8.02% |
| Activate | 4.77 | 4.37 | +0.4 | 4,528 | 8.90% |
| Use | 6.45 NPS | 5.95 | +0.5 | 16,258 | 27.24% |

### Roadmap Table
| Initiative | Jan | Feb | Mar | Q2 | Q3 | Q4 | Status |
|------------|-----|-----|-----|----|----|----|----|
| VOC Enhancement | ███ | ███ | ✓ | | | | Complete |
| Journey Ops | ███ | ███ | ███ | ███ | ✓ | | In Progress |
| App Redesign | | | ███ | ███ | ███ | ███ | Planning |

## Call-Out Metrics

### Format
```
[Large Number]x
[Description text below]
```

### Examples
```
2.2x
Cross-sell among platinum customers

3.1x
Lower churn among platinum customers

21%
NPS improvement over 6 quarters

95
Issues being resolved through Design Thinking
```

## Section Headers

### Major Sections (Divider Page)
- Customer Experience
- Network Experience
- Product Performance
- Strategic Initiatives
- Financial Impact

### Sub-Sections (Front Cover 2)
- 2025 Customer Experience Performance
- Customer Journeys Implementation
- Customer Journey Dashboards
- Customer Experience Strategy & Roadmap
- Platinum Experience

## Status Language

### Progress Indicators
- "In-progress" - Active work
- "Planning and execution in-progress" - Early stage
- "Operational, continuous improvement in-progress" - BAU
- "Completion" - Done
- "MVP launched [X] months early" - Ahead of schedule
- "Phase 2" - Next stage indicator

### Performance Descriptors
- "Performing well above industry benchmarks"
- "Seeing its best quarter in Q4"
- "At an all-time high"
- "Consistently trending down" (for call volumes - positive)
- "Steadily improving"
- "Has plateau-ed at [value]"

## Voice of Customer References

### Pain Point Format
```
TOP 3 PAIN-POINTS FROM VOICE OF CUSTOMER
1. [Issue category]: [Brief description]
2. [Issue category]: [Brief description]
3. [Issue category]: [Brief description]
```

### Issue Tracking Format
```
Issues tracked: [#]
Call vol. - [Month]: [#,###]
```

## Journey Owner Attribution

Always include at bottom of journey slides:
```
Journey Owner: [Full Name]
```

Examples from template:
- Journey Owner: Wayne Poh (Buy)
- Journey Owner: NAGALINGAM Yogamala (Activate)
- Journey Owner: Roy Looi (Get Help)
- Journey Owner: Claire Stern (Pay)
- Journey Owner: Natasha Tan (Renew)

## Program-Specific Content

### Platinum Program Elements
- Dedicated Platinum hotline
- Platinum Lounge at Paragon
- Platinum priority queue
- Platinum Hub Trooper service
- Platinum Broadband Installations

### Supernova Plan Elements
- Supernova Elite plans
- Platinum eligibility
- Industry leading benefits
- New propositions

### VOC Program Elements
- Voice of Customer forum
- VOC AI model
- Closed Loop Automation
- Customer issue tracking
- Verbatim analysis

## Cross-Reference

- For PPTX technical operations (thumbnails, inventory, rearrange, replace), use the `pptx` skill
- For email communications to executives, use `starhub-exec-comms` skill
- For churn/analytics narratives within slides, use `churn-insights-writer` skill
- For model performance summaries, use `model-dashboard-narrator` skill
