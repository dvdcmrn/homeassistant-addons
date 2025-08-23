# OLED System Monitor Add-on for Home Assistant

This add-on displays system information on an OLED display connected to your Home Assistant device via I2C.

## Features

- Support for SSD1306 and SH1106 OLED displays
- Customizable metrics (CPU, RAM, disk usage, temperature, uptime)
- Configurable display settings (contrast, rotation)
- Network information display
- Custom text support
- Visual bar graphs for usage metrics

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
| `width` | Display width in pixels | 128 |
| `height` | Display height in pixels | 64 |
| `rotate` | Display rotation (0, 1, 2, 3) | 0 |
| `contrast` | Display contrast (0-255) | 255 |

### System Options

| Option | Description | Default |
|--------|-------------|---------|
| `update_interval` | Update interval in seconds | 1 |
| `title` | Title to display | HEIMDALL |
| `show_title` | Whether to show the title | true |
| `show_temperature` | Whether to show temperature with title | true |

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

## Example Configurations

### Basic System Monitor
```yaml
display:
  type: "sh1106"
  i2c_address: "0x3C"
metrics:
  - type: "cpu"
    position: 1
  -
