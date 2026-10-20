#!/usr/bin/env python3
"""
SF Symbols export helper for the Cupertino Icons integration.
Runs on macOS with the SF Symbols app; exports SVGs for use in Home Assistant.
"""

import argparse
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional


class SFSymbolsExporter:
    """Export SF Symbols to SVG format for Home Assistant."""

    def __init__(self, output_dir: str = None):
        self.output_dir = (
            Path(output_dir) if output_dir else Path.cwd() / "exported_symbols"
        )
        self.temp_dir = Path(tempfile.mkdtemp())

    def check_requirements(self) -> bool:
        try:
            sf_symbols_path = "/Applications/SF Symbols.app"
            if not Path(sf_symbols_path).exists():
                print(
                    "FAIL: SF Symbols app not found. Install it from Apple Developer."
                )
                return False

            subprocess.run(
                ["osascript", "-e", "return 1"], capture_output=True, check=True
            )

            print("OK: SF Symbols app found")
            print("OK: AppleScript support available")
            return True

        except Exception as e:
            print(f"FAIL: Requirements check failed: {e}")
            return False

    def list_available_symbols(self) -> List[str]:
        common_symbols = [
            "house",
            "house.fill",
            "heart",
            "heart.fill",
            "star",
            "star.fill",
            "person",
            "person.fill",
            "gear",
            "lightbulb",
            "lightbulb.fill",
            "thermometer",
            "humidity",
            "leaf",
            "leaf.fill",
            "drop",
            "drop.fill",
            "lock",
            "lock.fill",
            "wifi",
            "bluetooth",
            "battery.100",
            "battery.50",
            "play",
            "pause",
            "stop",
            "volume.3",
            "volume.2",
            "volume.1",
            "sun.max",
            "moon",
            "cloud",
            "cloud.rain",
            "snow",
            "wind",
        ]
        return common_symbols

    def export_symbol_to_svg(self, symbol_name: str, size: int = 24) -> Optional[str]:
        try:
            applescript = f"""
            tell application "SF Symbols"
                activate
                delay 0.5

                set search field to "{symbol_name}"
                delay 0.5

                key code 125
                delay 0.2

                key code 8 using {{command down}}
                delay 0.5

                set svgData to the clipboard as string
                return svgData
            end tell
            """

            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0 and result.stdout.strip():
                svg_content = self.clean_svg_content(result.stdout.strip())

                output_file = self.output_dir / f"{symbol_name}.svg"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(svg_content)

                print(f"OK: Exported {symbol_name}.svg")
                return str(output_file)
            print(f"FAIL: Could not export {symbol_name}")
            return None

        except Exception as e:
            print(f"FAIL: Error exporting {symbol_name}: {e}")
            return None

    def clean_svg_content(self, svg_content: str) -> str:
        if svg_content.startswith("<?xml"):
            svg_content = (
                svg_content.split(">", 1)[1] if ">" in svg_content else svg_content
            )

        if not svg_content.strip().startswith("<svg"):
            svg_content = (
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
                f'width="24" height="24">{svg_content}</svg>'
            )

        svg_content = svg_content.replace("\n", " ").replace("\t", " ")
        while "  " in svg_content:
            svg_content = svg_content.replace("  ", " ")

        return svg_content.strip()

    def export_symbols(
        self, symbols: List[str], interactive: bool = False
    ) -> Dict[str, str]:
        if not self.check_requirements():
            return {}

        self.output_dir.mkdir(parents=True, exist_ok=True)

        exported = {}
        total = len(symbols)

        print(f"Starting export of {total} symbols...")
        print(f"Output directory: {self.output_dir}")
        print("Ensure SF Symbols is idle and can receive AppleScript commands.")

        if interactive:
            input("Press Enter to continue...")

        for i, symbol in enumerate(symbols, 1):
            print(f"[{i}/{total}] Exporting {symbol}...")
            file_path = self.export_symbol_to_svg(symbol)
            if file_path:
                exported[symbol] = file_path
            if i < total:
                time.sleep(0.5)

        print(
            f"\nExport complete: {len(exported)}/{total} symbols exported successfully."
        )
        return exported

    def create_symbol_list_ui(self) -> List[str]:
        available_symbols = self.list_available_symbols()

        print("Available SF Symbols:")
        for i, symbol in enumerate(available_symbols, 1):
            print(f"{i:2d}. {symbol}")

        print("\nSelect symbols to export:")
        print("  - Enter numbers separated by commas (e.g., 1,3,5)")
        print("  - Enter 'all' to export all symbols")
        print("  - Enter 'common' to export a curated list")

        selection = input("\nYour selection: ").strip()

        if selection.lower() == "all":
            return available_symbols
        if selection.lower() == "common":
            return available_symbols[:15]
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(",")]
            return [
                available_symbols[i] for i in indices if 0 <= i < len(available_symbols)
            ]
        except ValueError:
            print("Invalid selection. Using common symbols.")
            return available_symbols[:15]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export SF Symbols for Cupertino Icons (Home Assistant)"
    )
    parser.add_argument(
        "--output", "-o", help="Output directory", default="./exported_symbols"
    )
    parser.add_argument("--symbols", "-s", nargs="+", help="Specific symbols to export")
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive symbol selection"
    )
    parser.add_argument(
        "--list", "-l", action="store_true", help="List available symbols"
    )

    args = parser.parse_args()
    exporter = SFSymbolsExporter(args.output)

    if args.list:
        symbols = exporter.list_available_symbols()
        print("Available SF Symbols:")
        for symbol in symbols:
            print(f"  - {symbol}")
        return

    if args.symbols:
        symbols_to_export = args.symbols
    elif args.interactive:
        symbols_to_export = exporter.create_symbol_list_ui()
    else:
        symbols_to_export = exporter.list_available_symbols()[:10]

    if not symbols_to_export:
        print("No symbols selected for export.")
        sys.exit(1)

    exported = exporter.export_symbols(symbols_to_export, interactive=args.interactive)

    if exported:
        print(f"\nSuccessfully exported {len(exported)} symbols.")
        print(f"Location: {exporter.output_dir}")
        print("\nNext steps:")
        print("1. Add cupertino_icons: to configuration.yaml if not already present")
        print("2. Copy exported SVG files to www/cupertino-icons/ on your HA host")
        print("3. Call cupertino_icons.refresh_icons (or restart Home Assistant)")
        print(
            "4. Hard-reload the browser; use icons as sf:symbol-name (e.g., sf:house)"
        )


if __name__ == "__main__":
    main()
