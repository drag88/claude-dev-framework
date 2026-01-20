#!/usr/bin/env python3
"""Unpack an Office Open XML file (.pptx, .xlsx, .docx) to a directory."""

import sys
import zipfile
from pathlib import Path


def unpack(office_file: str, output_dir: str) -> None:
    """Extract OOXML archive to directory with proper structure."""
    office_path = Path(office_file)
    output_path = Path(output_dir)

    if not office_path.exists():
        print(f"Error: File not found: {office_file}", file=sys.stderr)
        sys.exit(1)

    output_path.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(office_path, 'r') as zf:
        zf.extractall(output_path)

    print(f"Unpacked {office_file} to {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python unpack.py <office_file> <output_dir>", file=sys.stderr)
        sys.exit(1)

    unpack(sys.argv[1], sys.argv[2])
