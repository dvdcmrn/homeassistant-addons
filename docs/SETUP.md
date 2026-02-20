# dvdcmrn Home Assistant Icons – Setup

This integration is installed **only via HACS**. Manual installation is not supported.

## Prerequisites

- Home Assistant with [HACS](https://hacs.xyz/) installed
- For exporting icons on macOS: SF Symbols app and Python 3.9+

## Installation via HACS

1. In Home Assistant, open **HACS** → **Integrations**.
2. Click the three dots (top right) → **Custom repositories**.
3. Add repository URL: `https://github.com/dvdcmrn/homeassistant-icons`
4. Category: **Integration** → **Add**.
5. Search for **dvdcmrn Home Assistant Icons** and click **Download**.
6. Restart Home Assistant.

## Configuration

Add to `configuration.yaml`:

```yaml
dvdcmrn_icons:
```

Restart Home Assistant. The integration creates `www/dvdcmrn_icons/icons/` in your config directory.

## Adding icons

Put SVG files in `www/dvdcmrn_icons/icons/` on your Home Assistant server. File name = icon name (e.g. `house.svg` for `sf:house`).

**Option A – Export script (macOS)**  
Clone this repo, run `python3 scripts/export_sf_symbols.py --interactive --output ~/exported_icons`, then copy the generated SVGs to `www/dvdcmrn_icons/icons/` (Samba, SSH, File editor, etc.).

**Option B – Manual**  
In the SF Symbols app, copy a symbol as SVG and save it into `www/dvdcmrn_icons/icons/` with the correct name.

After adding icons, call **dvdcmrn_icons.refresh_icons** or restart Home Assistant.

## Usage

Use the `sf:` prefix in dashboards:

```yaml
type: button
entity: light.living_room
icon: sf:house
```

Example:

```yaml
type: entities
entities:
  - entity: light.living_room
    icon: sf:house
    name: Living Room
  - entity: sensor.temperature
    icon: sf:thermometer
    name: Temperature
  - entity: switch.fan
    icon: sf:wind
    name: Fan
```

## Services

- **dvdcmrn_icons.refresh_icons** – Refresh the list of available icons.

## Troubleshooting

- Icons not showing: Check `www/dvdcmrn_icons/icons/`, file names (e.g. `house.svg`), then `dvdcmrn_icons.refresh_icons` or restart.
- Export script: Requires SF Symbols app and AppleScript; use `--interactive` for debugging.

SF Symbols are copyright Apple Inc. This integration is for personal use and is not affiliated with Apple.
