# Office Open XML (OOXML) Guide for PowerPoint

This document describes how to edit PowerPoint presentations by working directly with the OOXML format.

## Overview

A .pptx file is a ZIP archive containing XML files and resources. Understanding this structure allows you to make precise edits that aren't possible through high-level libraries.

## File Structure

```
presentation.pptx (ZIP archive)
├── [Content_Types].xml          # MIME types for all parts
├── _rels/
│   └── .rels                    # Root relationships
├── docProps/
│   ├── app.xml                  # Application properties
│   ├── core.xml                 # Core properties (title, author)
│   └── thumbnail.jpeg           # Thumbnail image
└── ppt/
    ├── presentation.xml         # Main presentation file
    ├── presProps.xml            # Presentation properties
    ├── tableStyles.xml          # Table style definitions
    ├── viewProps.xml            # View properties
    ├── _rels/
    │   └── presentation.xml.rels # Presentation relationships
    ├── slideLayouts/
    │   ├── slideLayout1.xml     # Layout definitions
    │   ├── slideLayout2.xml
    │   └── _rels/
    ├── slideMasters/
    │   ├── slideMaster1.xml     # Master slide definitions
    │   └── _rels/
    ├── slides/
    │   ├── slide1.xml           # Individual slides
    │   ├── slide2.xml
    │   └── _rels/
    ├── notesSlides/             # Speaker notes (optional)
    │   ├── notesSlide1.xml
    │   └── _rels/
    ├── comments/                # Comments (optional)
    │   └── modernComment_*.xml
    ├── theme/
    │   └── theme1.xml           # Theme definitions
    └── media/                   # Images, audio, video
        ├── image1.png
        └── image2.jpeg
```

## Namespaces

Common XML namespaces used in OOXML:

```xml
xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
```

## Slide Structure (slide*.xml)

### Basic Slide XML

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
       xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
       xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <!-- Shape tree - contains all shapes on the slide -->
      <p:nvGrpSpPr>...</p:nvGrpSpPr>
      <p:grpSpPr>...</p:grpSpPr>

      <!-- Text shape example -->
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="2" name="Title 1"/>
          <p:cNvSpPr>
            <a:spLocks noGrp="1"/>
          </p:cNvSpPr>
          <p:nvPr>
            <p:ph type="title"/>  <!-- Placeholder type -->
          </p:nvPr>
        </p:nvSpPr>
        <p:spPr>
          <!-- Shape properties (position, size) -->
        </p:spPr>
        <p:txBody>
          <!-- Text content -->
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US"/>
              <a:t>Title Text</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
</p:sld>
```

### Text Elements

#### Paragraph (`<a:p>`)
```xml
<a:p>
  <a:pPr algn="ctr" lvl="0">  <!-- alignment, indent level -->
    <a:buNone/>               <!-- no bullet -->
    <!-- or <a:buChar char="•"/> for bullet -->
  </a:pPr>
  <a:r>
    <a:rPr lang="en-US" sz="2400" b="1">  <!-- size in 100ths of pt, bold -->
      <a:solidFill>
        <a:srgbClr val="FF0000"/>  <!-- RGB color -->
      </a:solidFill>
    </a:rPr>
    <a:t>Text content</a:t>
  </a:r>
</a:p>
```

#### Run Properties (`<a:rPr>`)
- `sz` - Font size in 100ths of a point (2400 = 24pt)
- `b="1"` - Bold
- `i="1"` - Italic
- `u="sng"` - Single underline
- `lang` - Language code

#### Paragraph Properties (`<a:pPr>`)
- `algn` - Alignment: `l` (left), `ctr` (center), `r` (right), `just` (justify)
- `lvl` - Indent level (0-8)
- `<a:buNone/>` - No bullet
- `<a:buChar char="•"/>` - Character bullet
- `<a:buAutoNum type="arabicPeriod"/>` - Numbered list

### Position and Size

Positions and sizes use EMUs (English Metric Units):
- 1 inch = 914400 EMUs
- 1 point = 12700 EMUs
- 1 cm = 360000 EMUs

```xml
<p:spPr>
  <a:xfrm>
    <a:off x="457200" y="274638"/>    <!-- position: 0.5", 0.3" -->
    <a:ext cx="8229600" cy="1143000"/> <!-- size: 9", 1.25" -->
  </a:xfrm>
</p:spPr>
```

### Colors

#### RGB Color
```xml
<a:solidFill>
  <a:srgbClr val="FF5733"/>
</a:solidFill>
```

#### Theme Color
```xml
<a:solidFill>
  <a:schemeClr val="dk1"/>  <!-- dark 1 -->
</a:solidFill>
```

Theme color values: `dk1`, `lt1`, `dk2`, `lt2`, `accent1`-`accent6`, `hlink`, `folHlink`

## Common Edit Operations

### Changing Text Content

Find the `<a:t>` element and update its content:

```python
import xml.etree.ElementTree as ET

# Parse slide XML
tree = ET.parse('ppt/slides/slide1.xml')
root = tree.getroot()

