# MacBook keyboard layout with keycodes
# This maps each key to its adjacent keys on a standard MacBook keyboard

# MacOS keycodes for common keys
# Format: KEY_NAME: KEYCODE

# Row 1 (number row)
# ` 1 2 3 4 5 6 7 8 9 0 - =
KEY_GRAVE = 50       # `
KEY_1 = 18           # 1
KEY_2 = 19           # 2
KEY_3 = 20           # 3
KEY_4 = 21           # 4
KEY_5 = 23           # 5
KEY_6 = 22           # 6
KEY_7 = 26           # 7
KEY_8 = 28           # 8
KEY_9 = 25           # 9
KEY_0 = 29           # 0
KEY_MINUS = 27       # -
KEY_EQUAL = 24       # =
KEY_DELETE = 51      # Delete/Backspace
KEY_ESCAPE = 53      # Escape key

# Row 2
# tab q w e r t y u i o p [ ] \
KEY_TAB = 48         # Tab
KEY_Q = 12           # Q
KEY_W = 13           # W
KEY_E = 14           # E
KEY_R = 15           # R
KEY_T = 17           # T
KEY_Y = 16           # Y
KEY_U = 32           # U
KEY_I = 34           # I
KEY_O = 31           # O
KEY_P = 35           # P
KEY_LEFTBRACKET = 33 # [
KEY_RIGHTBRACKET = 30 # ]
KEY_BACKSLASH = 42   # \

# Row 3
# caps a s d f g h j k l ; ' return
KEY_CAPSLOCK = 57    # Caps Lock
KEY_A = 0            # A
KEY_S = 1            # S
KEY_D = 2            # D
KEY_F = 3            # F
KEY_G = 5            # G
KEY_H = 4            # H
KEY_J = 38           # J
KEY_K = 40           # K
KEY_L = 37           # L
KEY_SEMICOLON = 41   # ;
KEY_QUOTE = 39       # '
KEY_RETURN = 36      # Return/Enter

# Row 4
# shift z x c v b n m , . / shift
KEY_SHIFT_LEFT = 56  # Left Shift
KEY_Z = 6            # Z
KEY_X = 7            # X
KEY_C = 8            # C
KEY_V = 9            # V
KEY_B = 11           # B
KEY_N = 45           # N
KEY_M = 46           # M
KEY_COMMA = 43       # ,
KEY_PERIOD = 47      # .
KEY_SLASH = 44       # /
KEY_SHIFT_RIGHT = 60 # Right Shift

# Row 5 (bottom row)
# fn control option command space command option
KEY_FN = 63          # Fn
KEY_CONTROL_LEFT = 59 # Left Control
KEY_OPTION_LEFT = 58  # Left Option/Alt
KEY_COMMAND_LEFT = 55 # Left Command
KEY_SPACE = 49        # Space
KEY_COMMAND_RIGHT = 54 # Right Command
KEY_OPTION_RIGHT = 61  # Right Option/Alt
KEY_CONTROL_RIGHT = 62 # Right Control

# Arrow keys
KEY_LEFT = 123       # Left Arrow
KEY_RIGHT = 124      # Right Arrow
KEY_DOWN = 125       # Down Arrow
KEY_UP = 126         # Up Arrow

