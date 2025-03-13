import rumps
import threading
import os
import time
import subprocess
import objc
import json
import datetime
from Quartz import (
    CGEventTapCreate,
    kCGEventKeyDown,
    kCGEventKeyUp,
    kCGHIDEventTap,
    kCGSessionEventTap,
    CGEventTapEnable,
    CFMachPortCreateRunLoopSource,
    CFRunLoopGetCurrent,
    CFRunLoopAddSource,
    kCFRunLoopCommonModes,
    CFRunLoopRun,
    CGEventGetIntegerValueField,
    kCGKeyboardEventKeycode,
    CGEventGetFlags,
    CGEventSetType,
    kCGEventNull,
    CGEventPost,
    kCGAnnotatedSessionEventTap,
    CGEventCreate,
    CGEventSetFlags,
    kCGEventFlagMaskAlternate,
    kCGEventFlagMaskCommand,
    kCGEventFlagMaskControl,
    kCGEventFlagMaskShift,
    CGEventSetIntegerValueField,
    CGEventMaskBit,
    CGEventSourceCreate,
    kCGEventSourceStateHIDSystemState,
)
from playsound import playsound
from mac_keyboard_layout import ADJACENT_KEYS, IGNORED_COMBOS

# Path to the meow sound (make sure meow.mp3 is in the same folder)
MEOW_SOUND = os.path.join(os.path.dirname(__file__), "meow.mp3")

# Path to the stats file
STATS_FILE = os.path.join(os.path.dirname(__file__), "pawse_stats.json")

# Track pressed keys (keycode -> timestamp)
pressed_keys = {}
# Flag to indicate if cat typing is detected
cat_typing_detected = False
# Time of last meow to prevent too frequent meows
last_meow_time = 0
# Minimum time between meows (in seconds)
MIN_MEOW_INTERVAL = 1.0
# Duration to block keystrokes after cat typing is detected (in seconds)
BLOCK_DURATION = 3.0  # Increased from 2.0 to 3.0 seconds
# Time when blocking started
block_start_time = 0
# Flag to indicate if we're in aggressive blocking mode
aggressive_blocking = False
# Flag to track if sound is currently playing
sound_playing = False
# Flag to track if notification was shown
notification_shown = False
# Track key press history for rapid typing detection
key_press_history = []
# Time window for rapid typing detection (in seconds)
RAPID_TYPING_WINDOW = 1.0
# Number of keys required in the window to trigger rapid typing detection
RAPID_TYPING_THRESHOLD = 12  # Increased from 8 to 12 to make it stricter
# Feature flags
sound_enabled = True
blocking_enabled = True
# Cat typing counter for today
cat_typing_count = 0

# Add a global variable to store the app instance
rumps_app = None

# Function to load stats from file
def load_stats():
    global cat_typing_count
    today = datetime.date.today().isoformat()
    
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
                # If we have stats for today, load them
                if today in stats:
                    cat_typing_count = stats[today]
                    print(f"Loaded cat typing count for today: {cat_typing_count}")
                else:
                    # New day, start fresh
                    cat_typing_count = 0
                    print("New day, starting fresh cat typing count")
        else:
            print("No stats file found, starting with count 0")
            cat_typing_count = 0
    except Exception as e:
        print(f"Error loading stats: {e}")
        cat_typing_count = 0

# Function to save stats to file
def save_stats():
    today = datetime.date.today().isoformat()
    
    try:
        # Load existing stats if file exists
        stats = {}
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
        
        # Update today's count
        stats[today] = cat_typing_count
        
        # Save back to file
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f)
        
        print(f"Saved cat typing count for today: {cat_typing_count}")
    except Exception as e:
        print(f"Error saving stats: {e}")

# Function to check if the app has accessibility permissions
def has_accessibility_permissions():
    try:
        # Try to create a test event tap
        test_tap = CGEventTapCreate(
            kCGAnnotatedSessionEventTap,  # Use the same tap type as our main tap
            0,
            1,
            (1 << kCGEventKeyDown),
            lambda proxy, type, event, refcon: event,
            None
        )
        
        if test_tap:
            # Clean up the test tap
            CGEventTapEnable(test_tap, False)
            return True
        return False
    except Exception as e:
        print(f"Error checking permissions: {e}")
        return False

# Function to check if the app is running with sudo privileges
def is_running_as_sudo():
    return os.geteuid() == 0

