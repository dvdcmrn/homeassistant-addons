# Changelog

All notable changes to the "OLED System Monitor" Home Assistant add-on are documented in this file.

## 1.0.1 - 2025-09-15
- Bump add-on version so Home Assistant surfaces the update
- Add changelog and link from README
- Minor documentation improvements

## 1.0.2 - 2025-09-15
- Change default system title to "home assistant"
- Update README default value table

## 1.2.0 - 2025-09-15
- Limit add-on to Raspberry Pi 5 (aarch64) on Home Assistant OS
- Flatten configuration to single-page options with labels/descriptions
- Add automatic debug-mode fallback when I2C/OLED init fails
- Slim Docker image dependencies for HA OS base
- Update README for HA OS on RPi 5 only

### Internal
- Migrate base image to `ghcr.io/home-assistant/aarch64-addon-base:3.18`

## 1.0.0
- Initial public release