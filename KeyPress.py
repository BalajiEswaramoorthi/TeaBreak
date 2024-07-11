import time
import logging
import ctypes

# Define some parameters from the Windows API
SCROLL_LOCK_KEY = 0x91
VK_VOLUME_UP = 0xAF
VK_VOLUME_DOWN = 0xAE
SHIFT_KEY = 0x10

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002

class KeyPress:
    """Class to handle key press events"""
    @staticmethod
    def press_key(hex_key_code):
        """
        Press a key

        Input : Hex code for the key

        Action : Press the key
        """
        extra = ctypes.c_ulong(0)
        ii_ = ctypes.c_ulong(0)
        x = ctypes.c_ulong(0)
        ii_.value = hex_key_code
        x.value = KEYEVENTF_EXTENDEDKEY | 0
        ctypes.windll.user32.keybd_event(ii_, 0, x, 0)

    @staticmethod
    def release_key(hex_key_code):
        """
        Release a key

        Input : Hex code for the key

        Action : Release the key
        """
        extra = ctypes.c_ulong(0)
        ii_ = ctypes.c_ulong(0)
        x = ctypes.c_ulong(0)
        ii_.value = hex_key_code
        x.value = KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP
        ctypes.windll.user32.keybd_event(ii_, 0, x, 0)

    @staticmethod
    def press_key_once(key):
        """
        Press and release a key once
        """
        KeyPress.press_key(key)
        KeyPress.release_key(key)

    def key_press(self):
        """
        Press the SHIFT key
        """
        self.press_key_once(SHIFT_KEY)