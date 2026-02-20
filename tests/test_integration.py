"""Tests for the dvdcmrn Home Assistant Icons integration."""
import pytest
from unittest.mock import Mock, patch
from pathlib import Path

from custom_components.dvdcmrn_icons import async_setup, DOMAIN
from custom_components.dvdcmrn_icons.icon_manager import DvdcmrnIconsIconManager


@pytest.fixture
def mock_hass():
    """Create a mock Home Assistant instance."""
    hass = Mock()
    hass.config.config_dir = "/tmp/test_config"
    hass.data = {}
    return hass


@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    return {DOMAIN: {}}


class TestDvdcmrnIconsIntegration:
    """Test the dvdcmrn Home Assistant Icons integration."""

    @pytest.mark.asyncio
    async def test_async_setup(self, mock_hass, mock_config):
        """Test that the integration sets up correctly."""
        with patch('pathlib.Path.mkdir'):
            result = await async_setup(mock_hass, mock_config)
            assert result is True
            assert DOMAIN in mock_hass.data


class TestDvdcmrnIconsIconManager:
    """Test the icon manager."""

    def test_scan_icons_empty_directory(self, tmp_path):
        """Test scanning icons from an empty directory."""
        manager = DvdcmrnIconsIconManager(Mock(), tmp_path)
        icons = manager.scan_icons()
        assert icons == []

    def test_scan_icons_with_files(self, tmp_path):
        """Test scanning icons from a directory with SVG files."""
        # Create test SVG files
        (tmp_path / "house.svg").write_text("<svg></svg>")
        (tmp_path / "heart.svg").write_text("<svg></svg>")
        
        manager = DvdcmrnIconsIconManager(Mock(), tmp_path)
        icons = manager.scan_icons()
        assert set(icons) == {"house", "heart"}

    def test_get_icon_path_exists(self, tmp_path):
        """Test getting icon path when file exists."""
        svg_file = tmp_path / "house.svg"
        svg_file.write_text("<svg></svg>")
        
        manager = DvdcmrnIconsIconManager(Mock(), tmp_path)
        path = manager.get_icon_path("house")
        assert path == str(svg_file)

    def test_get_icon_path_not_exists(self, tmp_path):
        """Test getting icon path when file doesn't exist."""
        manager = DvdcmrnIconsIconManager(Mock(), tmp_path)
        path = manager.get_icon_path("nonexistent")
        assert path is None

    def test_validate_icon_valid_svg(self, tmp_path):
        """Test validating a valid SVG file."""
        svg_file = tmp_path / "test.svg"
        svg_file.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>')
        
        manager = DvdcmrnIconsIconManager(Mock(), tmp_path)
        assert manager.validate_icon(svg_file) is True

    def test_validate_icon_invalid_svg(self, tmp_path):
        """Test validating an invalid SVG file."""
        svg_file = tmp_path / "test.svg"
        svg_file.write_text("not an svg")
        
        manager = DvdcmrnIconsIconManager(Mock(), tmp_path)
        assert manager.validate_icon(svg_file) is False
