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

### HAOS first-time setup (I2C + debug SSH)

From **1.5.0**, this add-on uses the same **`full_access: true`** / **`SYS_ADMIN`** manifest pattern as [adamoutler/HassOSConfigurator](https://github.com/adamoutler/HassOSConfigurator) ([Pi4EnableI2C](https://github.com/adamoutler/HassOSConfigurator/tree/main/Pi4EnableI2C), [HassOsEnableSSH](https://github.com/adamoutler/HassOSConfigurator/tree/main/HassOsEnableSSH)). It can mount HAOS boot partitions to enable GPIO I2C and debug SSH on port **22222**.

**After upgrading from 1.4.x:** uninstall the old add-on, reload the repository, install **1.5.0** fresh, then start it. A manifest-only update does not reset **`protected: true`** from older installs.

```yaml
system:
  enable_i2c: true          # writes dtparam=i2c_arm=on to boot config.txt
  enable_ssh: true          # optional: enable host debug SSH on port 22222
  ssh_public_key: "ssh-ed25519 AAAA... your-key"
display:
  type: "sh1106"
  i2c_address: "0x3C"
  i2c_port: "1"
```

1. Start the add-on and read the logs.
2. **Hard power-off reboot** 2–3 times (not just Restart in the UI).
3. Confirm I2C: `i2cdetect -y 1` on the **host** via `ssh root@thor -p 22222` (not the Terminal & SSH add-on shell).
4. When `0x3c` appears, the OLED should initialize on bus **1**.

Set **`enable_i2c: false`** and **`enable_ssh: false`** after the first successful setup if you prefer.

### Protection mode (Info tab, not the three-dot menu)

There is **no** global Settings → System → Hardware protection switch, and **no** protection option in the add-on three-dot menu.

Add-ons that declare **`full_access: true`** (this add-on from 1.5.0, HassOS I2C Configurator, HassOS SSH Configurator) install with **`protected: false`** automatically. On the add-on **Info** tab you may see **Protection mode** — it should already be **off**. If it is **on**, turn it **off** there, then restart the add-on.

Older 1.4.x installs used **`devices`** + **`gpio`** without **`full_access`**, stayed **`protected: true`**, and never showed that toggle. Reinstall 1.5.0 to pick up the new manifest.

**Security note:** `full_access` is rating **1** (same class as adamoutler configurators). Disable SSH/I2C configurators after first-run if you only need the display.

## Configuration

### Display Options

| Option | Description | Default |
|--------|-------------|---------|
| `type` | Display type (ssd1306 or sh1106) | sh1106 |
| `i2c_address` | I2C address of the display (usually 0x3C) | 0x3C |
| `i2c_port` | I2C port (`1` for Pi 3/4/5 GPIO header; see troubleshooting) | 1 |
| `width` | Display width in pixels | 128 |
| `height` | Display height in pixels | 64 |
| `rotate` | Display rotation (0, 1, 2, 3) | 0 |
| `contrast` | Display contrast (0-255) | 255 |

### System Options

| Option | Description | Default |
|--------|-------------|---------|
| `update_interval` | Update interval in seconds (recommend 5+ to minimize I2C/USB interference) | 5 |
| `title` | Title to display | home assistant |
| `show_title` | Whether to show the title | true |
| `show_temperature` | Whether to show temperature with title | true |
| `debug_mode` | Run in debug mode (console output only) | false |
| `enable_i2c` | Run Pi4EnableI2C-style boot configurator on start | true |
| `enable_ssh` | Run HassOsEnableSSH-style configurator (port 22222) | false |
| `ssh_public_key` | Full line from your `id_ed25519.pub` / `id_rsa.pub` | (empty) |

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

1. **Run the built-in configurators:**
   - Set `system.enable_i2c: true`, start the add-on, hard reboot 2–3 times
   - Check add-on logs for boot-partition mount errors; if present, open the add-on **Info** tab and turn **Protection mode** off

2. **Check available I2C devices:**
   - Set `debug_mode: true` in the configuration
   - Check the add-on logs to see what devices are available

3. **Manual I2C port configuration:**
   - Set `i2c_port` to a specific value instead of "auto"
   - Common values:
     - Raspberry Pi Zero: 0
     - Raspberry Pi 3/4/5 (40-pin GPIO SDA/SCL): **1**
   - **Pi 5 note:** Standard SH1106/SSD1306 modules wired to **GPIO2 (SDA)** and **GPIO3 (SCL)** use **`/dev/i2c-1`**. Buses **13** and **14** are different controllers; do not use them for header wiring. A full-grid scan on 13/14 is not trustworthy.

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
   - Check for loose connections (PoE HAT / case stacking often misaligns GPIO pins on Pi 5)
   - Confirm the display on the bus with host debug SSH: `i2cdetect -y 1` (port **22222**, not the SSH add-on shell)
   - Try address **0x3D** if the module has an address jumper
   - Run **HassOS I2C Configurator** once if boot I2C may not be enabled yet
   - Or use this add-on's **`system.enable_i2c: true`** (1.5.0+, requires fresh install with `full_access` manifest)

### Add-on protection (Info tab only)
   - Set `debug_mode: true` to run without the display and see system metrics

### Debug Mode

Enable debug mode to test the add-on without an OLED display:

```yaml
system:
  debug_mode: true
```

This will output all metrics to the console/logs instead of trying to use the OLED display.

## Example Configurations

### First boot on HAOS (I2C + SSH + display)
```yaml
system:
  enable_i2c: true
  enable_ssh: true
  ssh_public_key: "ssh-ed25519 AAAA... paste full public key line"
  update_interval: 5
display:
  type: "sh1106"
  i2c_address: "0x3C"
  i2c_port: "1"
metrics:
  - type: "cpu"
    position: 1
  - type: "memory"
    position: 2
  - type: "disk"
    position: 3
```

### Basic System Monitor (after I2C is enabled)
```yaml
system:
  enable_i2c: false
  enable_ssh: false
  update_interval: 5
display:
  type: "sh1106"
  i2c_address: "0x3C"
  i2c_port: "1"
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
