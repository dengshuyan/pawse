#!/bin/bash

echo "Cleaning previous builds..."
rm -rf build dist *.pyc __pycache__ .eggs *.egg-info

echo "Installing required packages..."
pip3 install --upgrade pip
pip3 install --upgrade py2app
pip3 install -r requirements.txt

echo "Building development version for testing..."
python3 setup.py py2app -A

echo "Testing application..."
if [ -d "dist/Pawse.app" ]; then
    echo "Build successful! Testing launch..."
    open dist/Pawse.app
    
    echo "Waiting for 5 seconds to check if app launches..."
    sleep 5
    
    # Check if the app is running
    if pgrep -f "Pawse.app" > /dev/null; then
        echo "App launched successfully!"
        
        echo "Creating production build..."
        rm -rf build dist
        python3 setup.py py2app
        
        echo "Creating DMG..."
        if [ -f "dist/Pawse.dmg" ]; then
            rm "dist/Pawse.dmg"
        fi
        hdiutil create -volname "Pawse" -srcfolder "dist/Pawse.app" -ov -format UDZO "dist/Pawse.dmg"
        
        echo "Build complete! You can find the app in dist/Pawse.app and the installer in dist/Pawse.dmg"
    else
        echo "App failed to launch properly. Please check the console for errors."
        exit 1
    fi
else
    echo "Build failed! Check the output above for errors."
    exit 1
fi 