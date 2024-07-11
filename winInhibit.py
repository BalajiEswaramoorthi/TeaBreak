import logging
import ctypes

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001

class WindowsInhibitor:
    """Class to prevent Windows from going to sleep"""
    @staticmethod
    def inhibit():
        """Prevent Windows from going to sleep"""
        logging.info("Preventing Windows from going to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)

    @staticmethod
    def uninhibit():
        """Allow Windows to go to sleep"""
        logging.info("Allowing Windows to go to sleep")
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)