# Function to open Security & Privacy preferences
def open_accessibility_preferences():
    try:
        subprocess.run(["open", "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"])
    except Exception as e:
        print(f"Error opening preferences: {e}")
        # Fallback to a more generic command
        subprocess.run(["open", "/System/Library/PreferencePanes/Security.prefPane"])

# Function to play a meow sound
def play_meow():
    global last_meow_time, sound_playing
    current_time = time.time()
    
    # Only play if sound is enabled and enough time has passed since the last meow
    if sound_enabled and current_time - last_meow_time >= MIN_MEOW_INTERVAL and not sound_playing:
        try:
            sound_playing = True
            # Use a separate thread to play the sound to avoid blocking
            sound_thread = threading.Thread(target=_play_sound_thread, daemon=True)
            sound_thread.start()
            last_meow_time = current_time
        except Exception as e:
            print("Error starting sound thread:", e)
            sound_playing = False

def _play_sound_thread():
    global sound_playing
    try:
        # Try to play the sound with playsound
        playsound(MEOW_SOUND)
    except Exception as e:
        print("Error playing sound:", e)
        # Fallback to system sound if playsound fails
        try:
            subprocess.run(["afplay", MEOW_SOUND], check=False)
        except Exception as e2:
            print("Fallback sound also failed:", e2)
    finally:
        sound_playing = False

# Function to check if keys are adjacent
def are_keys_adjacent(keys):
    if len(keys) < 2:  # Need at least 2 keys to check adjacency
        return False
    
    # Print all keys being checked
    print(f"Checking adjacency for keys: {keys}")
    
    # Count how many adjacent pairs we find
    adjacent_pairs = 0
        
    # Check if at least 2 keys are adjacent to each other
    for key1 in keys:
        for key2 in keys:
            if key1 != key2 and key2 in ADJACENT_KEYS.get(key1, []):
                print(f"Found adjacent keys: {key1} and {key2}")
                adjacent_pairs += 1
    
    # We divide by 2 because each pair is counted twice (A->B and B->A)
    adjacent_pairs = adjacent_pairs // 2
    print(f"Found {adjacent_pairs} adjacent pairs")
    
    # Require at least 3 adjacent pairs for detection
    if adjacent_pairs >= 3:
        return True
    
    print("Not enough adjacent keys found in the cluster")
    return False

# Function to detect cat-like typing
def is_cat_typing():
    global key_press_history
    current_time = time.time()
    
    # Clean up old key presses (older than 0.5 seconds)
    active_keys = [k for k, t in pressed_keys.items() if current_time - t < 0.5]
    
    # Clean up old key press history (older than RAPID_TYPING_WINDOW)
    key_press_history = [t for t in key_press_history if current_time - t < RAPID_TYPING_WINDOW]
    
    print(f"Current pressed keys: {active_keys}, count: {len(active_keys)}")  # Debug print
    print(f"Key press history count: {len(key_press_history)} in last {RAPID_TYPING_WINDOW} seconds")
    
    # Check for rapid typing (many keys in a short time)
    if len(key_press_history) >= RAPID_TYPING_THRESHOLD:
        print(f"Rapid typing detected! {len(key_press_history)} keys in {RAPID_TYPING_WINDOW} seconds")
        return True
    
    # Need at least 4 keys for cat typing (changed from 5 back to 4)
    if len(active_keys) >= 4:
        # Check if the pressed keys match any ignored combos
        for combo in IGNORED_COMBOS:
            if combo.issubset(set(active_keys)):
                print(f"Ignored combo detected: {combo}")
                return False
        
        # Check if keys are adjacent (cat-like typing)
        if are_keys_adjacent(active_keys):
            print("Adjacent keys detected in the cluster")
            return True
        else:
            print("No adjacent keys found despite having 4+ keys pressed")
    
    return False

# Function to completely block a keyboard event
def block_keyboard_event(event):
    # Method 1: Convert to null event
    CGEventSetType(event, kCGEventNull)
    
    # Method 2: Clear all flags (modifiers)
    CGEventSetFlags(event, 0)
    
    # Method 3: Set the keycode to 0 (which is typically ignored)
    CGEventSetIntegerValueField(event, kCGKeyboardEventKeycode, 0)
    
    # Return None to prevent the event from propagating
    return None

# Function to create a more aggressive event blocker
def create_aggressive_blocker():
    # Create a source for system events
    source = CGEventSourceCreate(kCGEventSourceStateHIDSystemState)
    if source:
        print("Created aggressive event blocker")
    else:
        print("Failed to create aggressive event blocker")
    return source

