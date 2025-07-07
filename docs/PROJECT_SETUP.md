# Home Assistant SF Symbols Integration Setup

## 1. Project Structure

Create this folder structure in your VS Code workspace:

```
sf_symbols_integration/
├── custom_components/
│   └── sf_symbols/
│       ├── __init__.py
│       ├── manifest.json
│       ├── services.yaml
│       └── icon_manager.py
├── www/
│   └── sf_symbols/
│       └── icons/
│           └── (SF Symbol SVGs will go here)
├── docs/
│   ├── README.md
│   └── SETUP.md
├── scripts/
│   └── export_sf_symbols.py
└── requirements.txt
```

## 2. VS Code Setup

### Install Python Extension
- Install the "Python" extension by Microsoft
- Install the "Home Assistant Config Helper" extension

### Create Virtual Environment
```bash
cd sf_symbols_integration
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
```json
{
  "domain": "sf_symbols",
  "name": "SF Symbols Icon Provider",
  "version": "1.0.0",
  "documentation": "https://github.com/yourusername/sf-symbols-ha",
  "requirements": [],
  "codeowners": ["@yourusername"],
  "iot_class": "local_polling"
}
```

### __init__.py
```python
"""SF Symbols integration for Home Assistant."""
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "sf_symbols"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the SF Symbols integration."""
    # Register the icon provider
    hass.data[DOMAIN] = {}
    return True
```

## 5. Icon Management

The integration will:
1. Monitor the `www/sf_symbols/icons/` directory
2. Register available icons with Home Assistant
3. Provide the `sfs:` prefix for icon usage
4. Handle SVG optimization for web use

## 6. Export Script Requirements

The export script needs to:
- Convert SF Symbols to SVG format
- Optimize SVGs for web use
- Handle naming conventions
- Batch process multiple icons
- Provide a UI for icon selection
