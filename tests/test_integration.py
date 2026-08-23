"""Tests for YAML setup wiring."""

from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

from custom_components.cupertino_icons import (
    DATA_EXTRA_MODULE_URL,
    DOMAIN,
    ICONS_DIR,
    LOADER_URL,
    async_setup,
    handle_refresh_icons,
)

FIXTURES = Path(__file__).parent / "fixtures"


def _copy_fixture(tmp_path: Path, fixture_name: str, dest_name: str) -> Path:
    dest = tmp_path / dest_name
    dest.write_text(
        (FIXTURES / fixture_name).read_text(encoding="utf-8"), encoding="utf-8"
    )
    return dest


def _mock_hass(tmp_path: Path) -> Mock:
    hass = Mock()
    hass.config.config_dir = str(tmp_path)
    hass.data = {}
    hass.http = Mock()
    hass.http.async_register_static_paths = AsyncMock()
    hass.http.register_view = Mock()
    hass.bus = Mock()
    return hass


class TestIntegrationSetup:
    """Tests for YAML setup wiring."""

    @pytest.mark.asyncio
    async def test_async_setup_creates_folder_and_registers_frontend(
        self, tmp_path: Path
    ) -> None:
        hass = _mock_hass(tmp_path)
        with patch("custom_components.cupertino_icons.async_register_admin_service"):
            result = await async_setup(hass, {DOMAIN: {}})

        assert DOMAIN == "cupertino_icons"
        assert ICONS_DIR == "www/cupertino-icons"
        assert LOADER_URL == "/cupertino-icons/iconset.js"
        assert result is True
        icons_dir = tmp_path / ICONS_DIR
        assert icons_dir.is_dir()
        assert (icons_dir / "README.txt").is_file()
        assert LOADER_URL in hass.data[DATA_EXTRA_MODULE_URL]
        hass.http.async_register_static_paths.assert_awaited()
        assert hass.http.register_view.call_count == 2
        assert DOMAIN in hass.data

    @pytest.mark.asyncio
    async def test_refresh_icons_fires_event(self, tmp_path: Path) -> None:
        hass = _mock_hass(tmp_path)
        icons_dir = tmp_path / ICONS_DIR
        icons_dir.mkdir(parents=True)
        _copy_fixture(icons_dir, "house.svg", "house.svg")
        hass.data[DOMAIN] = {"icons_path": icons_dir}
        call = Mock()
        call.hass = hass

        await handle_refresh_icons(call)

        hass.bus.async_fire.assert_called_once()
        event_name, payload = hass.bus.async_fire.call_args.args
        assert event_name == "cupertino_icons_refreshed"
        assert payload["count"] == 1
