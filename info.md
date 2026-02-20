# dvdcmrn Home Assistant Icons

Use Apple SF Symbols in Home Assistant with the `sf:` icon prefix.

**Install via HACS only.** Add this as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories/) in HACS, then install the integration.

After installation:
1. Add `dvdcmrn_icons:` to your `configuration.yaml`
2. Restart Home Assistant
3. Add SVG icons to `www/dvdcmrn_icons/icons/` (e.g. by using the export script on macOS and copying the files to your server)

Use icons in your dashboard with the `sf:` prefix: `icon: sf:house`, `sf:heart`, etc.
