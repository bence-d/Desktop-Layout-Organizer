import tkinter as tk
import tkinter.ttk as ttk
import sv_ttk

class InputDialog:
    
    @staticmethod
    def center_window(self):
        windowWidth = 250
        windowHeight = 150

        x = (self.window.winfo_screenwidth() // 2) - (self.windowWidth // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.windowHeight // 2) -50
        self.window.geometry('{}x{}+{}+{}'.format(self.windowWidth, self.windowHeight, x, y))
