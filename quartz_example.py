import time
import threading
import os
import rumps
from Quartz import (
    CGEventTapCreate,
    kCGEventKeyDown,
    kCGEventKeyUp,
    kCGEventFlagMaskCommand,
    kCGEventFlagMaskShift,
    kCGEventFlagMaskControl,
    kCGEventFlagMaskAlternate,
    kCGHIDEventTap,
    CGEventTapEnable,
    CGEventCreateKeyboardEvent,
    CFMachPortCreateRunLoopSource,
    CFRunLoopGetCurrent,
    CFRunLoopAddSource,
    kCFRunLoopCommonModes,
    CFRunLoopRun,
    CGEventGetIntegerValueField,
    kCGKeyboardEventKeycode,
    CGEventSetFlags,
    CGEventPost,
    kCGHIDEventTap,
    CGEventGetFlags,
)
from playsound import playsound

# Path to the meow sound
MEOW_SOUND = os.path.join(os.path.dirname(__file__), "meow.mp3")

# Time of last meow to prevent too frequent meows
last_meow_time = 0
# Minimum time between meows (in seconds)
MIN_MEOW_INTERVAL = 1.0

# Track pressed keys (keycode -> timestamp)
pressed_keys = {}
# Flag to indicate if cat typing is detected
cat_typing_detected = False

# Define adjacent keys on a MacBook keyboard by keycode
# This is a simplified version - you would need to expand this
ADJACENT_KEYS = {
    # Example: keycode -> list of adjacent keycodes
    0: [1, 13],  # A -> S, Q
    1: [0, 2, 13, 14],  # S -> A, D, Q, W
    # ... more key mappings ...
}

# Keys to ignore when pressed together (common shortcuts)
IGNORED_COMBOS = [
    # Example: set of keycodes for Command+Space, etc.
    {55, 49},  # Command + Space
    # ... more combinations ...
]

# Function to play a meow sound
def play_meow():
    global last_meow_time
    current_time = time.time()
    
    # Only play if enough time has passed since the last meow
    if current_time - last_meow_time >= MIN_MEOW_INTERVAL:
        try:
            playsound(MEOW_SOUND)
            last_meow_time = current_time
        except Exception as e:
            print("Error playing sound:", e)

# Function to check if keys are adjacent
def are_keys_adjacent(keys):
    if len(keys) < 4:
        return False
        
    # Check if at least 3 keys are adjacent to each other
    for key1 in keys:
        adjacent_count = 0
        for key2 in keys:
            if key1 != key2 and key2 in ADJACENT_KEYS.get(key1, []):
                adjacent_count += 1
        
        # If this key is adjacent to at least 3 other keys, it's a cluster
        if adjacent_count >= 3:
            return True
    
    return False

# Function to detect cat-like typing
def is_cat_typing():
    # Clean up old key presses (older than 0.5 seconds)
    current_time = time.time()
    active_keys = [k for k, t in pressed_keys.items() if current_time - t < 0.5]
    
    # Need at least 4 keys for cat typing
    if len(active_keys) >= 4:
        # Check if the pressed keys match any ignored combos
        for combo in IGNORED_COMBOS:
            if combo.issubset(set(active_keys)):
                return False
        
        # Check if the keys are adjacent (cat-like typing)
        if are_keys_adjacent(active_keys):
            return True
    
    return False

# Callback for the event tap
def event_tap_callback(proxy, event_type, event, refcon):
    global cat_typing_detected, pressed_keys
    
    # Get the keycode
    keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
    
    if event_type == kCGEventKeyDown:
        # Record the key press with timestamp
        pressed_keys[keycode] = time.time()
        print(f"Key pressed: {keycode}, total keys: {len(pressed_keys)}")
        
        # Check if it's cat typing
        if is_cat_typing():
            if not cat_typing_detected:
                print("Cat typing detected! Meow!")
                cat_typing_detected = True
                # Play meow sound
                threading.Thread(target=play_meow, daemon=True).start()
                # Show notification
                threading.Thread(
                    target=lambda: rumps.notification("Pawse", "🐾", "Cat typing detected! Blocking keystrokes..."),
                    daemon=True
                ).start()
            
            # Block the keystroke by returning None
            return None
        else:
            cat_typing_detected = False
    
    elif event_type == kCGEventKeyUp:
        # Remove the key from pressed keys
        if keycode in pressed_keys:
            del pressed_keys[keycode]
            print(f"Key released: {keycode}, remaining keys: {len(pressed_keys)}")
        
        # If we were blocking, but no longer detect cat typing, stop blocking
        if cat_typing_detected and not is_cat_typing():
            cat_typing_detected = False
    
    # Allow the keystroke to pass through
    return event

class QuartzPawseApp(rumps.App):
    def __init__(self):
        super(QuartzPawseApp, self).__init__("Pawse", icon="pawse_icon.png")
        self.menu = ["Stop Pawse"]  # Start with Stop Pawse as the menu item
        self.tap = None
        self.tap_thread = None
        self.running = True
        
        # Start Pawse automatically
        self.start_event_tap()
        rumps.notification("Pawse", "🐾", "Pawse is now active with Quartz event monitoring!")
        print("Pawse started - monitoring for cat typing using Quartz API")

    @rumps.clicked("Stop Pawse")
    def toggle_pawse(self, sender):
        if not self.running:
            # Start Pawse
            self.running = True
            self.start_event_tap()
            sender.title = "Stop Pawse"
            rumps.notification("Pawse", "🐾", "Pawse is now active!")
            print("Pawse started - monitoring for cat typing")
        else:
            # Stop Pawse
            self.running = False
            self.stop_event_tap()
            sender.title = "Start Pawse"
            rumps.notification("Pawse", "🐾", "Pawse is now stopped!")
            print("Pawse stopped")

    def start_event_tap(self):
        # Start in a separate thread to not block the main app
        self.tap_thread = threading.Thread(target=self._create_event_tap, daemon=True)
        self.tap_thread.start()

    def _create_event_tap(self):
        # Create an event tap to monitor keyboard events
        self.tap = CGEventTapCreate(
            kCGHIDEventTap,  # Tap at the point where HID events enter the system
            0,  # Place the tap at the beginning of the event tap chain
            0,  # Options (0 = default)
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
            
            # Run the loop (this will block until the tap is disabled)
            CFRunLoopRun()
        else:
            print("Failed to create event tap. Make sure the app has accessibility permissions.")

    def stop_event_tap(self):
        if self.tap:
            # Disable the event tap
            CGEventTapEnable(self.tap, False)
            print("Quartz event tap disabled")

if __name__ == "__main__":
    app = QuartzPawseApp()
    app.run() 