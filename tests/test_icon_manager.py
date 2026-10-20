"""Tests for SF icon scanning, naming, and SVG parsing."""

from pathlib import Path

import pytest

from custom_components.cupertino_icons.icon_manager import IconManager

FIXTURES = Path(__file__).parent / "fixtures"


def _copy_fixture(tmp_path: Path, fixture_name: str, dest_name: str) -> Path:
    dest = tmp_path / dest_name
    dest.write_text(
        (FIXTURES / fixture_name).read_text(encoding="utf-8"), encoding="utf-8"
    )
    return dest


class TestIconManager:
    """Tests for scanning, naming, and SVG parsing."""

    def test_scan_icons_empty_directory(self, tmp_path: Path) -> None:
        manager = IconManager(tmp_path)
        assert manager.list_icons() == []

    def test_dotted_filename_maps_to_hyphen_ha_name(self, tmp_path: Path) -> None:
        _copy_fixture(tmp_path, "house.svg", "homepod.fill.svg")
        manager = IconManager(tmp_path)
        listed = manager.list_icons()
        assert listed == [{"name": "homepod-fill", "keywords": ["homepod", "fill"]}]

    def test_get_icon_prefers_dotted_filename(self, tmp_path: Path) -> None:
        _copy_fixture(tmp_path, "house.svg", "homepod.fill.svg")
        manager = IconManager(tmp_path)
        icon = manager.get_icon("homepod-fill")
        assert icon is not None
        assert "M12 3" in icon["path"]
        assert icon["viewBox"] == "0 0 24 24"

    def test_hyphen_filename_is_fallback(self, tmp_path: Path) -> None:
        _copy_fixture(tmp_path, "house.svg", "homepod-fill.svg")
        manager = IconManager(tmp_path)
        icon = manager.get_icon("homepod-fill")
        assert icon is not None
        assert "M12 3" in icon["path"]
        assert manager.list_icons()[0]["name"] == "homepod-fill"

    def test_dotted_filename_wins_over_hyphen_duplicate(self, tmp_path: Path) -> None:
        _copy_fixture(tmp_path, "house.svg", "homepod.fill.svg")
        hyphen = tmp_path / "homepod-fill.svg"
        hyphen.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
            '<path d="M1 1 L2 2"/></svg>',
            encoding="utf-8",
        )
        manager = IconManager(tmp_path)
        icon = manager.get_icon("homepod-fill")
        assert icon is not None
        assert "M12 3" in icon["path"]
        assert len(manager.list_icons()) == 1

    def test_skips_invisible_chrome_and_ignores_fill(self, tmp_path: Path) -> None:
        _copy_fixture(tmp_path, "with_chrome.svg", "house.svg")
        manager = IconManager(tmp_path)
        icon = manager.get_icon("house")
        assert icon is not None
        assert "M4 12" in icon["path"]
        assert "rect" not in icon["path"].lower()

    def test_rejects_xcode_symbol_template(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        _copy_fixture(tmp_path, "template_symbol.svg", "homepod.fill.svg")
        manager = IconManager(tmp_path)
        assert manager.get_icon("homepod-fill") is None
        assert manager.list_icons() == []
        assert "template" in caplog.text.lower()

    def test_missing_icon_returns_none(self, tmp_path: Path) -> None:
        manager = IconManager(tmp_path)
        assert manager.get_icon("nope") is None

    def test_invalid_svg_is_skipped(self, tmp_path: Path) -> None:
        (tmp_path / "broken.svg").write_text("not an svg", encoding="utf-8")
        manager = IconManager(tmp_path)
        assert manager.list_icons() == []
        assert manager.get_icon("broken") is None

    def test_simple_name_without_dots(self, tmp_path: Path) -> None:
        _copy_fixture(tmp_path, "house.svg", "house.svg")
        manager = IconManager(tmp_path)
        assert manager.list_icons()[0]["name"] == "house"
        assert manager.get_icon("house") is not None

    def test_count_svgs(self, tmp_path: Path) -> None:
        _copy_fixture(tmp_path, "house.svg", "house.svg")
        (tmp_path / "notes.txt").write_text("ignore", encoding="utf-8")
        manager = IconManager(tmp_path)
        assert manager.count_svgs() == 1
