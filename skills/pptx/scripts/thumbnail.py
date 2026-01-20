#!/usr/bin/env python3
"""Generate thumbnail grids from PowerPoint presentations."""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow", file=sys.stderr)
    sys.exit(1)


def convert_to_pdf(pptx_path: Path, output_dir: Path) -> Path:
    """Convert PPTX to PDF using LibreOffice."""
    result = subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(output_dir), str(pptx_path)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"LibreOffice conversion failed: {result.stderr}")
    return output_dir / f"{pptx_path.stem}.pdf"


def pdf_to_images(pdf_path: Path, output_dir: Path) -> list[Path]:
    """Convert PDF pages to images using pdftoppm."""
    prefix = output_dir / "slide"
    result = subprocess.run(
        ["pdftoppm", "-jpeg", "-r", "150", str(pdf_path), str(prefix)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdftoppm failed: {result.stderr}")
    return sorted(output_dir.glob("slide-*.jpg"))


def create_thumbnail_grid(images: list[Path], output_path: Path, cols: int = 5) -> None:
    """Create a grid of thumbnails with slide numbers."""
    if not images:
        print("No images to process", file=sys.stderr)
        return

    # Calculate grid dimensions
    thumb_width = 300
    thumb_height = int(thumb_width * 9 / 16)  # 16:9 aspect ratio
    padding = 10
    label_height = 25

    rows = (len(images) + cols - 1) // cols
    grid_width = cols * (thumb_width + padding) + padding
    grid_height = rows * (thumb_height + label_height + padding) + padding

    grid = Image.new('RGB', (grid_width, grid_height), 'white')
    draw = ImageDraw.Draw(grid)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except (OSError, IOError):
        font = ImageFont.load_default()

    for idx, img_path in enumerate(images):
        row, col = divmod(idx, cols)
        x = col * (thumb_width + padding) + padding
        y = row * (thumb_height + label_height + padding) + padding

        with Image.open(img_path) as img:
            img.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
            # Center thumbnail in cell
            offset_x = (thumb_width - img.width) // 2
            offset_y = (thumb_height - img.height) // 2
            grid.paste(img, (x + offset_x, y + offset_y))

        # Add slide number label (0-indexed)
        label = f"Slide {idx}"
        draw.text((x + 5, y + thumb_height + 2), label, fill='black', font=font)

    grid.save(output_path, "JPEG", quality=90)
    print(f"Created thumbnail grid: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate thumbnail grids from PPTX")
    parser.add_argument("pptx_file", help="PowerPoint file to process")
    parser.add_argument("output_prefix", nargs="?", default="thumbnails", help="Output file prefix")
    parser.add_argument("--cols", type=int, default=5, choices=range(3, 7), help="Columns per grid (3-6)")
    args = parser.parse_args()

    pptx_path = Path(args.pptx_file)
    if not pptx_path.exists():
        print(f"Error: File not found: {args.pptx_file}", file=sys.stderr)
        sys.exit(1)

    # Grid limits based on columns
    max_per_grid = {3: 12, 4: 20, 5: 30, 6: 42}[args.cols]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Convert PPTX to PDF, then to images
        pdf_path = convert_to_pdf(pptx_path, tmpdir)
        images = pdf_to_images(pdf_path, tmpdir)

        if not images:
            print("Error: No slides found in presentation", file=sys.stderr)
            sys.exit(1)

        # Create grids (split if needed)
        for grid_idx, start in enumerate(range(0, len(images), max_per_grid)):
            batch = images[start:start + max_per_grid]
            if len(images) <= max_per_grid:
                output_path = Path(f"{args.output_prefix}.jpg")
            else:
                output_path = Path(f"{args.output_prefix}-{grid_idx + 1}.jpg")
            create_thumbnail_grid(batch, output_path, args.cols)


if __name__ == "__main__":
    main()
