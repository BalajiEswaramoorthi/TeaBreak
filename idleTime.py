from ctypes import Structure, c_uint, byref, sizeof, windll
import logging

class LastInputInfo(Structure):
    """Structure for last input info"""
    _fields_ = [('cb_size', c_uint), ('dw_time', c_uint)]

class IdleTime:
    """Class to handle idle time"""
    def __init__(self):
        """
        Init IdleTime
        """
        self.threshold = 45
        self.idle_time = 0
        self.idle_status = False

    def update_idle_time_threshold(self, threshold):
        """
        Update idle time threshold

        Input: idle time threshold
        Output: void
        """
        self.threshold = threshold

    def get_idle_status(self):
        """
        Get idle status

        Output:
            True    : System idle time exceeded the configured limit
            False   : System is not idle
        """
        last_input_info = LastInputInfo()
        last_input_info.cb_size = sizeof(last_input_info)
        windll.user32.GetLastInputInfo(byref(last_input_info))
        ms = windll.kernel32.GetTickCount() - last_input_info.dw_time

        self.idle_time = ms / 1000.0
        self.idle_status = True if self.idle_time >= self.threshold else False

        logging.info("Idle Time : %d Idle Status: %d", self.idle_time, self.idle_status)
        return self.idle_status