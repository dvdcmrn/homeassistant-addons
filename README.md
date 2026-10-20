# Home Assistant (dvdcmrn)

One repository for David Cameron's Home Assistant add-ons, HACS integrations, themes, and related tooling.

- **Repository URL (after rename):** https://github.com/dvdcmrn/homeassistant
- **Current URL:** https://github.com/dvdcmrn/homeassistant-addons
- **Maintainer:** [dvdcmrn](https://github.com/dvdcmrn)

## Contents

| Path | Purpose |
| --- | --- |
| `repository.yaml` | Home Assistant Supervisor add-on store index |
| `addons/oled_display/` | OLED System Monitor add-on |
| `hacs.json` | HACS metadata for the Cupertino Icons integration |
| `custom_components/cupertino_icons/` | SF Symbols (`sf:`) icon integration (HACS) |
| `brand/` | Integration brand assets (`icon.png`) for HACS / home-assistant/brands |
| `themes/` | YAML themes (manual install; not a HACS theme repo) |
| `icons/` | Optional reference SVGs (no Apple symbol artwork shipped) |
| `scripts/` | Development and HAOS helper scripts |
| `tests/` | Python tests for Cupertino Icons |

---

## Add-on store (Supervisor)

1. Open **Settings** → **Add-ons** → **Add-on store**.
2. Open the menu (top right) → **Repositories**.
3. Add: `https://github.com/dvdcmrn/homeassistant` (or `homeassistant-addons` until the repo is renamed).
4. Install **OLED System Monitor** from the store.

Details: [addons/oled_display/README.md](./addons/oled_display/README.md)

---

## HACS: Cupertino Icons (integration)

This repo is a **custom HACS integration** repository. Themes are **not** installed through HACS from this repo (HACS does not support integration + theme in one repo).

1. Open **HACS** → **Integrations** → menu → **Custom repositories**.
2. Add the repository URL and category **Integration**.
3. Search for **Cupertino Icons**, download, and restart Home Assistant.
4. Add to `configuration.yaml`:

```yaml
cupertino_icons:
```

5. Export symbols on a Mac with [SF Symbols](https://developer.apple.com/sf-symbols/) using **File → Export Image…** (SVG), not **Export Symbol…**.
6. Copy SVGs into `www/cupertino-icons/` on your Home Assistant host.
7. Call `cupertino_icons.refresh_icons` or restart, then hard-reload the browser.

Dashboard example:

```yaml
icon: sf:homepod-fill
```

Validate exports locally:

```bash
python3 scripts/validate_sf_icons.py /path/to/exported/icons
```

On macOS you can batch-export with `python3 scripts/export_sf_symbols.py` (see script help); prefer **File → Export Image…** in SF Symbols when AppleScript export is unreliable.

More detail: [info.md](./info.md) and the Cupertino Icons section in this README's history in `docs/SETUP.md`.

---

## Themes (manual install)

HACS theme repositories must be separate from integrations. Copy files from `themes/` into your config:

1. Ensure `configuration.yaml` includes:

```yaml
frontend:
  themes: !include_dir_merge_named themes
```

2. Copy desired `themes/*.yaml` to `/config/themes/` on your Home Assistant host.
3. **Developer Tools** → **Services** → call `frontend.reload_themes`.
4. Select the theme under **Profile** → **Theme**.

Included themes (from **hass-themes** and live HA export):

| File | Description |
| --- | --- |
| `dvdcmrn-theme.yaml` | GitHub-inspired palette |
| `dvdcmrn-dracula.yaml` | Dracula-style variant |
| `dvdcmrn-dark-highcontrast.yaml` | High-contrast dark (card-mod / Mushroom friendly) |

See [themes/README.md](./themes/README.md) for details.

Optional Mac export helper: `scripts/export_sf_symbols.py` (copy output to `www/cupertino-icons/`). Reference SVG: [icons/playstation.logo.svg](./icons/playstation.logo.svg) from legacy **pinnacles**.

---

## Development

```bash
python3 scripts/setup_dev.py
source venv/bin/activate
pytest tests/ -v
```

CI runs lint, typecheck, and tests on push/PR. See [AGENTS.md](./AGENTS.md) for agent notes.

---

## License and disclaimer

Add-ons and integration code are licensed as described in [LICENSE](./LICENSE). Cupertino Icons does **not** ship SF Symbols artwork. SF Symbols are copyright Apple Inc. This project is not affiliated with Apple.

## Support

Open an issue at https://github.com/dvdcmrn/homeassistant/issues (after rename) or on the current repository URL.
