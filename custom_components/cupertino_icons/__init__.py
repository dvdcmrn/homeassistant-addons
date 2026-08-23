"""Cupertino Icons integration (user-exported SF Symbols)."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.components.http.view import HomeAssistantView
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.service import async_register_admin_service
from homeassistant.helpers.typing import ConfigType

from .icon_manager import IconManager

_LOGGER = logging.getLogger(__name__)

DOMAIN = "cupertino_icons"
URL_BASE = "/cupertino-icons"
ICONS_DIR = "www/cupertino-icons"
DATA_EXTRA_MODULE_URL = "frontend_extra_module_url"
LOADER_URL = f"{URL_BASE}/iconset.js"
LIST_URL = f"{URL_BASE}/list"
ICON_URL = f"{URL_BASE}/icon/{{icon_name}}"
CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)
FOLDER_README_NAME = "README.txt"
FOLDER_README = """SF Symbols for Home Assistant (sf: prefix)

Drop SVG files exported from the SF Symbols Mac app into this folder.
Use File → Export Image… and choose SVG — not File → Export Symbol….

Keep Apple's dotted filename, e.g. homepod.fill.svg
Then use it in a dashboard as: icon: sf:homepod-fill

After adding files, call the cupertino_icons.refresh_icons service (or restart)
and hard-reload the browser.

This integration ships no Apple artwork. Symbols you export stay on this
Home Assistant host and are for personal use.
"""


class ListingView(HomeAssistantView):
    """List usable sf: icon names for the icon picker."""

    requires_auth = False
    url = LIST_URL
    name = "api:cupertino-icons:list"

    def __init__(self, manager: IconManager) -> None:
        self.manager = manager

    async def get(self, request):
        """Return [{name, keywords}, ...]."""
        return self.json(self.manager.list_icons())


class IconView(HomeAssistantView):
    """Return path data for one sf: icon."""

    requires_auth = False
    url = ICON_URL
    name = "api:cupertino-icons:icon"

    def __init__(self, manager: IconManager) -> None:
        self.manager = manager

    async def get(self, request, icon_name: str):
        """Return {path, viewBox} or 404."""
        icon = self.manager.get_icon(icon_name)
        if icon is None:
            return self.json({"message": "Icon not found"}, status_code=404)
        return self.json(icon)


def _ensure_icons_dir(icons_path: Path) -> None:
    icons_path.mkdir(parents=True, exist_ok=True)
    readme = icons_path / FOLDER_README_NAME
    if not readme.exists():
        readme.write_text(FOLDER_README, encoding="utf-8")


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Cupertino Icons integration."""
    icons_path = Path(hass.config.config_dir) / ICONS_DIR
    _ensure_icons_dir(icons_path)
    manager = IconManager(icons_path)
    hass.data[DOMAIN] = {"icons_path": icons_path, "manager": manager}

    loader_path = Path(__file__).parent / "iconset.js"
    await hass.http.async_register_static_paths(
        [StaticPathConfig(LOADER_URL, str(loader_path), True)]
    )
    hass.data.setdefault(DATA_EXTRA_MODULE_URL, set()).add(LOADER_URL)

    hass.http.register_view(ListingView(manager))
    hass.http.register_view(IconView(manager))

    async_register_admin_service(
        hass,
        DOMAIN,
        "refresh_icons",
        handle_refresh_icons,
        schema=None,
    )

    _LOGGER.info("Cupertino Icons loaded; drop SVGs in %s", icons_path)
    return True


async def handle_refresh_icons(call: ServiceCall) -> None:
    """Rescan www/cupertino-icons and notify the frontend."""
    hass = call.hass
    stored = hass.data.get(DOMAIN, {})
    icons_path = stored.get("icons_path")
    if icons_path is None:
        icons_path = Path(hass.config.config_dir) / ICONS_DIR
        _ensure_icons_dir(icons_path)
    manager = stored.get("manager") or IconManager(icons_path)
    icon_count = manager.count_svgs()
    _LOGGER.info("Refreshed icons: %s SVG files in %s", icon_count, icons_path)
    hass.bus.async_fire("cupertino_icons_refreshed", {"count": icon_count})
