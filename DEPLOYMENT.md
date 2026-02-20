# Deployment Guide

This integration is distributed **only via HACS**. Users install it by adding this repo as a custom repository in HACS.

## GitHub repository

- Repository must be **public** on GitHub.
- Set a short **description** and **topics** (e.g. `home-assistant`, `hacs`, `icons`, `sf-symbols`) for discoverability.
- Ensure the default branch (e.g. `main`) contains the integration under `custom_components/dvdcmrn_icons/`.

## HACS requirements (already in repo)

- **hacs.json** in the repo root (defines display name; `render_readme: true` uses README in HACS).
- **info.md** in the repo root (optional; shown in HACS under the description).
- **manifest.json** in `custom_components/dvdcmrn_icons/` with at least: `version`, `name`, `domain`, `documentation`, `issue_tracker`, `codeowners`.

## Adding as a custom repository

Users add this repository in HACS:

1. HACS → Integrations → three dots → Custom repositories.
2. URL: `https://github.com/dvdcmrn/homeassistant-icons`
3. Category: Integration → Add.
4. Search for "dvdcmrn Home Assistant Icons" and download.

To appear in the **default HACS store** (no custom repo needed), the integration must be submitted and accepted (see [HACS include process](https://hacs.dev/docs/publish/include/) and [home-assistant/brands](https://github.com/home-assistant/brands) for UI compliance).

## Releases (optional)

Publishing GitHub releases is optional but recommended so users can choose a version in HACS:

1. Update `version` in `custom_components/dvdcmrn_icons/manifest.json`.
2. Create a tag and release:
   ```bash
   git tag -a v1.0.1 -m "Release 1.0.1"
   git push origin v1.0.1
   ```
3. On GitHub: Releases → Create new release → choose the tag, add notes.

Without releases, HACS uses the default branch.

## Development workflow

```bash
# Setup
python3 scripts/setup_dev.py
source venv/bin/activate

# Test
pytest tests/ -v

# Before release: bump version in manifest.json, then tag and push.
```

## Pre-release checklist

- [ ] Tests pass (`pytest tests/`)
- [ ] Version in `manifest.json` updated
- [ ] README and info.md accurate
- [ ] No manual install instructions (HACS only)
