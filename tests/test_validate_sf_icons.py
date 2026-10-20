"""Tests for the SVG validator CLI."""

from pathlib import Path

from scripts.validate_sf_icons import main, validate_directory

FIXTURES = Path(__file__).parent / "fixtures"


def test_validate_directory_ok(tmp_path: Path, capsys) -> None:
    dest = tmp_path / "homepod.fill.svg"
    dest.write_text(
        (FIXTURES / "house.svg").read_text(encoding="utf-8"), encoding="utf-8"
    )
    assert validate_directory(tmp_path) == 0
    output = capsys.readouterr().out
    assert "sf:homepod-fill" in output
    assert "OK" in output


def test_validate_directory_rejects_template(tmp_path: Path, capsys) -> None:
    dest = tmp_path / "homepod.fill.svg"
    dest.write_text(
        (FIXTURES / "template_symbol.svg").read_text(encoding="utf-8"), encoding="utf-8"
    )
    assert validate_directory(tmp_path) == 1
    output = capsys.readouterr().out
    assert "FAIL" in output


def test_main_missing_directory(tmp_path: Path) -> None:
    assert main([str(tmp_path / "nope")]) == 2