# Define adjacent keys on a MacBook keyboard
# This maps each key to its adjacent keys
ADJACENT_KEYS = {
    # Row 1 (number row)
    KEY_GRAVE: [KEY_1, KEY_TAB, KEY_ESCAPE],
    KEY_1: [KEY_GRAVE, KEY_2, KEY_Q, KEY_TAB],
    KEY_2: [KEY_1, KEY_3, KEY_Q, KEY_W],
    KEY_3: [KEY_2, KEY_4, KEY_W, KEY_E],
    KEY_4: [KEY_3, KEY_5, KEY_E, KEY_R],
    KEY_5: [KEY_4, KEY_6, KEY_R, KEY_T],
    KEY_6: [KEY_5, KEY_7, KEY_T, KEY_Y],
    KEY_7: [KEY_6, KEY_8, KEY_Y, KEY_U],
    KEY_8: [KEY_7, KEY_9, KEY_U, KEY_I],
    KEY_9: [KEY_8, KEY_0, KEY_I, KEY_O],
    KEY_0: [KEY_9, KEY_MINUS, KEY_O, KEY_P],
    KEY_MINUS: [KEY_0, KEY_EQUAL, KEY_P, KEY_LEFTBRACKET],
    KEY_EQUAL: [KEY_MINUS, KEY_DELETE, KEY_LEFTBRACKET, KEY_RIGHTBRACKET],
    KEY_DELETE: [KEY_EQUAL, KEY_RIGHTBRACKET, KEY_BACKSLASH],
    
    # Row 2
    KEY_TAB: [KEY_GRAVE, KEY_1, KEY_Q, KEY_CAPSLOCK],
    KEY_Q: [KEY_TAB, KEY_1, KEY_2, KEY_W, KEY_A, KEY_CAPSLOCK],
    KEY_W: [KEY_Q, KEY_2, KEY_3, KEY_E, KEY_S, KEY_A],
    KEY_E: [KEY_W, KEY_3, KEY_4, KEY_R, KEY_D, KEY_S],
    KEY_R: [KEY_E, KEY_4, KEY_5, KEY_T, KEY_F, KEY_D],
    KEY_T: [KEY_R, KEY_5, KEY_6, KEY_Y, KEY_G, KEY_F],
    KEY_Y: [KEY_T, KEY_6, KEY_7, KEY_U, KEY_H, KEY_G],
    KEY_U: [KEY_Y, KEY_7, KEY_8, KEY_I, KEY_J, KEY_H],
    KEY_I: [KEY_U, KEY_8, KEY_9, KEY_O, KEY_K, KEY_J],
    KEY_O: [KEY_I, KEY_9, KEY_0, KEY_P, KEY_L, KEY_K],
    KEY_P: [KEY_O, KEY_0, KEY_MINUS, KEY_LEFTBRACKET, KEY_SEMICOLON, KEY_L],
    KEY_LEFTBRACKET: [KEY_P, KEY_MINUS, KEY_EQUAL, KEY_RIGHTBRACKET, KEY_QUOTE, KEY_SEMICOLON],
    KEY_RIGHTBRACKET: [KEY_LEFTBRACKET, KEY_EQUAL, KEY_DELETE, KEY_BACKSLASH, KEY_RETURN, KEY_QUOTE],
    KEY_BACKSLASH: [KEY_RIGHTBRACKET, KEY_DELETE, KEY_RETURN],
    
    # Row 3
    KEY_CAPSLOCK: [KEY_TAB, KEY_Q, KEY_A, KEY_SHIFT_LEFT],
    KEY_A: [KEY_CAPSLOCK, KEY_Q, KEY_W, KEY_S, KEY_Z, KEY_SHIFT_LEFT],
    KEY_S: [KEY_A, KEY_W, KEY_E, KEY_D, KEY_X, KEY_Z],
    KEY_D: [KEY_S, KEY_E, KEY_R, KEY_F, KEY_C, KEY_X],
    KEY_F: [KEY_D, KEY_R, KEY_T, KEY_G, KEY_V, KEY_C],
    KEY_G: [KEY_F, KEY_T, KEY_Y, KEY_H, KEY_B, KEY_V],
    KEY_H: [KEY_G, KEY_Y, KEY_U, KEY_J, KEY_N, KEY_B],
    KEY_J: [KEY_H, KEY_U, KEY_I, KEY_K, KEY_M, KEY_N],
    KEY_K: [KEY_J, KEY_I, KEY_O, KEY_L, KEY_COMMA, KEY_M],
    KEY_L: [KEY_K, KEY_O, KEY_P, KEY_SEMICOLON, KEY_PERIOD, KEY_COMMA],
    KEY_SEMICOLON: [KEY_L, KEY_P, KEY_LEFTBRACKET, KEY_QUOTE, KEY_SLASH, KEY_PERIOD],
    KEY_QUOTE: [KEY_SEMICOLON, KEY_LEFTBRACKET, KEY_RIGHTBRACKET, KEY_RETURN, KEY_SLASH],
    KEY_RETURN: [KEY_QUOTE, KEY_RIGHTBRACKET, KEY_BACKSLASH, KEY_SHIFT_RIGHT],
    
    # Row 4
    KEY_SHIFT_LEFT: [KEY_CAPSLOCK, KEY_A, KEY_Z, KEY_FN, KEY_CONTROL_LEFT],
    KEY_Z: [KEY_SHIFT_LEFT, KEY_A, KEY_S, KEY_X, KEY_FN, KEY_CONTROL_LEFT],
    KEY_X: [KEY_Z, KEY_S, KEY_D, KEY_C, KEY_OPTION_LEFT, KEY_FN],
    KEY_C: [KEY_X, KEY_D, KEY_F, KEY_V, KEY_OPTION_LEFT, KEY_COMMAND_LEFT],
    KEY_V: [KEY_C, KEY_F, KEY_G, KEY_B, KEY_COMMAND_LEFT, KEY_SPACE],
    KEY_B: [KEY_V, KEY_G, KEY_H, KEY_N, KEY_SPACE],
    KEY_N: [KEY_B, KEY_H, KEY_J, KEY_M, KEY_SPACE],
    KEY_M: [KEY_N, KEY_J, KEY_K, KEY_COMMA, KEY_SPACE, KEY_COMMAND_RIGHT],
    KEY_COMMA: [KEY_M, KEY_K, KEY_L, KEY_PERIOD, KEY_COMMAND_RIGHT, KEY_OPTION_RIGHT],
    KEY_PERIOD: [KEY_COMMA, KEY_L, KEY_SEMICOLON, KEY_SLASH, KEY_OPTION_RIGHT, KEY_CONTROL_RIGHT],
    KEY_SLASH: [KEY_PERIOD, KEY_SEMICOLON, KEY_QUOTE, KEY_SHIFT_RIGHT, KEY_CONTROL_RIGHT],
    KEY_SHIFT_RIGHT: [KEY_SLASH, KEY_QUOTE, KEY_RETURN, KEY_CONTROL_RIGHT],
    
    # Row 5 (bottom row)
    KEY_FN: [KEY_SHIFT_LEFT, KEY_Z, KEY_X, KEY_CONTROL_LEFT, KEY_OPTION_LEFT],
    KEY_CONTROL_LEFT: [KEY_SHIFT_LEFT, KEY_Z, KEY_FN, KEY_OPTION_LEFT],
    KEY_OPTION_LEFT: [KEY_CONTROL_LEFT, KEY_FN, KEY_X, KEY_C, KEY_COMMAND_LEFT],
    KEY_COMMAND_LEFT: [KEY_OPTION_LEFT, KEY_C, KEY_V, KEY_SPACE],
    KEY_SPACE: [KEY_COMMAND_LEFT, KEY_V, KEY_B, KEY_N, KEY_M, KEY_COMMAND_RIGHT],
    KEY_COMMAND_RIGHT: [KEY_SPACE, KEY_M, KEY_COMMA, KEY_OPTION_RIGHT],
    KEY_OPTION_RIGHT: [KEY_COMMAND_RIGHT, KEY_COMMA, KEY_PERIOD, KEY_CONTROL_RIGHT],
    KEY_CONTROL_RIGHT: [KEY_OPTION_RIGHT, KEY_PERIOD, KEY_SLASH, KEY_SHIFT_RIGHT],
    
    # Arrow keys
    KEY_LEFT: [KEY_DOWN, KEY_RIGHT],
    KEY_DOWN: [KEY_LEFT, KEY_RIGHT, KEY_UP],
    KEY_RIGHT: [KEY_LEFT, KEY_DOWN, KEY_UP],
    KEY_UP: [KEY_DOWN, KEY_RIGHT],
    
    # Escape key
    KEY_ESCAPE: [KEY_GRAVE, KEY_1],
}

