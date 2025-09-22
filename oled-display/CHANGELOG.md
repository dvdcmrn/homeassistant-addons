# Changelog

All notable changes to the "OLED System Monitor" Home Assistant add-on are documented in this file.

## 1.3.3 - 2025-01-27
- Add comprehensive I2C diagnostics and troubleshooting
- Enhanced error reporting with detailed exception information
- Automatic I2C bus scanning when display initialization fails
- Improved troubleshooting documentation and tips
- Better hardware connection verification guidance

## 1.0.1 - 2025-09-15
- Bump add-on version so Home Assistant surfaces the update
- Add changelog and link from README
- Minor documentation improvements

## 1.0.2 - 2025-09-15
- Change default system title to "home assistant"
- Update README default value table

## 1.2.1 - 2025-09-15
- Version bump only; no functional changes

## 1.3.0 - 2025-09-15
- Add optional I2C enablement (Pi 4 / HA OS) via `system.enable_i2c`
- New script `enable_i2c.sh` and integration at service startup
- Documentation updates with safety notes

## 1.3.1 - 2025-09-15
- Skip I2C enablement if /dev/i2c-* devices already exist
- Prefer bus 1 during auto-detection

## 1.3.2 - 2025-01-27
- **Enhanced I2C enablement** based on [HassOSConfigurator](https://github.com/adamoutler/HassOSConfigurator/tree/main/Pi4EnableI2C) by adamoutler
- Comprehensive boot partition scanning (sda1, sdb1, mmcblk0p1, nvme0n1p1)
- Support for both `dtparam=i2c_vc=on` and `dtparam=i2c_arm=on` configuration
- Enhanced Raspbian support with i2c-bcm2708 module loading
- Improved error handling and protection mode detection
- Added standalone [Pi4EnableI2C directory](../../Pi4EnableI2C/) for manual I2C setup
- Updated documentation with proper attribution and detailed instructions

## 1.0.0
- Initial public release