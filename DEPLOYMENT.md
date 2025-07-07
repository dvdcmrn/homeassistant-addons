# Deployment Guide

## 🚀 GitHub Deployment

### 1. Initialize Git Repository (if not already done)

```bash
git init
git add .
git commit -m "Initial commit: SF Symbols Home Assistant integration"
```

### 2. Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `sf-symbols-home-assistant` or `home-assistant-sf-symbols`
3. Make it public or private as preferred
4. **Don't** initialize with README, .gitignore, or license (we already have these)

### 3. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 4. Update Repository URLs

After pushing to GitHub, update these files with your actual repository URL:

- `custom_components/sf_symbols/manifest.json` - Update the `documentation` field
- `README.md` - Update any GitHub links
- `docs/SETUP.md` - Update any GitHub links

## 🏠 Home Assistant Deployment

### Method 1: Manual Installation (Recommended for Development)

1. **Copy Integration Files**
   ```bash
   # Copy the integration to your Home Assistant config directory
   cp -r custom_components/sf_symbols /path/to/homeassistant/config/custom_components/
   
   # Create the www directory structure
   mkdir -p /path/to/homeassistant/config/www/sf_symbols/icons
   ```

2. **Add to Configuration**
   Add this to your `configuration.yaml`:
   ```yaml
   sf_symbols:
   ```

3. **Restart Home Assistant**
   Restart Home Assistant to load the integration.

### Method 2: HACS Installation (For Distribution)

If you want to distribute this through HACS (Home Assistant Community Store):

1. **Fork the Repository**
   - Fork your repository to create a personal copy

2. **Submit to HACS**
   - Follow the [HACS submission process](https://hacs.xyz/docs/publish/start)
   - This requires additional files like `hacs.json` and proper documentation

3. **Users can then install via HACS**
   - Users can install directly from HACS interface
   - Automatic updates when you release new versions

## 📦 Release Process

### 1. Version Management

Update the version in `custom_components/sf_symbols/manifest.json`:

```json
{
  "version": "1.0.1"
}
```

### 2. Create Release

```bash
# Tag the release
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1

# Create GitHub release
# Go to GitHub → Releases → Create new release
# Use the tag you just created
```

### 3. Update Documentation

- Update `README.md` with new features/fixes
- Update `docs/SETUP.md` if needed
- Update any version-specific instructions

## 🔧 Development Workflow

### 1. Setup Development Environment

```bash
# Run the setup script
python3 scripts/setup_dev.py

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows
```

### 2. Development Commands

```bash
# Run tests
python -m pytest tests/

# Format code
black .

# Lint code
flake8 .

# Run the export script
python3 scripts/export_sf_symbols.py --interactive
```

### 3. Testing in Home Assistant

1. Copy updated files to your Home Assistant config
2. Restart Home Assistant
3. Test the integration functionality
4. Check logs for any errors

## 📋 Pre-Deployment Checklist

- [ ] All tests pass (`python -m pytest tests/`)
- [ ] Code is formatted (`black .`)
- [ ] Linting passes (`flake8 .`)
- [ ] Documentation is updated
- [ ] Version numbers are updated
- [ ] Sample icons are included
- [ ] README.md is complete and accurate
- [ ] License file is present
- [ ] .gitignore is comprehensive
- [ ] GitHub Actions workflow is working

## 🐛 Troubleshooting

### Common Issues

1. **Integration not loading**
   - Check Home Assistant logs
   - Verify file permissions
   - Ensure all required files are present

2. **Icons not showing**
   - Verify SVG files are in correct directory
   - Check file naming conventions
   - Restart Home Assistant

3. **Export script issues**
   - Ensure SF Symbols app is installed
   - Check AppleScript permissions
   - Run with `--interactive` flag for debugging

### Getting Help

- Check the [troubleshooting section](README.md#-troubleshooting) in README
- Review the [detailed setup guide](docs/SETUP.md)
- Open an issue on GitHub with detailed information

## 📈 Future Enhancements

Consider these improvements for future releases:

- [ ] HACS integration
- [ ] More comprehensive icon library
- [ ] Web interface for icon management
- [ ] Icon categories and search
- [ ] Custom icon creation tools
- [ ] Integration with other icon providers
- [ ] Performance optimizations
- [ ] More extensive testing

---

**Happy coding! 🎉** 