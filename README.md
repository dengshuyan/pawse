# Pawse - Cat Typing Detector and Blocker

<img src="pawse_icon.png" alt="Pawse Icon" width="16"/>

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
- Python 3.6 or later (only needed for building from source)
- Required permissions:
  - Accessibility permissions (for keystroke monitoring and blocking)
  - Input Monitoring permissions (for keyboard event detection)

## Installation

### Option 1: Using the Pre-built App (Recommended)

1. Download the latest release of Pawse.app from the releases page
2. Move Pawse.app to your Applications folder
3. Open System Settings > Privacy & Security
4. Grant the following permissions to Pawse:
   - Accessibility: System Settings > Privacy & Security > Accessibility
   - Input Monitoring: System Settings > Privacy & Security > Input Monitoring
5. Launch Pawse from your Applications folder

### Option 2: From Source

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/pawse.git
   cd pawse
   ```

2. Install the required dependencies:
   ```
   pip3 install rumps pyobjc playsound py2app
   ```

3. Build the application:
   ```
   python3 setup.py py2app
   ```
   This will create a standalone application in the `dist` folder.

4. Move Pawse.app from the `dist` folder to your Applications folder

5. Grant required permissions:
   - Open System Settings > Privacy & Security
   - Add Pawse to both Accessibility and Input Monitoring permissions
   - Make sure both checkboxes are checked

## Usage

1. **First Run**: When you first run Pawse, it will request necessary permissions
   - Follow the prompts to open System Settings > Privacy & Security
   - Add Pawse to both Accessibility and Input Monitoring permissions
   - Make sure both checkboxes are checked

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

- **App Not Working**: 
  - Make sure both Accessibility and Input Monitoring permissions are granted
  - Try removing and re-adding the permissions
  - Restart the application after granting permissions

- **Keystroke Blocking Not Working**: 
  - Check if Accessibility permissions are granted
  - Try removing and re-adding the Accessibility permission
  - Restart the application

- **Sound Not Playing**: 
  - Ensure your system volume is on
  - Check if sound is enabled in Pawse's menu
  - Verify that the meow.mp3 file is present in the app bundle

- **High CPU Usage**: 
  - If you notice high CPU usage, try restarting the application
  - Check if the app is running multiple instances

## Distribution

To distribute Pawse to other users:

1. Build the application using `python3 setup.py py2app`
2. Share the `Pawse.app` from the `dist` folder
3. Instruct users to:
   - Move Pawse.app to their Applications folder
   - Grant both Accessibility and Input Monitoring permissions
   - Launch the app from Applications

## License

[MIT License](LICENSE)

## Acknowledgements

- Meow sound from SOUND_GARAGE
- Special thanks to all the cats who helped test this application by walking on keyboards

<img src="cat_typing.JPG" alt="Special Thanks" width="48"/>