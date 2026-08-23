# Cupertino Icons - Development Setup

This integration is distributed **only via HACS**; end users do not install it manually. This guide is for developers working on the repo.

## 1. Project Structure

```
homeassistant-icons/
├── custom_components/
│   └── cupertino_icons/
│       ├── __init__.py
│       ├── icon_manager.py
│       ├── iconset.js
│       ├── manifest.json
│       └── services.yaml
├── docs/
│   ├── SETUP.md
│   └── PROJECT_SETUP.md
├── scripts/
│   └── validate_sf_icons.py
├── tests/
│   └── fixtures/
├── hacs.json
├── info.md
├── README.md
└── requirements.txt
```

User-exported SVGs live on the Home Assistant host in `config/www/cupertino-icons/`, not in this repository.

## 2. Local tests

```bash
cd homeassistant-icons
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
```

On a machine without Home Assistant installed, `tests/conftest.py` stubs the HA imports so icon-manager tests still run.

## 3. How icons are registered

1. `async_setup` creates `www/cupertino-icons/` and registers `/cupertino-icons/iconset.js` on `frontend_extra_module_url`.
2. `iconset.js` sets `window.customIcons["sf"]`.
3. The frontend fetches `/cupertino-icons/list` and `/cupertino-icons/icon/<name>`.
4. `homepod.fill.svg` is served as `sf:homepod-fill`. Xcode symbol templates are rejected.

## 4. Validating exports

```bash
python3 scripts/validate_sf_icons.py /path/to/exported_svgs
```

Use **File → Export Image…** (SVG) from SF Symbols. Do not use **File → Export Symbol…**.

## 5. Manifest

`custom_components/cupertino_icons/manifest.json` must include `issue_tracker` and other HACS-required keys. `iot_class` is `calculated` (no device polling).
