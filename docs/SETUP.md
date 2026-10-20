# Cupertino Icons – Setup

This integration is installed **only via HACS**. Manual installation is not supported. It ships no SF Symbols; you export the SVGs you want.

## Prerequisites

- Home Assistant with [HACS](https://hacs.xyz/) installed
- For exporting icons: a Mac with the [SF Symbols](https://developer.apple.com/sf-symbols/) app

## Installation via HACS

1. In Home Assistant, open **HACS** → **Integrations**.
2. Click the three dots (top right) → **Custom repositories**.
3. Add repository URL: `https://github.com/dvdcmrn/homeassistant`
4. Category: **Integration** → **Add**.
5. Search for **Cupertino Icons** and click **Download**.
6. Restart Home Assistant.

## Configuration

Add to `configuration.yaml`:

```yaml
cupertino_icons:
```

Restart Home Assistant. The integration creates an empty `www/cupertino-icons/` folder in your config directory.

## Exporting icons

**Use File → Export Image…, not File → Export Symbol…**

Export Symbol writes an Xcode template and will not render in dashboards.

1. Open SF Symbols and select a symbol (for example `homepod.fill`).
2. Set weight to **Regular** (or the weight you want).
3. **File → Export Image…** → format **SVG**.
4. Keep Apple's dotted filename: `homepod.fill.svg`.
5. Copy the file to `www/cupertino-icons/` on the Home Assistant host (Samba, SSH, or File Editor).
6. Call **cupertino_icons.refresh_icons** or restart, then hard-reload the browser.

Optional: right-click → **Copy Image as SVG**, paste into `homepod.fill.svg`.

On a Mac, validate before copying:

```bash
python3 scripts/validate_sf_icons.py ~/exported_icons
```

## Naming

`homepod.fill.svg` is used as `icon: sf:homepod-fill`. Dots become hyphens. A hyphenated filename is accepted if the dotted file is missing.

## Usage

```yaml
type: button
entity: media_player.living_room_homepod
icon: sf:homepod-fill
```

## Services

- **cupertino_icons.refresh_icons** – Rescan `www/cupertino-icons` after adding files.

## Troubleshooting

- Icons not showing: check `www/cupertino-icons/`, filenames, then refresh/restart and hard-reload.
- Blank icon: re-export with **File → Export Image…** (SVG), not Export Symbol.

SF Symbols are copyright Apple Inc. This integration is for personal use and is not affiliated with Apple.
