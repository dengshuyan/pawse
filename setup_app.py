"""
This is a setup.py script for creating a standalone macOS application using py2app.

Usage:
    python setup_app.py py2app
"""

from setuptools import setup

APP = ['pawse_menu.py']
DATA_FILES = ['meow.mp3', 'pawse_icon.png']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,  # This makes it a menu bar app without a dock icon
        'CFBundleName': 'Pawse',
        'CFBundleDisplayName': 'Pawse',
        'CFBundleIdentifier': 'com.yourusername.pawse',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2025 Alina. All rights reserved.',
        'NSRequiresAquaSystemAppearance': False,  # Support dark mode
    },
    'packages': ['rumps', 'playsound'],
    'includes': ['objc', 'Foundation', 'AppKit', 'Quartz'],
    'resources': DATA_FILES,
    'iconfile': 'pawse_icon.png',
}

setup(
    name='Pawse',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 