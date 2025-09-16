# OLED System Monitor Add-on (Home Assistant OS on Raspberry Pi 5)

This add-on displays system information on an OLED display connected to a Raspberry Pi 5 running Home Assistant OS, using the I2C interface. It targets RPi 5 (aarch64) exclusively.

## Features

- Support for SSD1306 and SH1106 OLED displays
- Customizable metrics (CPU, RAM, disk usage, temperature, uptime)
- Configurable display settings (contrast, rotation)
- Network information display
- Custom text support
- Visual bar graphs for usage metrics
- Automatic I2C device detection
- Debug mode for testing without OLED display

## Installation (Home Assistant OS, Raspberry Pi 5 only)

1. Add the custom repository to Home Assistant:
   - Settings → Add-ons → Add-on Store → ⋮ → Repositories → Add the repo URL → Add
2. Install the "OLED System Monitor" add-on from the store.
3. Enable I2C on the host:
   - Settings → System → Hardware → All hardware → ⋮ menu → Enable I2C → Reboot host.
   - After reboot, verify I2C is present: Settings → System → Hardware → look for `/dev/i2c-1`.
4. Start the add-on. If I2C is not yet present, the add-on will log metrics in debug mode until `/dev/i2c-1` is exposed by HA OS.

## Hardware Setup (RPi 5)

Connect your OLED display to the Raspberry Pi 5 header:
- VCC → 3.3V
- GND → Ground
- SCL → GPIO 3 (SCL)
- SDA → GPIO 2 (SDA)

Ensure I2C is enabled in Home Assistant OS (see Installation step 3).

## Configuration (single-page)

The add-on presents simple, descriptive settings. Legacy nested options remain supported for compatibility.

Key settings:

- `display_type` (ssd1306|sh1106): Your OLED controller type. Most 128x64 modules are sh1106 or ssd1306.
- `i2c_address`: Hex address of your display. Commonly `0x3C`.
- `i2c_port`: I2C bus number. Use `auto` for RPi 5 (usually `1`).
- `width`, `height`: Pixel dimensions. Common modules are 128x64.
- `rotate`: 0,1,2,3 to rotate display if oriented differently.
- `contrast`: 0–255 brightness level.
- `update_interval`: Seconds between screen updates.
- `title`, `show_title`, `show_temperature`: Header line controls.
- `show_cpu`, `show_memory`, `show_disk`, `show_temperature_metric`, `show_uptime`: Toggle metrics. `disk_mount_point` for disk metric path.
- `custom_text_enabled`, `custom_text`, `custom_text_position`: Optional custom line.
- `show_ip`, `network_interface`, `network_label`, `network_position`: IP address line.

## Troubleshooting (HA OS on RPi 5)

### I2C device not found

1) Ensure I2C is enabled: Settings → System → Hardware → All hardware → ⋮ → Enable I2C → Reboot host.

2) After reboot, confirm `/dev/i2c-1` is listed under hardware in HA.

3) Wiring: VCC→3.3V, GND→GND, SCL→GPIO3 (SCL), SDA→GPIO2 (SDA).

4) Set `i2c_port: "1"` if auto-detection fails.

If I2C is missing at startup, the add-on now falls back to debug mode and prints metrics in logs until I2C becomes available.

### Enable I2C via Home Assistant Operating System terminal

Alternatively, by attaching a keyboard and screen to your device, you can access the physical terminal to the Home Assistant Operating System.

You can enable I2C via this terminal (from Home Assistant docs):

1. Login as root.
2. Type `login` and press enter to access the shell.
3. Type the following to enable I2C, you may need to replace `sda1` with `sdb1` or `mmcblk0p1` depending on your platform:

```
mkdir /tmp/mnt
mount /dev/sda1 /tmp/mnt
mkdir -p /tmp/mnt/modules
echo -ne i2c-dev>/tmp/mnt/modules/rpi-i2c.conf
echo dtparam=i2c_vc=on >> /tmp/mnt/config.txt
echo dtparam=i2c_arm=on >> /tmp/mnt/config.txt
sync
reboot
```

Source: Home Assistant OS Common Tasks (`https://www.home-assistant.io/common-tasks/os/`).

### Debug mode

Set `debug_mode: true` to run without the OLED. This is automatic if initialization fails.

## Example configurations

### Minimal (defaults)
```yaml
display_type: "sh1106"
i2c_address: "0x3C"
i2c_port: "auto"
```

### Customized layout
```yaml
title: "Home Assistant"
show_title: true
show_temperature: true
show_cpu: true
show_memory: true
show_disk: true
disk_mount_point: "/"
show_temperature_metric: false
show_uptime: true
custom_text_enabled: true
custom_text: "Welcome"
custom_text_position: 4
show_ip: true
network_interface: "eth0"
network_label: "IP"
```

## Changelog

See the [CHANGELOG](./CHANGELOG.md) for release notes.
