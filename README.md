# Cupertino Icons

Use Apple SF Symbols in Home Assistant dashboards with the `sf:` icon prefix. This integration is installed **only via HACS**. It ships **no symbols**. You export the ones you want on a Mac and copy the SVGs onto your Home Assistant host.

## Installation (HACS only)

1. Open **HACS** in Home Assistant.
2. Go to **Integrations** and click the three dots (top right), then **Custom repositories**.
3. Add this repository URL: `https://github.com/dvdcmrn/homeassistant-icons`
4. Choose category **Integration** and click **Add**.
5. Search for **Cupertino Icons** in HACS and click **Download**.
6. Restart Home Assistant.

## Configuration

Add to your `configuration.yaml`:

```yaml
cupertino_icons:
```

Restart Home Assistant again. The integration creates an empty `www/cupertino-icons/` folder in your config directory (plus a short `README.txt` that is not an icon).

## Exporting icons from SF Symbols

Install [SF Symbols](https://developer.apple.com/sf-symbols/) on a Mac.

**Use File → Export Image…, not File → Export Symbol…**

Export Symbol (`⇧⌘E`) writes an Xcode template (multiple weights and guides). Those files will not render as dashboard icons.

1. Open SF Symbols and select a symbol, for example `homepod.fill`.
2. Set the weight to **Regular** (or the weight you want).
3. Choose **File → Export Image…**
4. Format: **SVG**. Save as `homepod.fill.svg` (keep Apple's dotted name).
5. Copy the file to `www/cupertino-icons/` on your Home Assistant host (Samba, SSH, or the File Editor add-on).
6. Call **Developer Tools → Services → `cupertino_icons.refresh_icons`** (or restart Home Assistant), then hard-reload the browser.

Optional: right-click the symbol → **Copy Image as SVG**, paste into a file named `homepod.fill.svg`.

On a Mac you can check files before copying:

```bash
python3 scripts/validate_sf_icons.py ~/exported_icons
```

Usable files print as `OK  homepod.fill.svg  ->  sf:homepod-fill`. Templates and broken SVGs print `FAIL`.

## Naming

| File on disk | Dashboard icon |
| --- | --- |
| `homepod.fill.svg` | `sf:homepod-fill` |
| `house.svg` | `sf:house` |
| `homepod-fill.svg` | `sf:homepod-fill` (fallback if the dotted name is absent) |

Dots in the Apple symbol name become hyphens after `sf:`. Prefer the dotted filename.

## Usage

```yaml
icon: sf:homepod-fill
```

Example card:

```yaml
type: entities
entities:
  - entity: media_player.living_room_homepod
    icon: sf:homepod-fill
    name: HomePod
  - entity: light.living_room
    icon: sf:house
    name: Living Room
```

The HA icon picker lists whatever you have exported. Icons follow the active theme color.

## Services

- **cupertino_icons.refresh_icons** – Rescan `www/cupertino-icons` after adding or replacing files.

## Troubleshooting

- **Icons not showing:** Confirm the SVG is in `www/cupertino-icons/`, the name mapping above, then `cupertino_icons.refresh_icons` or restart, then hard-reload the browser.
- **Blank icon:** You probably exported a **symbol template**. Re-export with **File → Export Image…** as SVG.
- **Validator:** `python3 scripts/validate_sf_icons.py /path/to/cupertino-icons`

## License and disclaimer

For personal use. This repository does not include SF Symbols artwork. SF Symbols are copyright Apple Inc. This project is not affiliated with Apple.

## Support

Open an issue on GitHub with your setup details if something does not work.