# Callback for the event tap
def event_tap_callback(proxy, event_type, event, refcon):
    global cat_typing_detected, pressed_keys, block_start_time, aggressive_blocking, notification_shown, key_press_history, cat_typing_count
    
    # Get the keycode
    keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
    current_time = time.time()
    
    # If we're in blocking mode and the block duration hasn't expired
    if blocking_enabled and cat_typing_detected and current_time - block_start_time < BLOCK_DURATION:
        print(f"Blocking keystroke (keycode: {keycode}) - cat typing protection active")
        # Block both key down and key up events during the blocking period
        return block_keyboard_event(event)
    elif cat_typing_detected:
        # Block duration expired, reset cat typing detection
        cat_typing_detected = False
        aggressive_blocking = False
        notification_shown = False
        print("Cat typing block duration expired, allowing keystrokes again")
    
    if event_type == kCGEventKeyDown:
        # Record the key press with timestamp
        pressed_keys[keycode] = current_time
        # Add to key press history for rapid typing detection
        key_press_history.append(current_time)
        
        print(f"Key pressed: {keycode}, total keys: {len(pressed_keys)}")
        
        # Check if it's cat typing
        if is_cat_typing():
            if not cat_typing_detected:
                print("Cat typing detected! Meow!")
                cat_typing_detected = True
                aggressive_blocking = True
                block_start_time = current_time
                
                # Increment cat typing counter and save stats
                cat_typing_count += 1
                save_stats()
                
                # Update the menu item immediately
                if rumps_app and hasattr(rumps_app, 'cat_counter_menu_item'):
                    rumps.Timer(lambda _: rumps_app.update_counter_display(), 0.1).start()
                
                # Create an aggressive blocker
                create_aggressive_blocker()
                
                # Play meow sound
                threading.Thread(target=play_meow, daemon=True).start()
                
                # Show notification only once per detection
                if not notification_shown:
                    notification_shown = True
                    notification_text = ""
                    if sound_enabled and blocking_enabled:
                        notification_text = "Cat typing detected! Playing sound and blocking keystrokes..."
                    elif sound_enabled:
                        notification_text = "Cat typing detected! Playing sound..."
                    elif blocking_enabled:
                        notification_text = "Cat typing detected! Blocking keystrokes..."
                    else:
                        notification_text = "Cat typing detected! (Both sound and blocking are disabled)"
                    
                    threading.Thread(
                        target=lambda: rumps.notification("Pawse", "🐾", notification_text),
                        daemon=True
                    ).start()
            
            # Only block if blocking is enabled
            if blocking_enabled:
                print(f"Blocking keystroke (keycode: {keycode})")
                return block_keyboard_event(event)
    
    elif event_type == kCGEventKeyUp:
        # Remove the key from pressed keys
        if keycode in pressed_keys:
            del pressed_keys[keycode]
            print(f"Key released: {keycode}, remaining keys: {len(pressed_keys)}")
        
        # If we're in cat typing mode, also block key up events
        if blocking_enabled and (cat_typing_detected or aggressive_blocking):
            print(f"Blocking key up event (keycode: {keycode})")
            return block_keyboard_event(event)
    
    # Clean up old key presses (older than 1 second)
    for k in list(pressed_keys.keys()):
        if current_time - pressed_keys[k] > 1.0:
            del pressed_keys[k]
            print(f"Removing stale key: {k}")
    
    # Allow the keystroke to pass through
    return event