# Keys to ignore when pressed together (common shortcuts)
IGNORED_COMBOS = [
    {KEY_COMMAND_LEFT, KEY_SPACE},  # Command + Space (Spotlight)
    {KEY_COMMAND_LEFT, KEY_TAB},    # Command + Tab (App Switcher)
    {KEY_COMMAND_LEFT, KEY_SHIFT_LEFT},  # Command + Shift
    {KEY_COMMAND_LEFT, KEY_OPTION_LEFT},  # Command + Option
    {KEY_COMMAND_LEFT, KEY_CONTROL_LEFT},  # Command + Control
    {KEY_SHIFT_LEFT, KEY_CONTROL_LEFT},  # Shift + Control
    {KEY_OPTION_LEFT, KEY_CONTROL_LEFT},  # Option + Control
    {KEY_SHIFT_LEFT, KEY_OPTION_LEFT},  # Shift + Option
    {KEY_COMMAND_LEFT, KEY_C},  # Command + C (Copy)
    {KEY_COMMAND_LEFT, KEY_V},  # Command + V (Paste)
    {KEY_COMMAND_LEFT, KEY_X},  # Command + X (Cut)
    {KEY_COMMAND_LEFT, KEY_Z},  # Command + Z (Undo)
    {KEY_COMMAND_LEFT, KEY_A},  # Command + A (Select All)
    {KEY_COMMAND_LEFT, KEY_S},  # Command + S (Save)
    {KEY_COMMAND_LEFT, KEY_W},  # Command + W (Close Window)
    {KEY_COMMAND_LEFT, KEY_Q},  # Command + Q (Quit App)
] 