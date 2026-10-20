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
| `dvdcmrn-theme.yaml` | GitHub-inspired light/dark palette (from legacy **hass-themes**). |
| `dvdcmrn-dracula.yaml` | Dracula palette variant with card-mod hooks (from legacy **hass-themes**). |
| `dvdcmrn-dark-highcontrast.yaml` | High-contrast dark theme (black base, palette accents). Supports card-mod and Mushroom. |

Theme YAML was reviewed for secrets and hostnames before publish. README screenshots from **hass-themes** were not included; add your own previews if you document themes publicly.
