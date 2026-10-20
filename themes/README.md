# Themes

These YAML files are for **manual** installation. This repository cannot publish themes through HACS while it also hosts the Cupertino Icons integration.

## Install

1. Add to `configuration.yaml`:

```yaml
frontend:
  themes: !include_dir_merge_named themes
```

2. Copy the `.yaml` files you want into `/config/themes/` on your Home Assistant host.
3. Run the `frontend.reload_themes` service (Developer Tools → Services).
4. Choose the theme under your user profile.

## Included themes

| File | Description |
| --- | --- |
| `dvdcmrn-dark-highcontrast.yaml` | High-contrast dark theme (black base, Dracula-inspired palette accents). Supports card-mod and Mushroom. |

Additional themes from the legacy `hass-themes` repository were not copied in this consolidation (private repo was not accessible to the automation token). Add `dvdcmrn-theme.yaml` and `dvdcmrn-dracula.yaml` here manually if you still need them, and review screenshots before publishing.
