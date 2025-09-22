# DVDCMRN Home Assistant Add-ons

My personal Home Assistant add-on library featuring custom add-ons for enhanced functionality.

## Repository Information

- **Repository URL**: https://github.com/dvdcmrn/homeassistant-addons
- **Maintainer**: David <git@dvdcmrn.de>

## Add-ons

### 1. OLED System Monitor

Display system information on an OLED display connected to your Home Assistant device via I2C.

**Features:**
- Support for SSD1306 and SH1106 OLED displays
- Customizable metrics (CPU, RAM, disk usage, temperature, uptime)
- Configurable display settings (contrast, rotation)
- Network information display
- Custom text support
- Visual bar graphs for usage metrics
- Automatic I2C device detection
- Debug mode for testing without OLED display

**Latest Version**: 1.3.2

**Installation:**
1. Add this repository to your Home Assistant instance
2. Install the "OLED System Monitor" add-on
3. Configure the add-on with your display settings
4. Start the add-on

**I2C Enablement:**
The add-on includes enhanced I2C enablement functionality based on the [HassOSConfigurator](https://github.com/adamoutler/HassOSConfigurator/tree/main/Pi4EnableI2C) project by [adamoutler](https://github.com/adamoutler). This allows automatic I2C configuration for Raspberry Pi 4 and Pi 5 devices running Home Assistant OS.

For detailed configuration options, troubleshooting, and I2C setup instructions, see the [OLED System Monitor documentation](./oled-display/README.md).

## Adding This Repository

To add this repository to your Home Assistant instance:

1. Go to **Supervisor** → **Add-on Store**
2. Click the three dots menu (⋮) in the top right corner
3. Select **Repositories**
4. Add this repository URL: `https://github.com/dvdcmrn/homeassistant-addons`
5. Click **Add**

## Support

For issues, feature requests, or questions about these add-ons, please visit the [GitHub repository](https://github.com/dvdcmrn/homeassistant-addons).
