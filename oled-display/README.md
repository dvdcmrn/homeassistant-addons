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

### Optional: Enable I2C automatically (Pi 4/5 / HA OS)

If you are running Home Assistant OS on a Raspberry Pi (Pi 4 or Pi 5) and I2C is not enabled, you can let the add-on attempt to enable I2C using enhanced functionality based on the [HassOSConfigurator](https://github.com/adamoutler/HassOSConfigurator/tree/main/Pi4EnableI2C) project by [adamoutler](https://github.com/adamoutler).

1. Edit the add-on configuration and set:

```yaml
system:
  enable_i2c: true
```

2. Start the add-on. It will perform comprehensive I2C enablement:
   - Scan for boot partitions (sda1, sdb1, mmcblk0p1, nvme0n1p1)
   - Add `dtparam=i2c_vc=on` and `dtparam=i2c_arm=on` to config.txt
   - Set up kernel module loading for both HASSOS and Raspbian
   - Load `i2c-dev` and `i2c-bcm2835` modules if possible

**Important Notes:**
- This may require up to **3 hard power-off reboots** (not just restarts) to take full effect
- **Why Multiple Reboots Are Needed:**
  1. **First Reboot**: Places I2C configuration files in the boot partition
  2. **Second Reboot**: Activates I2C hardware and loads kernel modules
  3. **Third Reboot** (sometimes needed): Ensures all I2C devices are properly initialized
- On some systems, protection mode must be disabled in Settings → System → Hardware
- This feature is off by default
- Check add-on logs after each reboot to see progress

**What to Expect During Each Restart:**
- **After 1st Restart**: Add-on will show "I2C devices already available" or continue with configuration
- **After 2nd Restart**: I2C hardware should be enabled, but device nodes may not be fully created yet
- **After 3rd Restart**: All I2C devices should be available at `/dev/i2c-*` and the OLED display should work

**Standalone I2C Enablement:**
If you need to enable I2C outside of the OLED add-on, you can use the standalone script in the [Pi5-I2C directory](../../Pi5-I2C/) which contains the complete implementation.

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
| `update_interval` | Update interval in seconds (recommend 5+ to minimize I2C/USB interference) | 1 |
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
   - Set `i2c_port` to a specific value instead of "auto"
   - Common values:
     - Raspberry Pi Zero: 0
     - Raspberry Pi 3/4: 1
     - Raspberry Pi 5 (GPIO I2C): 13 or 14 (try 13 first, then 14, then 1)
   - **Note for Pi 5**: Buses 0 and 1 are virtual adapters and may not work for hardware GPIO I2C. Use bus 13 or 14 for GPIO 2/3 connections.

4. **Verify hardware connections:**
   - Ensure proper wiring (VCC, GND, SCL, SDA)
   - Check that the display is powered correctly

### OLED Display Initialization Failed

If you see "ERROR: Failed to initialize display" but I2C devices are present:

1. **Check I2C device detection:**
   - The add-on will now automatically scan all I2C buses when initialization fails
   - Look for your display's I2C address (usually 0x3C) in the scan results

2. **Verify display type:**
   - Make sure you've selected the correct display type (ssd1306 or sh1106)
   - Most common displays are SH1106

3. **Check I2C address:**
   - Default is 0x3C, but some displays use 0x3D
   - Try both addresses if unsure

4. **Hardware troubleshooting:**
   - Ensure proper power supply (3.3V, not 5V)
   - Check for loose connections
   - Try a different I2C port (0, 1, 13, 14, etc.)
   - For Pi 5: Start with bus 13, then try 14, then 1

5. **Enable debug mode:**
   - Set `debug_mode: true` to run without the display and see system metrics

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