# Define namespaces
ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}

# Find and update text
for t_elem in root.findall('.//a:t', ns):
    if t_elem.text == 'Old Text':
        t_elem.text = 'New Text'

tree.write('ppt/slides/slide1.xml', xml_declaration=True, encoding='UTF-8')
```

### Adding a New Paragraph

```python
from lxml import etree

# Create new paragraph
ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
new_p = etree.Element('{http://schemas.openxmlformats.org/drawingml/2006/main}p')
r = etree.SubElement(new_p, '{http://schemas.openxmlformats.org/drawingml/2006/main}r')
rPr = etree.SubElement(r, '{http://schemas.openxmlformats.org/drawingml/2006/main}rPr')
rPr.set('lang', 'en-US')
t = etree.SubElement(r, '{http://schemas.openxmlformats.org/drawingml/2006/main}t')
t.text = 'New paragraph text'

# Append to text body
txBody = root.find('.//p:txBody', ns)
txBody.append(new_p)
```

### Changing Font Properties

```python
for rPr in root.findall('.//a:rPr', ns):
    rPr.set('sz', '2800')  # 28pt
    rPr.set('b', '1')       # bold
```

### Changing Colors

```python
for solidFill in root.findall('.//a:solidFill', ns):
    # Clear existing color
    for child in list(solidFill):
        solidFill.remove(child)
    # Add new RGB color
    srgbClr = etree.SubElement(solidFill, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
    srgbClr.set('val', '0066CC')
```

## Workflow for Editing Presentations

### 1. Unpack
```bash
python ooxml/scripts/unpack.py presentation.pptx unpacked/
```

### 2. Edit XML Files
Edit the relevant XML files in `unpacked/ppt/slides/`

### 3. Validate
```bash
python ooxml/scripts/validate.py unpacked/ --original presentation.pptx
```

### 4. Pack
```bash
python ooxml/scripts/pack.py unpacked/ output.pptx
```

## Theme and Master Slides

### Theme File (theme1.xml)

Contains color scheme, font scheme, and format scheme:

```xml
<a:theme>
  <a:themeElements>
    <a:clrScheme name="Office">
      <a:dk1><a:sysClr val="windowText"/></a:dk1>
      <a:lt1><a:sysClr val="window"/></a:lt1>
      <a:dk2><a:srgbClr val="44546A"/></a:dk2>
      <a:lt2><a:srgbClr val="E7E6E6"/></a:lt2>
      <a:accent1><a:srgbClr val="4472C4"/></a:accent1>
      <!-- accent2-6, hlink, folHlink -->
    </a:clrScheme>
    <a:fontScheme name="Office">
      <a:majorFont>
        <a:latin typeface="Calibri Light"/>
      </a:majorFont>
      <a:minorFont>
        <a:latin typeface="Calibri"/>
      </a:minorFont>
    </a:fontScheme>
  </a:themeElements>
</a:theme>
```

### Extracting Theme Colors

```python
tree = ET.parse('ppt/theme/theme1.xml')
root = tree.getroot()
ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}

for accent in root.findall('.//a:accent1/a:srgbClr', ns):
    print(f"Accent 1: #{accent.get('val')}")
```

## Relationships Files (*.rels)

Relationships connect parts of the document:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout"
                Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"
                Target="../media/image1.png"/>
</Relationships>
```

### Adding an Image Reference

1. Copy image to `ppt/media/`
2. Add relationship to `ppt/slides/_rels/slideN.xml.rels`
3. Reference in slide XML using the rId

## Speaker Notes

Located in `ppt/notesSlides/notesSlide*.xml`:

```xml
<p:notes>
  <p:cSld>
    <p:spTree>
      <p:sp>
        <p:nvSpPr>
          <p:nvPr><p:ph type="body" idx="1"/></p:nvPr>
        </p:nvSpPr>
        <p:txBody>
          <a:p>
            <a:r><a:t>Speaker notes text here</a:t></a:r>
          </a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
</p:notes>
```

## Comments

Located in `ppt/comments/`:

```xml
<p:cmLst>
  <p:cm authorId="0" dt="2024-01-15T10:30:00" idx="1">
    <p:pos x="100" y="100"/>
    <p:text>Comment text</p:text>
  </p:cm>
</p:cmLst>
```

## Validation Tips

### Common Errors

1. **Missing namespace declarations** - Ensure all required namespaces are declared
2. **Invalid element order** - XML elements must appear in the correct order
3. **Missing relationships** - Every referenced part needs a relationship entry
4. **Invalid rId references** - Relationship IDs must match

### Testing

Always test edited presentations in:
- Microsoft PowerPoint
- LibreOffice Impress
- Google Slides (via upload)

## Best Practices

1. **Always back up** the original file before editing
2. **Validate after each edit** to catch errors early
3. **Use lxml** instead of xml.etree for better namespace handling
4. **Preserve formatting** - copy existing element structure when adding new content
5. **Test incrementally** - make small changes and verify before proceeding
