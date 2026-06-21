# DVDCMRN Home Assistant Add-ons

My personal Home Assistant add-on library featuring custom add-ons for enhanced functionality.

## Repository Information

- **Repository URL**: https://github.com/dvdcmrn/homeassistant-addons
- **Maintainer**: [dvdcmrn](https://github.com/dvdcmrn)

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

**Latest Version**: 1.5.0

**Installation:**
1. Add this repository to your Home Assistant instance
2. Install the "OLED System Monitor" add-on
3. Configure the add-on with your display settings
4. Start the add-on

**HAOS setup (1.5.0+):** Built-in [Pi4EnableI2C](https://github.com/adamoutler/HassOSConfigurator/tree/main/Pi4EnableI2C) and [HassOsEnableSSH](https://github.com/adamoutler/HassOSConfigurator/tree/main/HassOsEnableSSH) configurators using the same `full_access` manifest as adamoutler's HassOSConfigurator add-ons. Reinstall when upgrading from 1.4.x.

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
