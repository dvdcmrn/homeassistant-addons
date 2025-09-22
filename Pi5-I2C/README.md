# Pi5-I2C - Raspberry Pi I2C Enablement

This directory contains enhanced I2C enablement functionality for Raspberry Pi devices (including Pi 4 and Pi 5) running Home Assistant OS, based on the [HassOSConfigurator](https://github.com/adamoutler/HassOSConfigurator/tree/main/Pi4EnableI2C) project by [adamoutler](https://github.com/adamoutler).

## Purpose

The `run.sh` script in this directory provides comprehensive I2C enablement for Raspberry Pi devices (including Pi 4 and Pi 5), including:

- Automatic detection of boot partitions (sda1, sdb1, mmcblk0p1, nvme0n1p1)
- Configuration of both I2C VC and I2C ARM interfaces
- Support for both Home Assistant OS and Raspbian systems
- Proper module loading for I2C functionality
- Enhanced error handling and logging

## Usage

### As a Standalone Script

You can run this script directly on your Home Assistant OS system:

```bash
# Make executable and run
chmod +x run.sh
./run.sh
```

### Integration with OLED System Monitor

This functionality is automatically integrated into the OLED System Monitor add-on. To use it:

1. Install the OLED System Monitor add-on from this repository
2. Set `system.enable_i2c: true` in the add-on configuration
3. Start the add-on - it will automatically attempt I2C enablement

## What It Does

The script performs the following operations:

1. **Checks for existing I2C devices** - If I2C is already enabled, exits gracefully
2. **Scans for boot partitions** - Looks for common partition names where config.txt might be located
3. **Mounts partitions** - Temporarily mounts boot partitions to access configuration files
4. **Configures I2C parameters** - Adds the following to config.txt:
   - `dtparam=i2c_vc=on` - Enables I2C on the VideoCore
   - `dtparam=i2c_arm=on` - Enables I2C on the ARM processor
5. **Sets up kernel modules** - Creates module configuration files for automatic loading
6. **Provides clear instructions** - Tells you when a reboot is required

## Important Notes

⚠️ **Reboot Required**: After running this script, you must perform a **hard power-off reboot** for the changes to take effect.

⚠️ **Protection Mode**: This script cannot run if Home Assistant OS protection mode is enabled. Disable protection mode in the Info screen before running.

⚠️ **Multiple Reboots Required**: You may need to reboot up to 3 times for full I2C enablement:

**Why Multiple Reboots Are Needed:**
1. **First Reboot**: Places the configuration files (`dtparam=i2c_vc=on` and `dtparam=i2c_arm=on`) into the boot partition's `config.txt`
2. **Second Reboot**: Activates the I2C interfaces at the hardware level and loads the I2C kernel modules
3. **Third Reboot** (sometimes needed): Ensures all I2C devices are properly initialized and available at `/dev/i2c-*`

**What Happens During Each Restart:**
- **Restart 1**: The script writes I2C configuration to the boot partition, but the running system doesn't see these changes yet
- **Restart 2**: The bootloader reads the new configuration and enables I2C hardware, but device nodes may not be fully created
- **Restart 3**: Final initialization ensures all I2C device nodes are properly created and accessible

This multi-reboot process is necessary because Home Assistant OS uses a read-only filesystem and requires hardware-level changes to be applied during the boot process.

## Troubleshooting

### Protection Mode Error
```
Detected Protection Mode is enabled. Disable Protection Mode in Info Screen.
```
**Solution**: Go to Settings → System → Hardware and disable Protection Mode.

### No Partitions Found
```
No boot partitions found. Protection mode may be enabled?
```
**Solution**: Ensure protection mode is disabled and try again.

### I2C Still Not Working After Reboot
1. Verify the configuration was written to config.txt
2. Try a hard power-off (not just a restart)
3. Check that your hardware connections are correct
4. Ensure your OLED display is compatible (SSD1306/SH1106)

## Source Attribution

This implementation is based on the excellent work in the [HassOSConfigurator](https://github.com/adamoutler/HassOSConfigurator) repository by [adamoutler](https://github.com/adamoutler). The original implementation can be found in the [Pi4EnableI2C directory](https://github.com/adamoutler/HassOSConfigurator/tree/main/Pi4EnableI2C).

## Integration

This functionality is integrated into the OLED System Monitor add-on and can be enabled by setting:

```yaml
system:
  enable_i2c: true
```

For more information about the OLED System Monitor add-on, see the main [README](../README.md).
