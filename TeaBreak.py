import tkinter as tk
from tkinter import scrolledtext
import logging
from PIL import Image, ImageTk
import base64
from io import BytesIO

import KeyPress
import winInhibit
import pic2str
import idleTime

class TextHandler(logging.Handler):
    def __init__(self, text):
        logging.Handler.__init__(self)
        self.text = text
        self.debug_log_format = "%(asctime)s %(module)-15s %(funcName)-20.20s %(lineno)4d [%(levelname)-s]: %(message)s"
        self.log_format = "[%(asctime)s] [%(levelname)-s]: %(message)s"
        self.formatter = logging.Formatter(fmt=self.log_format, datefmt='%Y-%m-%d %H:%M:%S')

    def emit(self, record):
        msg = self.formatter.format(record)
        self.text.insert(tk.END, msg + "\n")
        self.text.see(tk.END)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TeaBreak")

        byte_data = base64.b64decode(pic2str.pngIcon)
        image_data = BytesIO(byte_data)
        print(image_data)
        image = Image.open(image_data)

        #iconImg = Image.open("teaBreak.png")
        photo = ImageTk.PhotoImage(image)
        self.iconphoto(False, photo)

        # Frame for console logs
        self.frame1 = tk.Frame(self, width=800, height=400)
        self.frame1.pack(fill="both", expand=True, padx=5, pady=5)

        self.console = scrolledtext.ScrolledText(self.frame1)
        self.console.pack(fill="both", expand=True)

        # Configure logging
        logging.basicConfig(level=logging.DEBUG)
        text_handler = TextHandler(self.console)
        logging.getLogger().addHandler(text_handler)

        # Frame for input buttons
        self.frame2 = tk.Frame(self)
        self.frame2.pack(fill="x", padx=5, pady=5)

        self.enableButton = tk.Button(self.frame2, text="Enable", command=self.enableTeabreak)
        self.enableButton.pack(side="left")

        self.disableButton = tk.Button(self.frame2, text="Disable", command=self.disableTeabreak)
        self.disableButton.pack(side="left")

        self.exitButton = tk.Button(self.frame2, text="Quit", command=self.quit)
        self.exitButton.pack(side="left")

        self.winInhibit = winInhibit.WindowsInhibitor()
        self.keyPress = KeyPress.KeyPress()

        self.winInhibit.inhibit()
        self.after(1000, self.checkIdleTime)
        self.activeState = True
        self.idleTime = idleTime.IdleTime()

    def disableTeabreak(self):
        if self.activeState == True:
            self.winInhibit.uninhibit()
        self.activeState = False
        logging.info("current active state = %d", self.activeState)

    def enableTeabreak(self):
        if self.activeState == False:
            self.winInhibit.inhibit()
        self.activeState =  True
        logging.info("current active state = %d", self.activeState)

    def checkIdleTime(self):
        if self.activeState == True:
            if (self.idleTime.get_idle_status() == True):
                self.keyPress.key_press()
        self.after(3000, self.checkIdleTime)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format = '%(asctime)s %(module)-15s %(funcName)-20.20s %(lineno)4d [%(levelname)-s]: %(message)s')
    app = Application()
    app.mainloop()