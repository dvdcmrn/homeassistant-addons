# dvdcmrn Home Assistant Icons - Development Setup

This integration is distributed **only via HACS**; end users do not install it manually. This guide is for developers working on the repo.

## 1. Project Structure

Create this folder structure in your VS Code workspace:

```
homeassistant-icons/
├── custom_components/
│   └── dvdcmrn_icons/
│       ├── __init__.py
│       ├── manifest.json
│       ├── services.yaml
│       └── icon_manager.py
├── www/
│   └── dvdcmrn_icons/
│       └── icons/
│           └── (SF Symbol SVGs will go here)
├── docs/
│   ├── SETUP.md
│   └── PROJECT_SETUP.md
├── scripts/
│   └── export_sf_symbols.py
├── hacs.json
├── info.md
├── README.md
└── requirements.txt
```

## 2. VS Code Setup

### Install Python Extension
- Install the "Python" extension by Microsoft
- Install the "Home Assistant Config Helper" extension

### Create Virtual Environment
```bash
cd homeassistant-icons
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install homeassistant
```

### VS Code Settings
Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "files.associations": {
        "*.yaml": "home-assistant"
    }
}
```

## 3. SF Symbols Export Process

### Method 1: Using SF Symbols App + Python Script
The SF Symbols app allows you to export individual symbols. We'll create a Python script to batch process them.

### Method 2: Command Line Tool (Recommended)
Use the `sf-symbols-extractor` tool or create a custom AppleScript/Shell script.

## 4. Home Assistant Integration Files

### manifest.json
Must include `issue_tracker` and other keys required by HACS. Example:
```json
{
  "domain": "dvdcmrn_icons",
  "name": "dvdcmrn Home Assistant Icons",
  "version": "1.0.0",
  "documentation": "https://github.com/dvdcmrn/homeassistant-icons",
  "issue_tracker": "https://github.com/dvdcmrn/homeassistant-icons/issues",
  "requirements": [],
  "codeowners": ["@dvdcmrn"],
  "iot_class": "local_polling"
}
```

### __init__.py
```python
"""dvdcmrn Home Assistant Icons integration."""
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "dvdcmrn_icons"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the dvdcmrn Home Assistant Icons integration."""
    # Register the icon provider
    hass.data[DOMAIN] = {}
    return True
```

## 5. Icon Management

The integration will:
1. Monitor the `www/dvdcmrn_icons/icons/` directory
2. Register available icons with Home Assistant
3. Provide the `sf:` prefix for icon usage
4. Handle SVG optimization for web use

## 6. Export Script Requirements

The export script needs to:
- Convert SF Symbols to SVG format
- Optimize SVGs for web use
- Handle naming conventions
- Batch process multiple icons
- Provide a UI for icon selection
