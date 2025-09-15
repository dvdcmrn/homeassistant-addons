# OLED System Monitor Add-on for Home Assistant

This add-on displays system information on an OLED display connected to your Home Assistant device via I2C.

## Features

- Support for SSD1306 and SH1106 OLED displays
- Customizable metrics (CPU, RAM, disk usage, temperature, uptime)
- Configurable display settings (contrast, rotation)
- Network information display
- Custom text support
- Visual bar graphs for usage metrics
- Automatic I2C device detection
- Debug mode for testing without OLED display

## Installation

1. Add this repository to your Home Assistant instance
2. Install the "OLED System Monitor" add-on
3. Configure the add-on with your display settings
4. Start the add-on

## Hardware Setup

Connect your OLED display to the Raspberry Pi:
- VCC → 3.3V
- GND → Ground
- SCL → GPIO 3 (SCL)
- SDA → GPIO 2 (SDA)

Make sure I2C is enabled on your Home Assistant device.

## Configuration

### Display Options

| Option | Description | Default |
|--------|-------------|---------|
| `type` | Display type (ssd1306 or sh1106) | sh1106 |
| `i2c_address` | I2C address of the display (usually 0x3C) | 0x3C |
| `i2c_port` | I2C port (auto, 0, 1, etc.) | auto |
| `width` | Display width in pixels | 128 |
| `height` | Display height in pixels | 64 |
| `rotate` | Display rotation (0, 1, 2, 3) | 0 |
| `contrast` | Display contrast (0-255) | 255 |

### System Options

| Option | Description | Default |
|--------|-------------|---------|
| `update_interval` | Update interval in seconds | 1 |
| `title` | Title to display | home assistant |
| `show_title` | Whether to show the title | true |
| `show_temperature` | Whether to show temperature with title | true |
| `debug_mode` | Run in debug mode (console output only) | false |

### Metrics

You can configure multiple metrics to display. Each metric has:

| Option | Description | Default |
|--------|-------------|---------|
| `type` | Metric type (cpu, memory, disk, temperature, uptime) | - |
| `position` | Display position (1-10) | - |
| `show_bar` | Whether to show a bar graph | true |
| `label` | Custom label for the metric | (metric type) |
| `mount_point` | Mount point for disk metrics | / |

### Custom Text

| Option | Description | Default |
|--------|-------------|---------|
| `enabled` | Whether to show custom text | false |
| `position` | Display position | 4 |
| `text` | Text to display | Home Assistant |

### Network Options

| Option | Description | Default |
|--------|-------------|---------|
| `show_ip` | Whether to show IP address | false |
| `position` | Display position | 5 |
| `interface` | Network interface to use | eth0 |
| `label` | Label for IP address | IP |

## Troubleshooting

### I2C Device Not Found

If you get an error like `DeviceNotFoundError: I2C device not found: /dev/i2c-1`, try these steps:

1. **Enable I2C in Home Assistant:**
   - Go to Settings → System → Hardware
   - Enable I2C interface

2. **Check available I2C devices:**
   - Set `debug_mode: true` in the configuration
   - Check the add-on logs to see what devices are available

3. **Manual I2C port configuration:**
   - Set `i2c_port` to a specific value (0, 1, etc.) instead of "auto"
   - Common values: 0 for Raspberry Pi Zero, 1 for Raspberry Pi 3/4

4. **Verify hardware connections:**
   - Ensure proper wiring (VCC, GND, SCL, SDA)
   - Check that the display is powered correctly

### Debug Mode

Enable debug mode to test the add-on without an OLED display:

```yaml
system:
  debug_mode: true
```

This will output all metrics to the console/logs instead of trying to use the OLED display.

## Example Configurations

### Basic System Monitor
```yaml
display:
  type: "sh1106"
  i2c_address: "0x3C"
  i2c_port: "auto"
metrics:
  - type: "cpu"
    position: 1
  - type: "memory"
    position: 2
  - type: "disk"
    position: 3
```

### Debug Mode for Testing
```yaml
system:
  debug_mode: true
  update_interval: 5
display:
  i2c_port: "auto"
metrics:
  - type: "cpu"
    position: 1
  - type: "memory"
    position: 2
  - type: "temperature"
    position: 3
```

## Changelog

See the [CHANGELOG](./CHANGELOG.md) for release notes.
