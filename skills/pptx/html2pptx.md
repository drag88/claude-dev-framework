# HTML to PowerPoint Conversion Guide

This document describes how to convert HTML slides to PowerPoint presentations using the html2pptx workflow.

## Overview

The html2pptx workflow allows you to:
1. Design slides using HTML/CSS (familiar web technologies)
2. Render them with Playwright for pixel-perfect positioning
3. Convert to PowerPoint with accurate layout preservation

## Slide Dimensions

Standard slide dimensions for 16:9 aspect ratio:
- **Width**: 720pt (10 inches)
- **Height**: 405pt (5.625 inches)

For 4:3 aspect ratio:
- **Width**: 720pt (10 inches)
- **Height**: 540pt (7.5 inches)

## HTML Structure

### Basic Slide Template

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      width: 720pt;
      height: 405pt;
      font-family: Arial, sans-serif;
      background: #FFFFFF;
    }
    .slide {
      width: 100%;
      height: 100%;
      padding: 40pt;
      display: flex;
      flex-direction: column;
    }
  </style>
</head>
<body>
  <div class="slide">
    <h1>Slide Title</h1>
    <p>Content goes here</p>
  </div>
</body>
</html>
```

## Text Elements

### Supported Elements
- `<h1>` through `<h6>` - Headings
- `<p>` - Paragraphs
- `<ul>`, `<ol>` - Lists
- `<li>` - List items
- `<span>` - Inline text styling

### Typography Guidelines

**Web-safe fonts only:**
- Arial, Helvetica (sans-serif)
- Times New Roman, Georgia (serif)
- Courier New (monospace)
- Verdana, Tahoma, Trebuchet MS
- Impact (display)

**Font size recommendations:**
- Titles: 36-48pt
- Subtitles: 24-32pt
- Body text: 14-18pt
- Captions: 10-12pt

## Layout Patterns

### Two-Column Layout

```html
<div class="slide">
  <h1>Title</h1>
  <div style="display: flex; flex: 1; gap: 30pt;">
    <div style="flex: 0.4;">
      <p>Left column content (40%)</p>
      <ul>
        <li>Point 1</li>
        <li>Point 2</li>
      </ul>
    </div>
    <div style="flex: 0.6;">
      <div class="placeholder" style="width: 100%; height: 100%; background: #ccc;">
        Chart/Table area (60%)
      </div>
    </div>
  </div>
</div>
```

### Full-Width Header with Content

```html
<div class="slide">
  <div style="background: #1C2833; color: white; padding: 20pt; margin: -40pt -40pt 30pt -40pt;">
    <h1>Section Title</h1>
  </div>
  <div style="flex: 1;">
    <p>Main content area</p>
  </div>
</div>
```

### Grid Layout (2x2)

```html
<div class="slide">
  <h1>Title</h1>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20pt; flex: 1;">
    <div class="card">Item 1</div>
    <div class="card">Item 2</div>
    <div class="card">Item 3</div>
    <div class="card">Item 4</div>
  </div>
</div>
```

## Placeholder Areas

Use `class="placeholder"` to mark areas for charts, tables, or images that will be added programmatically:

```html
<div class="placeholder"
     data-type="chart"
     data-chart-type="bar"
     style="width: 400pt; height: 250pt; background: #eee;">
  Chart placeholder
</div>
```

## Critical Formatting Rules

### DO:
- Use `pt` units for all dimensions (not px, em, or rem)
- Set explicit widths and heights on containers
- Use flexbox for layouts
- Include all styles inline or in `<style>` tags
- Test renders before conversion

### DON'T:
- Use external stylesheets (won't be loaded)
- Use CSS gradients directly (rasterize as PNG first)
- Use web fonts (stick to system fonts)
- Use SVG icons directly (rasterize as PNG first)
- Use viewport units (vw, vh)

## Rasterizing Graphics

### Gradients
Gradients must be rasterized to PNG before use:

```javascript
const sharp = require('sharp');

// Create gradient as SVG, then rasterize
const gradientSvg = `
<svg width="720" height="100">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#1C2833"/>
      <stop offset="100%" style="stop-color:#2E4053"/>
    </linearGradient>
  </defs>
  <rect width="720" height="100" fill="url(#grad)"/>
</svg>`;

await sharp(Buffer.from(gradientSvg))
  .png()
  .toFile('gradient-header.png');
```

### Icons
Rasterize SVG icons to PNG:

```javascript
const sharp = require('sharp');

// Icon SVG content
const iconSvg = `<svg>...</svg>`;

await sharp(Buffer.from(iconSvg))
  .resize(48, 48)
  .png()
  .toFile('icon.png');
```

Then reference in HTML:
```html
<img src="gradient-header.png" style="width: 720pt; height: 100pt;">
<img src="icon.png" style="width: 48pt; height: 48pt;">
```

## Using html2pptx.js

### Basic Usage

```javascript
const { html2pptx } = require('./html2pptx.js');
const PptxGenJS = require('pptxgenjs');

async function createPresentation() {
  const pptx = new PptxGenJS();

  // Process each HTML file
  await html2pptx(pptx, 'slide1.html');
  await html2pptx(pptx, 'slide2.html');
  await html2pptx(pptx, 'slide3.html');

  // Add charts/tables to placeholder areas
  // ... (using PptxGenJS API)

  // Save presentation
  await pptx.writeFile('output.pptx');
}

createPresentation();
```

### Adding Charts After Conversion

```javascript
// After html2pptx processing, add chart to slide
const slide = pptx.getSlide(1);

slide.addChart(pptx.ChartType.bar, [
  { name: 'Series 1', values: [10, 20, 30, 40] }
], {
  x: 4.0,  // Position matching placeholder
  y: 1.5,
  w: 5.5,
  h: 3.5,
  showLegend: false,
  showTitle: false
});
```

### Adding Tables

```javascript
slide.addTable([
  ['Header 1', 'Header 2', 'Header 3'],
  ['Data 1', 'Data 2', 'Data 3'],
  ['Data 4', 'Data 5', 'Data 6']
], {
  x: 0.5,
  y: 2.0,
  w: 9.0,
  fontSize: 12,
  border: { pt: 1, color: 'CCCCCC' }
});
```

## Validation Workflow

After generating the presentation:

1. **Create thumbnails**:
   ```bash
   python scripts/thumbnail.py output.pptx thumbnails --cols 4
   ```

2. **Review for issues**:
   - Text cutoff by shapes or edges
   - Overlapping elements
   - Positioning errors
   - Color contrast problems

3. **Fix and regenerate** if needed

## Common Issues and Solutions

### Text Cutoff
- Increase container padding
- Reduce font size
- Check overflow settings

### Positioning Errors
- Use explicit `pt` units
- Avoid percentage-based positioning for critical elements
- Test at exact slide dimensions

### Font Rendering
- Stick to web-safe fonts
- Avoid font weights other than normal/bold
- Don't use font-stretch or font-variant

### Image Quality
- Export PNG at 2x resolution for crisp rendering
- Use appropriate compression
- Verify image dimensions match HTML specifications
