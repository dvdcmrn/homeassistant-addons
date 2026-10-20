"""Manage user-exported SF Symbol SVGs for the sf: Home Assistant prefix."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Dict, List, Optional, TypedDict
import xml.etree.ElementTree as ET

_LOGGER = logging.getLogger(__name__)

_WEIGHTS = (
    "Ultralight",
    "Thin",
    "Light",
    "Regular",
    "Medium",
    "Semibold",
    "Bold",
    "Heavy",
    "Black",
)
_TEMPLATE_ID = re.compile(r"^(" + "|".join(_WEIGHTS) + r")-(S|M|L)$")
_DEFAULT_VIEWBOX = "0 0 24 24"


class IconListItem(TypedDict):
    name: str
    keywords: List[str]


def to_ha_name(stem: str) -> str:
    """Convert an SVG filename stem to an sf: icon name (dots become hyphens)."""
    return stem.replace(".", "-")


def keywords_for(ha_name: str) -> List[str]:
    """Split an sf: name into icon-picker keywords."""
    return [part for part in ha_name.split("-") if part]


def _local_tag(tag: str) -> str:
    return tag.split("}", 1)[-1]


def _iter_elements(root: ET.Element):
    yield root
    for child in list(root):
        yield from _iter_elements(child)


def is_symbol_template(root: ET.Element) -> bool:
    """True if this SVG looks like an Xcode SF Symbol template (Export Symbol)."""
    for element in _iter_elements(root):
        element_id = element.attrib.get("id", "")
        if _TEMPLATE_ID.match(element_id):
            return True
    return False


def _collect_paths(element: ET.Element, paths: List[str]) -> None:
    if element.attrib.get("opacity") == "0":
        return
    if _local_tag(element.tag) == "path":
        d_attr = element.attrib.get("d")
        if d_attr:
            paths.append(d_attr.strip())
    for child in list(element):
        _collect_paths(child, paths)


def _viewbox_for(root: ET.Element) -> str:
    viewbox = root.attrib.get("viewBox") or root.attrib.get("viewbox")
    if viewbox:
        return " ".join(viewbox.split())
    width = root.attrib.get("width", "24")
    height = root.attrib.get("height", "24")
    return f"0 0 {width} {height}"


def parse_svg(svg_path: Path) -> Optional[Dict[str, str]]:
    """Return {path, viewBox} for a simple exported SVG, or None if unusable."""
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
    except ET.ParseError:
        _LOGGER.warning("Invalid SVG, skipping: %s", svg_path.name)
        return None

    if _local_tag(root.tag) != "svg":
        _LOGGER.warning("Not an SVG, skipping: %s", svg_path.name)
        return None

    if is_symbol_template(root):
        _LOGGER.warning(
            "Skipping Xcode symbol template %s. Use File → Export Image… (SVG), "
            "not File → Export Symbol…",
            svg_path.name,
        )
        return None

    paths: List[str] = []
    _collect_paths(root, paths)
    if not paths:
        _LOGGER.warning("No SVG path data in %s", svg_path.name)
        return None

    return {"path": " ".join(paths), "viewBox": _viewbox_for(root) or _DEFAULT_VIEWBOX}


class IconManager:
    """Scan www/cupertino-icons and resolve sf: names to SVG path data."""

    def __init__(self, icons_dir: Path) -> None:
        self.icons_dir = icons_dir

    def count_svgs(self) -> int:
        if not self.icons_dir.exists():
            return 0
        return len(list(self.icons_dir.glob("*.svg")))

    def resolve_file(self, ha_name: str) -> Optional[Path]:
        """Prefer Apple dotted names (homepod.fill.svg), then hyphenated fallback."""
        dotted_stem = ha_name.replace("-", ".")
        candidates = [self.icons_dir / f"{dotted_stem}.svg"]
        if dotted_stem != ha_name:
            candidates.append(self.icons_dir / f"{ha_name}.svg")
        for path in candidates:
            if path.is_file():
                return path
        return None

    def get_icon(self, ha_name: str) -> Optional[Dict[str, str]]:
        svg_path = self.resolve_file(ha_name)
        if svg_path is None:
            return None
        return parse_svg(svg_path)

    def list_icons(self) -> List[IconListItem]:
        """Return unique {name, keywords} entries for usable SVGs."""
        if not self.icons_dir.exists():
            return []

        by_name: Dict[str, IconListItem] = {}
        # Dotted Apple names first so they win over hyphen duplicates in listing.
        files = sorted(
            self.icons_dir.glob("*.svg"),
            key=lambda path: (0 if "." in path.stem else 1, path.name),
        )
        for svg_file in files:
            ha_name = to_ha_name(svg_file.stem)
            if ha_name in by_name:
                continue
            if parse_svg(svg_file) is None:
                continue
            by_name[ha_name] = {"name": ha_name, "keywords": keywords_for(ha_name)}
        return [by_name[name] for name in sorted(by_name)]
