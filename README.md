# Pawse - Cat Typing Detector and Blocker

<img src="pawse_icon.png" alt="Pawse Icon" width="100"/>

Pawse is a macOS menu bar application that detects when your cat walks on your keyboard and:
1. Plays a meow sound
2. Blocks keystrokes for a few seconds
3. Keeps track of how many times your cat has visited your keyboard today

## Features

- **Cat Typing Detection**: Uses advanced algorithms to detect when a cat is walking on your keyboard
  - Detects multiple keys pressed simultaneously (4+ keys)
  - Identifies adjacent key patterns typical of cat paws
  - Recognizes rapid typing patterns

- **Keystroke Blocking**: Temporarily blocks keyboard input when cat typing is detected
  - Prevents accidental commands, deletions, or other unwanted actions
  - Configurable blocking duration (currently set to 3 seconds)

- **Sound Alerts**: Plays a meow sound when cat typing is detected
  - Helps you know when your cat is on the keyboard even if you're away

- **Cat Visit Counter**: Keeps track of how many times your cat has stepped on your keyboard today
  - Stats are saved between sessions

- **Simple Menu Bar Interface**: Easy-to-use menu bar controls
  - Toggle sound alerts on/off
  - Toggle keystroke blocking on/off
  - View today's cat visit count

## Requirements

- macOS 10.14 or later
- Python 3.6 or later
- Accessibility permissions (required for keystroke monitoring and blocking)

## Installation

### Option 1: From Source

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/pawse.git
   cd pawse
   ```

2. Install the required dependencies:
   ```
   pip3 install rumps pyobjc playsound
   ```

3. Run the application:
   ```
   python3 pawse_menu.py
   ```

### Option 2: Using the Installer (Coming Soon)

A packaged installer will be available soon.

### Option 3: Building the App Yourself

You can build a standalone macOS application (.app) and create a DMG installer:

1. Install py2app and other required tools:
   ```
   pip3 install py2app
   brew install create-dmg
   ```

2. Build the application:
   ```
   python3 setup_app.py py2app
   ```
   This will create a standalone application in the `dist` folder.

3. Create a DMG installer (optional):
   ```
   ./create_dmg.sh
   ```
   This will create a DMG installer file that you can distribute.

## Usage

1. **First Run**: When you first run Pawse, it will request accessibility permissions
   - Follow the prompts to open System Preferences > Security & Privacy > Privacy > Accessibility
   - Add the application to the list of allowed apps

2. **Menu Bar Controls**:
   - Click the paw icon in the menu bar to access controls
   - Toggle "Meow Sound" on/off
   - Toggle "Keystroke Blocking" on/off
   - View "Cat Visits Today" counter
   - Quit the application

3. **When Cat Typing is Detected**:
   - A meow sound will play (if enabled)
   - Keystrokes will be blocked for 3 seconds (if enabled)
   - A notification will appear
   - The cat visit counter will increment

## How It Works

Pawse uses macOS's Quartz Event Tap API to monitor keyboard events. It detects cat typing through two methods:

1. **Multiple Adjacent Keys**: When 4 or more keys are pressed with at least 3 adjacent pairs
2. **Rapid Typing**: When many keys are pressed in a short time window

When cat typing is detected, Pawse can block keyboard events by converting them to null events, preventing any unwanted input.

## Troubleshooting

- **Keystroke Blocking Not Working**: Make sure Pawse has accessibility permissions
- **Sound Not Playing**: Ensure your system volume is on and the sound is enabled in Pawse
- **High CPU Usage**: If you notice high CPU usage, try restarting the application

## License

[MIT License](LICENSE)

## Acknowledgements

- Meow sound from SOUND_GARAGE
- Special thanks to all the cats who helped test this application by walking on keyboards 