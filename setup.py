from setuptools import setup

APP = ['pawse_menu.py']
DATA_FILES = ['meow.mp3', 'pawse_icon.png']
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'pawse_icon.png',
    'plist': {
        'CFBundleName': 'Pawse',
        'CFBundleDisplayName': 'Pawse',
        'CFBundleIdentifier': 'com.pawse.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.10',
        'LSApplicationCategoryType': 'public.app-category.utilities',
        'NSHighResolutionCapable': True,
        'NSAppleEventsUsageDescription': 'Pawse needs to monitor keyboard events to detect cat typing.',
        'NSAccessibilityUsageDescription': 'Pawse needs accessibility access to block keyboard input when cat typing is detected.',
        'NSMicrophoneUsageDescription': 'Pawse needs microphone access to play sound effects.',
        'LSUIElement': True,  # This makes it a menu bar app
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'rumps>=0.4.0',
        'pyobjc-framework-Quartz>=9.2',
        'pyobjc-framework-Cocoa>=9.2',
        'playsound>=1.3.0',
    ],
) 