/**
 * html2pptx.js - Convert HTML slides to PowerPoint
 *
 * Usage:
 *   const { html2pptx } = require('./html2pptx.js');
 *   const PptxGenJS = require('pptxgenjs');
 *
 *   const pptx = new PptxGenJS();
 *   await html2pptx(pptx, 'slide.html');
 *   await pptx.writeFile('output.pptx');
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Constants for conversion
const PT_TO_INCH = 1 / 72;
const DEFAULT_SLIDE_WIDTH = 10;  // inches (720pt)
const DEFAULT_SLIDE_HEIGHT = 5.625;  // inches (405pt for 16:9)

/**
 * Convert HTML file to PowerPoint slide
 * @param {PptxGenJS} pptx - PptxGenJS instance
 * @param {string} htmlPath - Path to HTML file
 * @param {object} options - Optional settings
 * @returns {object} Slide object and placeholder info
 */
async function html2pptx(pptx, htmlPath, options = {}) {
  const {
    slideWidth = DEFAULT_SLIDE_WIDTH,
    slideHeight = DEFAULT_SLIDE_HEIGHT,
  } = options;

  // Read HTML content
  const htmlContent = fs.readFileSync(htmlPath, 'utf-8');

  // Launch browser
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  // Set viewport to slide dimensions (in pixels at 96 DPI)
  const viewportWidth = Math.round(slideWidth * 96);
  const viewportHeight = Math.round(slideHeight * 96);
  await page.setViewportSize({ width: viewportWidth, height: viewportHeight });

  // Load HTML
  const htmlDir = path.dirname(path.resolve(htmlPath));
  await page.setContent(htmlContent, {
    baseURL: `file://${htmlDir}/`,
    waitUntil: 'networkidle'
  });

  // Extract elements from HTML
  const elements = await page.evaluate(() => {
    const results = [];

    // Process text elements
    const textSelectors = 'h1, h2, h3, h4, h5, h6, p, li, span';
    document.querySelectorAll(textSelectors).forEach((el, idx) => {
      const rect = el.getBoundingClientRect();
      const style = window.getComputedStyle(el);

      // Skip if no visible text or zero dimensions
      if (!el.textContent.trim() || rect.width === 0 || rect.height === 0) return;

      // Skip if parent is also a text element (avoid duplicates)
      if (el.parentElement && el.parentElement.matches(textSelectors)) return;

      results.push({
        type: 'text',
        text: el.textContent.trim(),
        tagName: el.tagName.toLowerCase(),
        x: rect.left,
        y: rect.top,
        w: rect.width,
        h: rect.height,
        fontSize: parseFloat(style.fontSize),
        fontFamily: style.fontFamily.split(',')[0].replace(/['"]/g, '').trim(),
        fontWeight: style.fontWeight,
        fontStyle: style.fontStyle,
        color: style.color,
        textAlign: style.textAlign,
        backgroundColor: style.backgroundColor
      });
    });

    // Process images
    document.querySelectorAll('img').forEach((el, idx) => {
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;

      results.push({
        type: 'image',
        src: el.src,
        x: rect.left,
        y: rect.top,
        w: rect.width,
        h: rect.height
      });
    });

    // Process placeholder divs
    document.querySelectorAll('.placeholder').forEach((el, idx) => {
      const rect = el.getBoundingClientRect();
      results.push({
        type: 'placeholder',
        dataType: el.dataset.type || 'generic',
        chartType: el.dataset.chartType,
        x: rect.left,
        y: rect.top,
        w: rect.width,
        h: rect.height
      });
    });

    // Process background shapes (divs with background color)
    document.querySelectorAll('div').forEach((el) => {
      const style = window.getComputedStyle(el);
      const bg = style.backgroundColor;

      // Skip transparent or placeholder elements
      if (bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent') return;
      if (el.classList.contains('placeholder')) return;
      if (el.classList.contains('slide')) return;

      const rect = el.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;

      results.push({
        type: 'shape',
        shapeType: 'rect',
        x: rect.left,
        y: rect.top,
        w: rect.width,
        h: rect.height,
        fill: bg
      });
    });

    return results;
  });

  // Take screenshot for reference
  const screenshotPath = htmlPath.replace('.html', '-preview.png');
  await page.screenshot({ path: screenshotPath, fullPage: false });

  await browser.close();

  // Create slide
  const slide = pptx.addSlide();

  // Scaling factor (pixels to inches)
  const scale = slideWidth / viewportWidth;

  // Track placeholders for later
  const placeholders = [];

  // Sort elements by z-index (shapes first, then text)
  const shapes = elements.filter(e => e.type === 'shape');
  const texts = elements.filter(e => e.type === 'text');
  const images = elements.filter(e => e.type === 'image');
  const placeholderElements = elements.filter(e => e.type === 'placeholder');

  // Add shapes (backgrounds)
  shapes.forEach(el => {
    const fill = rgbToHex(el.fill);
    if (fill) {
      slide.addShape(pptx.ShapeType.rect, {
        x: el.x * scale,
        y: el.y * scale,
        w: el.w * scale,
        h: el.h * scale,
        fill: { color: fill }
      });
    }
  });

  // Add images
  for (const el of images) {
    try {
      // Handle local file paths
      let imgPath = el.src;
      if (imgPath.startsWith('file://')) {
        imgPath = imgPath.replace('file://', '');
      }

      if (fs.existsSync(imgPath)) {
        const imgData = fs.readFileSync(imgPath);
        const base64 = imgData.toString('base64');
        const ext = path.extname(imgPath).toLowerCase().replace('.', '');

        slide.addImage({
          data: `image/${ext};base64,${base64}`,
          x: el.x * scale,
          y: el.y * scale,
          w: el.w * scale,
          h: el.h * scale
        });
      }
    } catch (err) {
      console.warn(`Warning: Could not add image ${el.src}: ${err.message}`);
    }
  }

  // Add text elements
  texts.forEach(el => {
    const textOpts = {
      x: el.x * scale,
      y: el.y * scale,
      w: el.w * scale,
      h: el.h * scale,
      fontSize: el.fontSize * 0.75, // px to pt conversion
      fontFace: mapFont(el.fontFamily),
      color: rgbToHex(el.color) || '000000',
      bold: el.fontWeight === 'bold' || parseInt(el.fontWeight) >= 700,
      italic: el.fontStyle === 'italic',
      align: mapAlign(el.textAlign),
      valign: 'top'
    };

    slide.addText(el.text, textOpts);
  });

  // Record placeholder positions
  placeholderElements.forEach(el => {
    placeholders.push({
      type: el.dataType,
      chartType: el.chartType,
      x: el.x * scale,
      y: el.y * scale,
      w: el.w * scale,
      h: el.h * scale
    });
  });

  return { slide, placeholders, screenshotPath };
}

/**
 * Convert RGB color string to hex
 */
function rgbToHex(rgb) {
  if (!rgb || rgb === 'transparent' || rgb === 'rgba(0, 0, 0, 0)') return null;

  const match = rgb.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!match) return null;

  const r = parseInt(match[1]).toString(16).padStart(2, '0');
  const g = parseInt(match[2]).toString(16).padStart(2, '0');
  const b = parseInt(match[3]).toString(16).padStart(2, '0');

  return `${r}${g}${b}`.toUpperCase();
}

/**
 * Map CSS font family to PowerPoint-safe font
 */
function mapFont(fontFamily) {
  const font = fontFamily.toLowerCase();

  if (font.includes('arial')) return 'Arial';
  if (font.includes('helvetica')) return 'Helvetica';
  if (font.includes('times')) return 'Times New Roman';
  if (font.includes('georgia')) return 'Georgia';
  if (font.includes('courier')) return 'Courier New';
  if (font.includes('verdana')) return 'Verdana';
  if (font.includes('tahoma')) return 'Tahoma';
  if (font.includes('trebuchet')) return 'Trebuchet MS';
  if (font.includes('impact')) return 'Impact';

  return 'Arial'; // Default fallback
}

/**
 * Map CSS text-align to PptxGenJS align
 */
function mapAlign(textAlign) {
  switch (textAlign) {
    case 'center': return 'center';
    case 'right': return 'right';
    case 'justify': return 'justify';
    default: return 'left';
  }
}

module.exports = { html2pptx, rgbToHex, mapFont, mapAlign };
