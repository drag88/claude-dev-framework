#!/usr/bin/env python3
"""Pack a directory back into an Office Open XML file (.pptx, .xlsx, .docx)."""

import sys
import zipfile
from pathlib import Path


def pack(input_dir: str, office_file: str) -> None:
    """Create OOXML archive from directory contents."""
    input_path = Path(input_dir)
    office_path = Path(office_file)

    if not input_path.exists():
        print(f"Error: Directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)

    # OOXML requires specific file ordering: [Content_Types].xml must be first
    content_types = input_path / "[Content_Types].xml"
    if not content_types.exists():
        print("Error: [Content_Types].xml not found in directory", file=sys.stderr)
        sys.exit(1)

    with zipfile.ZipFile(office_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add [Content_Types].xml first (required by OOXML spec)
        zf.write(content_types, "[Content_Types].xml")

        # Add all other files
        for file_path in sorted(input_path.rglob("*")):
            if file_path.is_file() and file_path.name != "[Content_Types].xml":
                arcname = file_path.relative_to(input_path)
                zf.write(file_path, arcname)

    print(f"Packed {input_dir} to {office_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pack.py <input_directory> <office_file>", file=sys.stderr)
        sys.exit(1)

    pack(sys.argv[1], sys.argv[2])
