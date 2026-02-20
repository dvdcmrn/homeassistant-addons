"""dvdcmrn Home Assistant Icons integration."""
import logging
import os
from pathlib import Path
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.helpers.service import async_register_admin_service

_LOGGER = logging.getLogger(__name__)

DOMAIN = "dvdcmrn_icons"
ICONS_DIR = "www/dvdcmrn_icons/icons"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the dvdcmrn Home Assistant Icons integration."""
    hass.data[DOMAIN] = {}
    
    # Ensure icons directory exists
    icons_path = Path(hass.config.config_dir) / ICONS_DIR
    icons_path.mkdir(parents=True, exist_ok=True)
    
    # Register icon provider
    await register_icon_provider(hass)
    
    # Register services
    async_register_admin_service(
        hass,
        DOMAIN,
        "refresh_icons",
        handle_refresh_icons,
        schema=None,
    )
    
    _LOGGER.info("dvdcmrn Home Assistant Icons integration loaded successfully")
    return True

async def register_icon_provider(hass: HomeAssistant):
    """Register the icon provider."""
    from homeassistant.components.frontend import async_register_built_in_panel
    
    # Register the icon provider with Home Assistant
    if hasattr(hass.components, 'frontend'):
        # This would register our custom icon provider
        # Implementation depends on HA's icon system
        pass

async def handle_refresh_icons(call: ServiceCall):
    """Handle the refresh_icons service call."""
    hass = call.hass
    icons_path = Path(hass.config.config_dir) / ICONS_DIR
    
    # Scan for new icons
    icon_count = len(list(icons_path.glob("*.svg")))
    
    _LOGGER.info(f"Refreshed icons: {icon_count} icons found")
    
    # Notify frontend to refresh
    hass.bus.async_fire("dvdcmrn_icons_refreshed", {"count": icon_count})
