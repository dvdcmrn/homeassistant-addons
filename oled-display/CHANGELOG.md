# Changelog

All notable changes to the "OLED System Monitor" Home Assistant add-on are documented in this file.

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

## 1.0.0
- Initial public release