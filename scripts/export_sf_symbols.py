#!/usr/bin/env python3
"""
SF Symbols Export Script for Home Assistant Integration
This script helps export SF Symbols from macOS to SVG format for use in Home Assistant.
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
import argparse

class SFSymbolsExporter:
    """Export SF Symbols to SVG format for Home Assistant."""
    
    def __init__(self, output_dir: str = None):
        """Initialize the exporter."""
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "exported_symbols"
        self.temp_dir = Path(tempfile.mkdtemp())
        
    def check_requirements(self) -> bool:
        """Check if SF Symbols app and required tools are available."""
        try:
            # Check if SF Symbols app is installed
            sf_symbols_path = "/Applications/SF Symbols.app"
            if not Path(sf_symbols_path).exists():
                print("❌ SF Symbols app not found. Please install it from Apple Developer portal.")
                return False
                
            # Check if we can run osascript
            subprocess.run(["osascript", "-e", "return 1"], 
                         capture_output=True, check=True)
            
            print("✅ SF Symbols app found")
            print("✅ AppleScript support available")
            return True
            
        except Exception as e:
            print(f"❌ Requirements check failed: {e}")
            return False
    
    def list_available_symbols(self) -> List[str]:
        """Get list of available SF Symbols."""
        # This would need to be implemented based on SF Symbols catalog
        # For now, return a sample list
        common_symbols = [
            "house", "house.fill", "heart", "heart.fill", "star", "star.fill",
            "person", "person.fill", "gear", "lightbulb", "lightbulb.fill",
            "thermometer", "humidity", "leaf", "leaf.fill", "drop", "drop.fill",
            "lock", "lock.fill", "wifi", "bluetooth", "battery.100", "battery.50",
            "play", "pause", "stop", "volume.3", "volume.2", "volume.1",
            "sun.max", "moon", "cloud", "cloud.rain", "snow", "wind"
        ]
        return common_symbols
    
    def export_symbol_to_svg(self, symbol_name: str, size: int = 24) -> Optional[str]:
        """Export a single SF Symbol to SVG format."""
        try:
            # Create AppleScript to export the symbol
            applescript = f'''
            tell application "SF Symbols"
                activate
                delay 0.5
                
                -- Search for the symbol
                set search field to "{symbol_name}"
                delay 0.5
                
                -- Select the symbol (assumes it's the first result)
                key code 125 -- Down arrow to select first result
                delay 0.2
                
                -- Copy as SVG
                key code 8 using {{command down}} -- Cmd+C
                delay 0.5
                
                -- Get clipboard content
                set svgData to the clipboard as string
                return svgData
            end tell
            '''
            
            # Run AppleScript
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout.strip():
                svg_content = result.stdout.strip()
                
                # Clean up the SVG content
                svg_content = self.clean_svg_content(svg_content)
                
                # Save to file
                output_file = self.output_dir / f"{symbol_name}.svg"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                
                print(f"✅ Exported: {symbol_name}.svg")
                return str(output_file)
            else:
                print(f"❌ Failed to export: {symbol_name}")
                return None
                
        except Exception as e:
            print(f"❌ Error exporting {symbol_name}: {e}")
            return None
    
    def clean_svg_content(self, svg_content: str) -> str:
        """Clean and optimize SVG content for Home Assistant."""
        # Remove any XML declaration if present
        if svg_content.startswith('<?xml'):
            svg_content = svg_content.split('>', 1)[1] if '>' in svg_content else svg_content
        
        # Ensure proper SVG structure
        if not svg_content.strip().startswith('<svg'):
            # If it's not a proper SVG, wrap it
            svg_content = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">{svg_content}</svg>'
        
        # Basic cleanup
        svg_content = svg_content.replace('\n', ' ').replace('\t', ' ')
        while '  ' in svg_content:
            svg_content = svg_content.replace('  ', ' ')
        
        return svg_content.strip()
    
    def export_symbols(self, symbols: List[str], interactive: bool = False) -> Dict[str, str]:
        """Export multiple SF Symbols."""
        if not self.check_requirements():
            return {}
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        exported = {}
        total = len(symbols)
        
        print(f"🚀 Starting export of {total} symbols...")
        print(f"📁 Output directory: {self.output_dir}")
        print("⚠️  Make sure SF Symbols app is not busy and can receive commands")
        
        if interactive:
            input("Press Enter to continue...")
        
        for i, symbol in enumerate(symbols, 1):
            print(f"[{i}/{total}] Exporting {symbol}...")
            
            file_path = self.export_symbol_to_svg(symbol)
            if file_path:
                exported[symbol] = file_path
            
            # Small delay between exports
            if i < total:
                import time
                time.sleep(0.5)
        
        print(f"\n✅ Export complete! {len(exported)}/{total} symbols exported successfully.")
        return exported
    
    def create_symbol_list_ui(self) -> List[str]:
        """Create a simple UI to select symbols."""
        available_symbols = self.list_available_symbols()
        
        print("📝 Available SF Symbols:")
        for i, symbol in enumerate(available_symbols, 1):
            print(f"{i:2d}. {symbol}")
        
        print("\n🎯 Select symbols to export:")
        print("   - Enter numbers separated by commas (e.g., 1,3,5)")
        print("   - Enter 'all' to export all symbols")
        print("   - Enter 'common' to export a curated list of common symbols")
        
        selection = input("\nYour selection: ").strip()
        
        if selection.lower() == 'all':
            return available_symbols
        elif selection.lower() == 'common':
            return available_symbols[:15]  # First 15 symbols
        else:
            try:
                indices = [int(x.strip()) - 1 for x in selection.split(',')]
                return [available_symbols[i] for i in indices if 0 <= i < len(available_symbols)]
            except ValueError:
                print("❌ Invalid selection. Using common symbols.")
                return available_symbols[:15]

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Export SF Symbols for Home Assistant")
    parser.add_argument("--output", "-o", help="Output directory", default="./exported_symbols")
    parser.add_argument("--symbols", "-s", nargs="+", help="Specific symbols to export")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive symbol selection")
    parser.add_argument("--list", "-l", action="store_true", help="List available symbols")
    
    args = parser.parse_args()
    
    exporter = SFSymbolsExporter(args.output)
    
    if args.list:
        symbols = exporter.list_available_symbols()
        print("📝 Available SF Symbols:")
        for symbol in symbols:
            print(f"  • {symbol}")
        return
    
    if args.symbols:
        symbols_to_export = args.symbols
    elif args.interactive:
        symbols_to_export = exporter.create_symbol_list_ui()
    else:
        # Default to common symbols
        symbols_to_export = exporter.list_available_symbols()[:10]
    
    if not symbols_to_export:
        print("❌ No symbols selected for export.")
        return
    
    exported = exporter.export_symbols(symbols_to_export, interactive=args.interactive)
    
    if exported:
        print(f"\n🎉 Successfully exported {len(exported)} symbols!")
        print(f"📁 Location: {exporter.output_dir}")
        print("\n📋 Next steps:")
        print("1. Copy the exported SVG files to your Home Assistant www/sf_symbols/icons/ directory")
        print("2. Restart Home Assistant or call the sf_symbols.refresh_icons service")
        print("3. Use icons with the sfs: prefix (e.g., sfs:house, sfs:heart)")

if __name__ == "__main__":
    main()