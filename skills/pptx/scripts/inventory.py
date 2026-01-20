#!/usr/bin/env python3
"""Extract text inventory from PowerPoint presentation shapes."""

import argparse
import json
import sys
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
except ImportError:
    print("Error: python-pptx is required. Install with: pip install python-pptx", file=sys.stderr)
    sys.exit(1)


def emu_to_inches(emu):
    """Convert EMUs to inches."""
    return emu / 914400 if emu else 0


def get_alignment_str(alignment):
    """Convert alignment enum to string."""
    if alignment == PP_ALIGN.CENTER:
        return "CENTER"
    elif alignment == PP_ALIGN.RIGHT:
        return "RIGHT"
    return None  # LEFT is default, don't include


def get_color_str(color):
    """Extract color as hex string."""
    try:
        if color.type is not None:
            if hasattr(color, 'rgb') and color.rgb:
                return f"{color.rgb}"
            if hasattr(color, 'theme_color') and color.theme_color:
                return None  # Will handle theme_color separately
    except Exception:
        pass
    return None


def get_theme_color_str(color):
    """Extract theme color name."""
    try:
        if hasattr(color, 'theme_color') and color.theme_color:
            return str(color.theme_color).replace("MSO_THEME_COLOR.", "")
    except Exception:
        pass
    return None


def extract_paragraph_info(paragraph):
    """Extract paragraph formatting info."""
    info = {"text": paragraph.text}

    # Bullet detection
    if paragraph.level is not None and paragraph.level >= 0:
        # Check if has bullet by examining XML
        pPr = paragraph._p.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}pPr')
        if pPr is not None:
            buNone = pPr.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}buNone')
            if buNone is None:  # Has bullet if buNone is NOT present
                info["bullet"] = True
                info["level"] = paragraph.level

    # Alignment
    if paragraph.alignment:
        align_str = get_alignment_str(paragraph.alignment)
        if align_str:
            info["alignment"] = align_str

    # Spacing (convert from EMUs to points)
    pPr = paragraph._p.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}pPr')
    if pPr is not None:
        spcBef = pPr.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}spcBef')
        if spcBef is not None:
            spcPts = spcBef.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}spcPts')
            if spcPts is not None and spcPts.get('val'):
                info["space_before"] = int(spcPts.get('val')) / 100

        spcAft = pPr.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}spcAft')
        if spcAft is not None:
            spcPts = spcAft.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}spcPts')
            if spcPts is not None and spcPts.get('val'):
                info["space_after"] = int(spcPts.get('val')) / 100

        lnSpc = pPr.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}lnSpc')
        if lnSpc is not None:
            spcPts = lnSpc.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}spcPts')
            if spcPts is not None and spcPts.get('val'):
                info["line_spacing"] = int(spcPts.get('val')) / 100

    # Font properties from first run
    if paragraph.runs:
        run = paragraph.runs[0]
        font = run.font
        if font.name:
            info["font_name"] = font.name
        if font.size:
            info["font_size"] = font.size.pt
        if font.bold:
            info["bold"] = True
        if font.italic:
            info["italic"] = True
        if font.underline:
            info["underline"] = True
        if font.color and font.color.type is not None:
            rgb = get_color_str(font.color)
            if rgb:
                info["color"] = rgb
            theme = get_theme_color_str(font.color)
            if theme:
                info["theme_color"] = theme

    return info


def extract_shape_info(shape, shape_idx):
    """Extract shape information including text and formatting."""
    info = {
        "left": round(emu_to_inches(shape.left), 2),
        "top": round(emu_to_inches(shape.top), 2),
        "width": round(emu_to_inches(shape.width), 2),
        "height": round(emu_to_inches(shape.height), 2),
    }

    # Placeholder type
    if shape.is_placeholder:
        ph_type = shape.placeholder_format.type
        # Skip slide numbers
        if str(ph_type) == "SLIDE_NUMBER (13)":
            return None
        info["placeholder_type"] = str(ph_type).split()[0]
    else:
        info["placeholder_type"] = None

    # Extract text
    if shape.has_text_frame:
        paragraphs = []
        for para in shape.text_frame.paragraphs:
            if para.text.strip():  # Only non-empty paragraphs
                paragraphs.append(extract_paragraph_info(para))
        if paragraphs:
            info["paragraphs"] = paragraphs

    return info if "paragraphs" in info else None


def extract_inventory(pptx_path: Path) -> dict:
    """Extract complete text inventory from presentation."""
    prs = Presentation(str(pptx_path))
    inventory = {}

    for slide_idx, slide in enumerate(prs.slides):
        slide_key = f"slide-{slide_idx}"
        shapes_info = {}

        # Sort shapes by position (top-to-bottom, left-to-right)
        text_shapes = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                text_shapes.append(shape)

        text_shapes.sort(key=lambda s: (s.top or 0, s.left or 0))

        shape_counter = 0
        for shape in text_shapes:
            info = extract_shape_info(shape, shape_counter)
            if info:
                shapes_info[f"shape-{shape_counter}"] = info
                shape_counter += 1

        if shapes_info:
            inventory[slide_key] = shapes_info

    return inventory


def main():
    parser = argparse.ArgumentParser(description="Extract text inventory from PPTX")
    parser.add_argument("pptx_file", help="PowerPoint file to analyze")
    parser.add_argument("output_file", help="Output JSON file")
    args = parser.parse_args()

    pptx_path = Path(args.pptx_file)
    if not pptx_path.exists():
        print(f"Error: File not found: {args.pptx_file}", file=sys.stderr)
        sys.exit(1)

    inventory = extract_inventory(pptx_path)

    with open(args.output_file, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=2)

    print(f"Inventory saved to: {args.output_file}")


if __name__ == "__main__":
    main()
