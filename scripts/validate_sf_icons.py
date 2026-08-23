#!/usr/bin/env python3
"""Validate SF Symbol SVGs for the cupertino_icons Home Assistant integration."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from custom_components.cupertino_icons.icon_manager import (  # noqa: E402
    IconManager,
    parse_svg,
    to_ha_name,
)


def validate_directory(directory: Path) -> int:
    """Print a report for each SVG. Return the number of unusable files."""
    if not directory.is_dir():
        print(f"Not a directory: {directory}", file=sys.stderr)
        return -1

    svgs = sorted(directory.glob("*.svg"))
    if not svgs:
        print(f"No SVG files in {directory}")
        return 0

    bad = 0
    for svg in svgs:
        ha_name = to_ha_name(svg.stem)
        result = parse_svg(svg)
        if result is None:
            print(f"FAIL  {svg.name}  (not a usable dashboard icon)")
            bad += 1
        else:
            print(f"OK    {svg.name}  ->  sf:{ha_name}")

    manager = IconManager(directory)
    print(
        f"\n{len(svgs) - bad} usable, {bad} skipped, "
        f"{manager.count_svgs()} svg files"
    )
    return bad


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Validate SVGs for the sf: Home Assistant icon prefix. "
            "Use File → Export Image… (SVG) from SF Symbols, not Export Symbol…"
        )
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Folder of SVG files (default: current directory)",
    )
    args = parser.parse_args(argv)
    directory = Path(args.directory).expanduser().resolve()
    result = validate_directory(directory)
    if result < 0:
        return 2
    return 1 if result else 0


if __name__ == "__main__":
    sys.exit(main())
