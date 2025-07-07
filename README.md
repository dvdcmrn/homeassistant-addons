# Pinnacles for Home Assistant

A custom Home Assistant integration that allows you to use Apple's SF Symbols in your Home Assistant dashboards.

## Overview

This integration provides a way to export SF Symbols from macOS and use them in Home Assistant with the `pinnacles:` prefix. Perfect for creating beautiful, consistent iconography in your smart home dashboard.

## Features

- Export SF Symbols to SVG format
- Automatic SVG optimization for web use
- Easy integration with Home Assistant dashboards
- Batch export capabilities
- Interactive symbol selection
- Icon validation and management

## Prerequisites

- macOS with SF Symbols app installed (free from Apple Developer portal)
- Home Assistant instance with custom integrations support
- Python 3.9+ for the export script

## Quick Start

### 1. Install the Integration

1. Copy the `custom_components/pinnacles/` folder to your Home Assistant `custom_components/` directory
2. Create the directory structure:
   ```
   config/
   ├── custom_components/
   │   └── pinnacles/
   └── www/
       └── pinnacles/
           └── icons/
   ```

### 2. Add to Configuration

Add this to your `configuration.yaml`:

```yaml
pinnacles:
```

### 3. Export Your First Icons

```bash
# Navigate to your project directory
cd /path/to/pinnacles_integration

# Run the interactive export script
python3 scripts/export_pinnacles.py --interactive --output ~/exported_pinnacles

# Copy exported symbols to Home Assistant
cp ~/exported_pinnacles/*.svg /path/to/homeassistant/www/pinnacles/icons/
```

### 4. Restart Home Assistant

Restart Home Assistant to load the integration and refresh the icons.

## Usage

### Using Icons in Dashboard

Once exported, use your Pinnacles icons with the `pinnacles:` prefix:

```yaml
type: button
entity: light.living_room
icon: pinnacles:house
```

### Example Dashboard Card

```yaml
type: entities
entities:
  - entity: light.living_room
    icon: pinnacles:house
    name: Living Room
  - entity: sensor.temperature
    icon: pinnacles:thermometer
    name: Temperature
  - entity: switch.fan
    icon: pinnacles:wind
    name: Fan
```

## Export Script Usage

### Interactive Mode
```bash
python3 scripts/export_pinnacles.py --interactive
```

### Export Specific Symbols
```bash
python3 scripts/export_pinnacles.py --symbols house heart star gear
```

### List Available Symbols
```bash
python3 scripts/export_pinnacles.py --list
```

### Custom Output Directory
```bash
python3 scripts/export_pinnacles.py --output ~/my_icons --symbols house heart
```

## Repository Structure

```
pinnacles_integration/
├── custom_components/
│   └── pinnacles/
│       ├── __init__.py          # Main integration file
│       ├── manifest.json        # Integration metadata
│       ├── services.yaml        # Service definitions
│       └── icon_manager.py      # Icon management utilities
├── www/
│   └── pinnacles/
│       └── icons/               # Place exported SVGs here
├── scripts/
│   └── export_pinnacles.py      # Pinnacles export script
├── docs/
│   ├── SETUP.md                 # Detailed setup instructions
│   └── PROJECT_SETUP.md         # Development setup guide
└── README.md                    # This file
```

## Available Services

- `pinnacles.refresh_icons`: Refresh the list of available icons after adding new ones

## Troubleshooting

### Icons Not Showing
1. Check that SVG files are in the correct directory: `www/pinnacles/icons/`
2. Ensure file names match the icon names you're using
3. Restart Home Assistant or call `pinnacles.refresh_icons`
4. Check the Home Assistant logs for any errors

### Export Script Issues
1. Ensure SF Symbols app is installed and can be automated
2. Check that AppleScript permissions are granted
3. Try running the script with `--interactive` flag for debugging

## Documentation

- [Detailed Setup Guide](docs/SETUP.md)
- [Development Setup](docs/PROJECT_SETUP.md)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This integration is for personal use only. SF Symbols are copyrighted by Apple Inc. and subject to their licensing terms.

## Disclaimer

This integration is not affiliated with Apple Inc. SF Symbols are copyrighted by Apple Inc. and subject to their licensing terms. This integration is provided for educational and personal use only.

## Support

If you encounter any issues:

1. Check the troubleshooting section
2. Review the detailed setup guide
3. Open an issue on GitHub with detailed information about your setup

---

Made for the Home Assistant community
