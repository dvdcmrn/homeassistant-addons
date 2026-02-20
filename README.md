# dvdcmrn Home Assistant Icons

Use Apple SF Symbols in your Home Assistant dashboards with the `sf:` icon prefix. This integration is installed **only via HACS** (Home Assistant Community Store).

## Installation (HACS only)

1. Open **HACS** in Home Assistant.
2. Go to **Integrations** and click the three dots (top right), then **Custom repositories**.
3. Add this repository URL: `https://github.com/dvdcmrn/homeassistant-icons`
4. Choose category **Integration** and click **Add**.
5. Search for **dvdcmrn Home Assistant Icons** in HACS and click **Download**.
6. Restart Home Assistant.

## Configuration

Add to your `configuration.yaml`:

```yaml
dvdcmrn_icons:
```

Restart Home Assistant again. The integration will create `www/dvdcmrn_icons/icons/` in your config directory.

## Adding icons

Icons are SVG files in `www/dvdcmrn_icons/icons/`. You can add them in two ways:

- **Export on macOS:** Use the script in this repo (requires SF Symbols app and Python). Run it, then copy the exported SVGs to `www/dvdcmrn_icons/icons/` on your Home Assistant host (e.g. via Samba, SSH, or the file editor add-on).
- **Manual:** Export SVGs from the [SF Symbols app](https://developer.apple.com/sf-symbols/) (Copy as SVG) and save into `www/dvdcmrn_icons/icons/` with the symbol name as filename (e.g. `house.svg`).

After adding or changing icons, call the service `dvdcmrn_icons.refresh_icons` or restart Home Assistant.

## Usage

Use the `sf:` prefix in your dashboards:

```yaml
icon: sf:house
```

Example card:

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

## Export script (optional, macOS)

If you have a Mac with the SF Symbols app and want to batch-export SVGs from this repo:

```bash
git clone https://github.com/dvdcmrn/homeassistant-icons.git
cd homeassistant-icons
python3 scripts/export_sf_symbols.py --interactive --output ~/exported_icons
# Copy ~/exported_icons/*.svg to your HA www/dvdcmrn_icons/icons/
```

Other commands: `--symbols house heart star`, `--list`, `--output /path`.

## Services

- **dvdcmrn_icons.refresh_icons** – Refresh the list of available icons after adding new files.

## Troubleshooting

- **Icons not showing:** Ensure SVGs are in `www/dvdcmrn_icons/icons/`, filenames match the icon name (e.g. `house.svg` for `sf:house`), then call `dvdcmrn_icons.refresh_icons` or restart.
- **Export script:** Needs SF Symbols app and AppleScript permissions; use `--interactive` for step-by-step.

## Repository structure

```
custom_components/dvdcmrn_icons/   # Integration (installed by HACS)
scripts/export_sf_symbols.py      # Optional macOS export script
docs/                              # Extra docs
```

## License and disclaimer

For personal use. SF Symbols are copyright Apple Inc.; this project is not affiliated with Apple.

## Support

Open an issue on GitHub with your setup details if something does not work.
