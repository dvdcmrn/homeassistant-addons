# SF Symbols Integration for Home Assistant

## Overview

This integration allows you to use Apple's SF Symbols in your Home Assistant dashboard by providing a way to export symbols yourself and use them with the `sfs:` prefix.

## Prerequisites

- macOS with SF Symbols app installed (free from Apple Developer portal)
- Home Assistant instance with custom integrations support
- Python 3.9+ for the export script

## Installation

### 1. Install the Integration

1. Copy the `custom_components/sf_symbols/` folder to your Home Assistant `custom_components/` directory
2. Create the directory structure:
   ```
   config/
   ├── custom_components/
   │   └── sf_symbols/
   └── www/
       └── sf_symbols/
           └── icons/
   ```

### 2. Add to Configuration

Add this to your `configuration.yaml`:

```yaml
sf_symbols:
```

### 3. Restart Home Assistant

Restart Home Assistant to load the integration.

## Exporting SF Symbols

### Method 1: Using the Export Script (Recommended)

1. **Download and setup the export script:**
   ```bash
   # Navigate to your project directory
   cd /path/to/sf_symbols_integration
   
   # Make the script executable
   chmod +x scripts/export_sf_symbols.py
   ```

2. **Run the interactive export:**
   ```bash
   python3 scripts/export_sf_symbols.py --interactive --output ~/exported_symbols
   ```

3. **Or export specific symbols:**
   ```bash
   python3 scripts/export_sf_symbols.py --symbols house heart star gear --output ~/exported_symbols
   ```

4. **Copy exported symbols to Home Assistant:**
   ```bash
   cp ~/exported_symbols/*.svg /path/to/homeassistant/www/sf_symbols/icons/
   ```

### Method 2: Manual Export from SF Symbols App

1. Open SF Symbols app
2. Search for your desired symbol
3. Right-click and select "Copy Symbol"
4. Choose "Copy as SVG"
5. Save the SVG content to a file in `www/sf_symbols/icons/`
6. Name the file with the symbol name (e.g., `house.svg`)

## Usage in Home Assistant

### Using Icons in Dashboard

Once exported, use your SF Symbols with the `sfs:` prefix:

```yaml
type: button
entity: light.living_room
icon: sfs:house
```

### Available Services

- `sf_symbols.refresh_icons`: Refresh the list of available icons after adding new ones

### Example Dashboard Card

```yaml
type: entities
entities:
  - entity: light.living_room
    icon: sfs:house
    name: Living Room
  - entity: sensor.temperature
    icon: sfs:thermometer
    name: Temperature
  - entity: switch.fan
    icon: sfs:wind
    name: Fan
```

## Terminal Commands for Batch Export

### Using sf-symbols-extract (Third-party tool)

If you prefer a more automated approach, you can use third-party tools:

```bash
# Install sf-symbols-extract (if available)
brew install sf-symbols-extract

# Export symbols
sf-symbols-extract --output ./exported_symbols --format svg house heart star
```

### Using AppleScript Automation

Create an AppleScript file to automate the SF Symbols app:

```applescript
-- Save as export_symbols.scpt
tell application "SF Symbols"
    activate
    delay 1
    
    set symbolList to {"house", "heart", "star", "gear"}
    
    repeat with symbolName in symbolList
        set search field to symbolName
        delay 0.5
        key code 125 -- Down arrow
        delay 0.2
        key code 8 using {command down} -- Cmd+C
        delay 0.5
        
        -- Save clipboard to file
        set svgData to the clipboard as string
        set filePath to "~/exported_symbols/" & symbolName & ".svg"
        
        try
            set fileRef to open for access file filePath with write permission
            write svgData to fileRef
            close access fileRef
        end try
    end repeat
end tell
```

Run with:
```bash
osascript export_symbols.scpt
```

## Troubleshooting

### Icons Not Showing

1. Check that SVG files are in the correct directory: `www/sf_symbols/icons/`
2. Ensure file names match the icon names you're using
3. Restart Home Assistant or call `sf_symbols.refresh_icons`
4. Check the Home Assistant logs for any errors

### Export Script Issues

1. Ensure SF Symbols app is installed and can be automated
2. Check that AppleScript permissions are granted
3. Try running the script with `--interactive` flag for debugging

### SVG Format Issues

1. Ensure SVG files are valid XML
2. Check that viewBox attributes are set correctly
3. Remove any unnecessary metadata from SVGs

## Icon Naming Conventions

- Use lowercase names with dots for variants: `house.fill`, `heart.circle`
- Replace spaces with dots: `person.crop.circle`
- Keep names consistent with SF Symbols naming

## Performance Tips

- Optimize SVG files by removing unnecessary attributes
- Keep icon files under 10KB each
- Limit the number of icons to what you actually use
- Use the refresh service sparingly

## Contributing

Feel free to contribute improvements to the export script or integration functionality!

## License

This integration is for personal use only. SF Symbols are copyrighted by Apple Inc. and subject to their licensing terms.