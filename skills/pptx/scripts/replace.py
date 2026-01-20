#!/usr/bin/env python3
"""Replace text in PowerPoint presentation shapes based on JSON specification."""

import argparse
import json
import sys
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
    from pptx.enum.dml import MSO_THEME_COLOR
except ImportError:
    print("Error: python-pptx is required. Install with: pip install python-pptx", file=sys.stderr)
    sys.exit(1)

# Import inventory functions
from inventory import extract_inventory


def get_alignment_enum(align_str):
    """Convert alignment string to enum."""
    if align_str == "CENTER":
        return PP_ALIGN.CENTER
    elif align_str == "RIGHT":
        return PP_ALIGN.RIGHT
    elif align_str == "LEFT":
        return PP_ALIGN.LEFT
    return None


def get_theme_color_enum(theme_str):
    """Convert theme color string to enum."""
    theme_map = {
        "DARK_1": MSO_THEME_COLOR.DARK_1,
        "LIGHT_1": MSO_THEME_COLOR.LIGHT_1,
        "DARK_2": MSO_THEME_COLOR.DARK_2,
        "LIGHT_2": MSO_THEME_COLOR.LIGHT_2,
        "ACCENT_1": MSO_THEME_COLOR.ACCENT_1,
        "ACCENT_2": MSO_THEME_COLOR.ACCENT_2,
        "ACCENT_3": MSO_THEME_COLOR.ACCENT_3,
        "ACCENT_4": MSO_THEME_COLOR.ACCENT_4,
        "ACCENT_5": MSO_THEME_COLOR.ACCENT_5,
        "ACCENT_6": MSO_THEME_COLOR.ACCENT_6,
    }
    return theme_map.get(theme_str)


def clear_text_frame(text_frame):
    """Clear all text from a text frame."""
    for para in text_frame.paragraphs:
        para.clear()


def apply_paragraph(text_frame, para_idx, para_spec):
    """Apply paragraph specification to text frame."""
    # Get or create paragraph
    while len(text_frame.paragraphs) <= para_idx:
        text_frame.add_paragraph()

    para = text_frame.paragraphs[para_idx]

    # Clear existing content
    para.clear()

    # Add run with text
    run = para.add_run()
    run.text = para_spec.get("text", "")

    # Apply bullet
    if para_spec.get("bullet"):
        para.level = para_spec.get("level", 0)
    else:
        # Disable bullet
        pPr = para._p.get_or_add_pPr()
        from lxml import etree
        nsmap = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
        buNone = etree.SubElement(pPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}buNone')

    # Apply alignment (skip if bullet - bullets default to left)
    if not para_spec.get("bullet") and para_spec.get("alignment"):
        align = get_alignment_enum(para_spec["alignment"])
        if align:
            para.alignment = align

    # Apply font properties
    font = run.font
    if para_spec.get("font_name"):
        font.name = para_spec["font_name"]
    if para_spec.get("font_size"):
        font.size = Pt(para_spec["font_size"])
    if para_spec.get("bold"):
        font.bold = True
    if para_spec.get("italic"):
        font.italic = True
    if para_spec.get("underline"):
        font.underline = True

    # Apply color
    if para_spec.get("color"):
        hex_color = para_spec["color"]
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        font.color.rgb = RGBColor(r, g, b)
    elif para_spec.get("theme_color"):
        theme = get_theme_color_enum(para_spec["theme_color"])
        if theme:
            font.color.theme_color = theme


def validate_replacement_json(inventory, replacement):
    """Validate that all shapes in replacement JSON exist in inventory."""
    errors = []

    for slide_key, shapes in replacement.items():
        if slide_key not in inventory:
            errors.append(f"Slide '{slide_key}' not found in inventory")
            continue

        inv_shapes = inventory[slide_key]
        for shape_key in shapes.keys():
            if shape_key not in inv_shapes:
                available = ", ".join(inv_shapes.keys())
                errors.append(f"Shape '{shape_key}' not found on '{slide_key}'. Available shapes: {available}")

    return errors


def replace_text(pptx_path: Path, replacement: dict, output_path: Path) -> None:
    """Replace text in presentation based on replacement specification."""
    # First extract inventory to know all shapes
    inventory = extract_inventory(pptx_path)

    # Validate replacement JSON
    errors = validate_replacement_json(inventory, replacement)
    if errors:
        print("ERROR: Invalid shapes in replacement JSON:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)

    # Load presentation
    prs = Presentation(str(pptx_path))

    # Process each slide
    for slide_idx, slide in enumerate(prs.slides):
        slide_key = f"slide-{slide_idx}"

        if slide_key not in inventory:
            continue

        # Get shapes sorted by position (same as inventory)
        text_shapes = [s for s in slide.shapes if s.has_text_frame]
        text_shapes.sort(key=lambda s: (s.top or 0, s.left or 0))

        # Clear all shapes first
        for shape in text_shapes:
            clear_text_frame(shape.text_frame)

        # Apply replacements
        if slide_key in replacement:
            slide_replacement = replacement[slide_key]

            for shape_idx, shape in enumerate(text_shapes):
                shape_key = f"shape-{shape_idx}"

                if shape_key in slide_replacement:
                    shape_spec = slide_replacement[shape_key]
                    paragraphs = shape_spec.get("paragraphs", [])

                    tf = shape.text_frame

                    for para_idx, para_spec in enumerate(paragraphs):
                        apply_paragraph(tf, para_idx, para_spec)

    prs.save(str(output_path))
    print(f"Saved updated presentation to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Replace text in PPTX based on JSON spec")
    parser.add_argument("pptx_file", help="Source PowerPoint file")
    parser.add_argument("replacement_json", help="JSON file with replacement specifications")
    parser.add_argument("output_file", help="Output PowerPoint file")
    args = parser.parse_args()

    pptx_path = Path(args.pptx_file)
    if not pptx_path.exists():
        print(f"Error: File not found: {args.pptx_file}", file=sys.stderr)
        sys.exit(1)

    json_path = Path(args.replacement_json)
    if not json_path.exists():
        print(f"Error: File not found: {args.replacement_json}", file=sys.stderr)
        sys.exit(1)

    with open(json_path, 'r', encoding='utf-8') as f:
        replacement = json.load(f)

    replace_text(pptx_path, replacement, Path(args.output_file))


if __name__ == "__main__":
    main()