class PawseApp(rumps.App):
    def __init__(self):
        global rumps_app
        super(PawseApp, self).__init__("Pawse", icon="pawse_icon.png")
        
        # Store reference to self in global variable
        rumps_app = self
        
        # Load stats from file
        load_stats()
        
        # Create menu items with checkmarks to show status
        self.sound_menu_item = rumps.MenuItem("Meow Sound: On", callback=self.toggle_sound)
        self.blocking_menu_item = rumps.MenuItem("Keystroke Blocking: On", callback=self.toggle_blocking)
        self.cat_counter_menu_item = rumps.MenuItem(f"Cat Visits Today: {cat_typing_count}")
        
        # Add menu items - remove our custom Quit option and let rumps handle it
        self.menu = [
            self.sound_menu_item,
            self.blocking_menu_item,
            self.cat_counter_menu_item,
        ]
        
        self.tap = None
        self.tap_thread = None
        self.running = True
        self.event_source = None  # For aggressive blocking
        
        # Start Pawse automatically
        self.start_event_tap()
        rumps.notification("Pawse", "🐾", "Pawse is now active with Quartz event monitoring!")
        print("Pawse started - monitoring for cat typing using Quartz API")
        
        # Start a timer to update the counter display every minute
        # (in case the counter is updated from another instance)
        self.timer = rumps.Timer(self.update_counter_display, 60)
        self.timer.start()

    def update_counter_display(self, _=None):
        self.cat_counter_menu_item.title = f"Cat Visits Today: {cat_typing_count}"

    def toggle_sound(self, sender):
        global sound_enabled
        sound_enabled = not sound_enabled
        sender.title = f"Meow Sound: {'On' if sound_enabled else 'Off'}"
        print(f"Meow sound {'enabled' if sound_enabled else 'disabled'}")

    def toggle_blocking(self, sender):
        global blocking_enabled
        blocking_enabled = not blocking_enabled
        sender.title = f"Keystroke Blocking: {'On' if blocking_enabled else 'Off'}"
        print(f"Keystroke blocking {'enabled' if blocking_enabled else 'disabled'}")

    def quit_application(self):
        # Override the default quit to ensure we clean up properly
        self.stop_event_tap()
        super(PawseApp, self).quit_application()

    def start_event_tap(self):
        # Check if we have accessibility permissions
        if not has_accessibility_permissions():
            print("Accessibility permissions not granted!")
            
            # Check if running as sudo
            if is_running_as_sudo():
                print("Running with sudo, but still can't create event tap.")
                rumps.notification(
                    "Pawse", 
                    "⚠️", 
                    "Even with sudo, accessibility permissions are required on macOS."
                )
            else:
                print("Not running with sudo. Try running with sudo or granting accessibility permissions.")
                rumps.notification(
                    "Pawse", 
                    "⚠️", 
                    "Accessibility permissions required! Click to open settings."
                )
                # Prompt user to open settings or try sudo
                choice = rumps.alert(
                    "Accessibility Permissions Required", 
                    "Pawse needs accessibility permissions to block cat typing.\nYou can either:\n1. Grant permissions in System Preferences\n2. Run the app with sudo",
                    "Open Settings", "Try sudo", "Cancel"
                )
                
                if choice == 1:  # Open Settings
                    open_accessibility_preferences()
                elif choice == 2:  # Try sudo
                    # Show instructions for running with sudo
                    rumps.alert(
                        "Run with sudo", 
                        "To run with sudo, open Terminal and type:\nsudo python3 " + os.path.abspath(__file__),
                        "OK"
                    )
            return
        
        # Start in a separate thread to not block the main app
        self.tap_thread = threading.Thread(target=self._create_event_tap, daemon=True)
        self.tap_thread.start()

    def _create_event_tap(self):
        # Create an event source for aggressive blocking
        self.event_source = CGEventSourceCreate(kCGEventSourceStateHIDSystemState)
        
        # Create an event tap to monitor keyboard events
        self.tap = CGEventTapCreate(
            kCGAnnotatedSessionEventTap,  # Use annotated session event tap for even better blocking
            0,  # Place the tap at the beginning of the event tap chain
            0,  # Options: 0 = default tap with highest priority
            (1 << kCGEventKeyDown) | (1 << kCGEventKeyUp),  # Only capture key down/up events
            event_tap_callback,  # Callback function
            None  # User data
        )
        
        if self.tap:
            # Create a run loop source and add it to the current run loop
            run_loop_source = CFMachPortCreateRunLoopSource(None, self.tap, 0)
            CFRunLoopAddSource(CFRunLoopGetCurrent(), run_loop_source, kCFRunLoopCommonModes)
            
            # Enable the event tap
            CGEventTapEnable(self.tap, True)
            
            print("Quartz event tap created and enabled")
            print("Keystroke blocking is active - cat typing will be intercepted")
            
            # Run the loop (this will block until the tap is disabled)
            CFRunLoopRun()
        else:
            print("Failed to create event tap. Make sure the app has accessibility permissions.")
            print("Without proper permissions, keystroke blocking won't work.")
            rumps.notification("Pawse", "⚠️", "Accessibility permissions required for keystroke blocking!")

    def stop_event_tap(self):
        if self.tap:
            # Disable the event tap
            CGEventTapEnable(self.tap, False)
            print("Quartz event tap disabled")

if __name__ == "__main__":
    app = PawseApp()
    app.run()

def main():
    """Entry point for the application when installed via pip."""
    app = PawseApp()
    app.run()