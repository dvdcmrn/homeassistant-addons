"""Icon management for Pinnacles integration."""
import logging
from pathlib import Path
from typing import Dict, List, Optional
import xml.etree.ElementTree as ET

_LOGGER = logging.getLogger(__name__)

class PinnaclesIconManager:
    """Manage Pinnacles icons for Home Assistant."""
    
    def __init__(self, hass, icons_dir: Path):
        """Initialize the icon manager."""
        self.hass = hass
        self.icons_dir = icons_dir
        self._icons_cache: Dict[str, str] = {}
        
    def scan_icons(self) -> List[str]:
        """Scan the icons directory and return available icons."""
        icons = []
        if not self.icons_dir.exists():
            return icons
            
        for svg_file in self.icons_dir.glob("*.svg"):
            icon_name = svg_file.stem
            icons.append(icon_name)
            
        return sorted(icons)
    
    def get_icon_path(self, icon_name: str) -> Optional[str]:
        """Get the path to an icon file."""
        svg_path = self.icons_dir / f"{icon_name}.svg"
        if svg_path.exists():
            return str(svg_path)
        return None
    
    def optimize_svg(self, svg_path: Path) -> bool:
        """Optimize SVG for web use."""
        try:
            tree = ET.parse(svg_path)
            root = tree.getroot()
            
            # Remove unnecessary attributes
            attrs_to_remove = ['id', 'data-name']
            for attr in attrs_to_remove:
                if attr in root.attrib:
                    del root.attrib[attr]
            
            # Ensure viewBox is set
            if 'viewBox' not in root.attrib:
                width = root.attrib.get('width', '24')
                height = root.attrib.get('height', '24')
                root.attrib['viewBox'] = f"0 0 {width} {height}"
            
            # Set standard dimensions
            root.attrib['width'] = '24'
            root.attrib['height'] = '24'
            
            # Save optimized SVG
            tree.write(svg_path, encoding='utf-8', xml_declaration=True)
            return True
            
        except Exception as e:
            _LOGGER.error(f"Failed to optimize SVG {svg_path}: {e}")
            return False
    
    def validate_icon(self, icon_path: Path) -> bool:
        """Validate that an icon is a proper SVG."""
        try:
            tree = ET.parse(icon_path)
            root = tree.getroot()
            return root.tag.endswith('svg')
        except Exception:
            return False 