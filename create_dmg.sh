#!/bin/bash

# Exit on error
set -e

echo "Creating Pawse DMG installer..."

# Install required tools if not already installed
if ! command -v create-dmg &> /dev/null; then
    echo "Installing create-dmg..."
    brew install create-dmg
fi

# Build the app using py2app
echo "Building macOS application..."
python3 setup_app.py py2app

# Create a DMG file
echo "Creating DMG installer..."
create-dmg \
  --volname "Pawse Installer" \
  --volicon "pawse_icon.png" \
  --background "pawse_icon.png" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "Pawse.app" 150 190 \
  --hide-extension "Pawse.app" \
  --app-drop-link 450 190 \
  "Pawse-1.0.0.dmg" \
  "dist/Pawse.app"

echo "DMG installer created: Pawse-1.0.0.dmg" 