# Cupertino Icons

Use Apple SF Symbols in Home Assistant with the `sf:` icon prefix. The integration ships **no symbols** — you export the SVGs you want.

**Install via HACS only.** Add this as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories/) in HACS, then install the integration.

After installation:

1. Add `cupertino_icons:` to your `configuration.yaml` and restart.
2. Export symbols from the SF Symbols Mac app with **File → Export Image…** (SVG), **not** File → Export Symbol…
3. Copy files such as `homepod.fill.svg` into `www/cupertino-icons/` on your Home Assistant host.
4. Call `cupertino_icons.refresh_icons` (or restart) and hard-reload the browser.

Use in dashboards: `icon: sf:homepod-fill`.
