#!/usr/bin/env python3
"""Rearrange, duplicate, and delete slides in a PowerPoint presentation."""

import argparse
import sys
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Inches
    import copy
except ImportError:
    print("Error: python-pptx is required. Install with: pip install python-pptx", file=sys.stderr)
    sys.exit(1)


def duplicate_slide(prs, index):
    """Duplicate a slide at the given index."""
    template = prs.slides[index]

    # Get the slide layout
    slide_layout = template.slide_layout

    # Add a new slide with the same layout
    new_slide = prs.slides.add_slide(slide_layout)

    # Copy shapes from template to new slide
    for shape in template.shapes:
        if shape.is_placeholder:
            # Handle placeholders
            try:
                ph = new_slide.placeholders[shape.placeholder_format.idx]
                if shape.has_text_frame:
                    # Copy text
                    for i, para in enumerate(shape.text_frame.paragraphs):
                        if i < len(ph.text_frame.paragraphs):
                            target_para = ph.text_frame.paragraphs[i]
                        else:
                            target_para = ph.text_frame.add_paragraph()
                        target_para.text = para.text
                        target_para.level = para.level
                        target_para.alignment = para.alignment
            except KeyError:
                pass
        else:
            # Clone non-placeholder shapes using XML
            el = shape.element
            new_el = copy.deepcopy(el)
            new_slide.shapes._spTree.insert_element_before(new_el, 'p:extLst')

    return new_slide


def rearrange_slides(input_file: str, output_file: str, order: str) -> None:
    """Create a new presentation with slides in specified order."""
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"Error: File not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    # Parse order string (e.g., "0,34,34,50,52")
    try:
        indices = [int(x.strip()) for x in order.split(',')]
    except ValueError:
        print("Error: Order must be comma-separated integers (e.g., '0,34,34,50,52')", file=sys.stderr)
        sys.exit(1)

    # Load presentation
    prs = Presentation(input_file)
    total_slides = len(prs.slides)

    # Validate indices
    for idx in indices:
        if idx < 0 or idx >= total_slides:
            print(f"Error: Slide index {idx} out of range (0-{total_slides-1})", file=sys.stderr)
            sys.exit(1)

    # Create new presentation from the template (to preserve masters/themes)
    new_prs = Presentation(input_file)

    # Delete all slides from new presentation
    while len(new_prs.slides) > 0:
        rId = new_prs.slides._sldIdLst[0].rId
        new_prs.part.drop_rel(rId)
        del new_prs.slides._sldIdLst[0]

    # Add slides in the specified order
    for idx in indices:
        source_slide = prs.slides[idx]
        slide_layout = source_slide.slide_layout

        # Add new slide with same layout
        new_slide = new_prs.slides.add_slide(slide_layout)

        # Copy all shapes
        for shape in source_slide.shapes:
            if shape.is_placeholder:
                try:
                    ph_idx = shape.placeholder_format.idx
                    if ph_idx in new_slide.placeholders:
                        target = new_slide.placeholders[ph_idx]
                        if shape.has_text_frame and target.has_text_frame:
                            # Clear existing text
                            for para in target.text_frame.paragraphs:
                                para.clear()

                            # Copy paragraphs
                            for i, para in enumerate(shape.text_frame.paragraphs):
                                if i == 0:
                                    target_para = target.text_frame.paragraphs[0]
                                else:
                                    target_para = target.text_frame.add_paragraph()

                                # Copy runs to preserve formatting
                                for run in para.runs:
                                    target_run = target_para.add_run()
                                    target_run.text = run.text
                                    if run.font.bold is not None:
                                        target_run.font.bold = run.font.bold
                                    if run.font.italic is not None:
                                        target_run.font.italic = run.font.italic
                                    if run.font.size is not None:
                                        target_run.font.size = run.font.size
                                    if run.font.name is not None:
                                        target_run.font.name = run.font.name

                                target_para.level = para.level
                                if para.alignment:
                                    target_para.alignment = para.alignment
                except (KeyError, AttributeError):
                    pass
            else:
                # Clone non-placeholder shapes
                el = shape.element
                new_el = copy.deepcopy(el)
                new_slide.shapes._spTree.insert_element_before(new_el, 'p:extLst')

    new_prs.save(output_file)
    print(f"Created {output_file} with {len(indices)} slides from indices: {order}")


def main():
    parser = argparse.ArgumentParser(description="Rearrange slides in a PPTX file")
    parser.add_argument("input_file", help="Source PowerPoint file")
    parser.add_argument("output_file", help="Output PowerPoint file")
    parser.add_argument("order", help="Comma-separated slide indices (0-based), e.g., '0,34,34,50,52'")
    args = parser.parse_args()

    rearrange_slides(args.input_file, args.output_file, args.order)


if __name__ == "__main__":
    main()
