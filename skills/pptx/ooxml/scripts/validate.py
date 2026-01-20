#!/usr/bin/env python3
"""Validate OOXML structure and XML well-formedness."""

import argparse
import sys
import zipfile
from pathlib import Path

try:
    from defusedxml import ElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET


def validate_xml_file(file_path: Path) -> list[str]:
    """Validate a single XML file, return list of errors."""
    errors = []
    try:
        ET.parse(file_path)
    except ET.ParseError as e:
        errors.append(f"{file_path}: XML parse error: {e}")
    return errors


def validate_directory(dir_path: Path) -> list[str]:
    """Validate all XML files in unpacked OOXML directory."""
    errors = []

    # Check required files
    content_types = dir_path / "[Content_Types].xml"
    if not content_types.exists():
        errors.append("Missing required file: [Content_Types].xml")

    rels_dir = dir_path / "_rels"
    if not rels_dir.exists():
        errors.append("Missing required directory: _rels/")

    # Validate all XML files
    for xml_file in dir_path.rglob("*.xml"):
        errors.extend(validate_xml_file(xml_file))

    for rels_file in dir_path.rglob("*.rels"):
        errors.extend(validate_xml_file(rels_file))

    return errors


def validate_archive(archive_path: Path) -> list[str]:
    """Validate OOXML archive without unpacking."""
    errors = []

    try:
        with zipfile.ZipFile(archive_path, 'r') as zf:
            # Check for required files
            names = zf.namelist()
            if "[Content_Types].xml" not in names:
                errors.append("Missing required file: [Content_Types].xml")

            # Validate XML content
            for name in names:
                if name.endswith('.xml') or name.endswith('.rels'):
                    try:
                        content = zf.read(name)
                        ET.fromstring(content)
                    except ET.ParseError as e:
                        errors.append(f"{name}: XML parse error: {e}")
    except zipfile.BadZipFile as e:
        errors.append(f"Invalid ZIP archive: {e}")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate OOXML structure")
    parser.add_argument("path", help="Directory or archive to validate")
    parser.add_argument("--original", help="Original file to compare against")
    args = parser.parse_args()

    path = Path(args.path)

    if path.is_dir():
        errors = validate_directory(path)
    elif path.is_file():
        errors = validate_archive(path)
    else:
        print(f"Error: Path not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    if errors:
        print("Validation errors found:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print("Validation passed: No errors found")


if __name__ == "__main__":
    main()
