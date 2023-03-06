import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from dlo_library import presetmanager as pmgr
from ui_dialog_inputdialog import InputDialog

class CreatePreset():
    windowWidth = 250
    windowHeight = 300

    def center_window(self):
        x = (self.window.winfo_screenwidth() // 2) - (self.windowWidth // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.windowHeight // 2) -50
        self.window.geometry('{}x{}+{}+{}'.format(self.windowWidth, self.windowHeight, x, y))

    valueToReturn = ""

    def __init__(self):
        # Elements
        self.window = tk.Tk(className="Create Preset")

        # Window Configuration
        self.window.title("New Preset")
        self.var = tk.StringVar()
        self.window.windowWidth = self.windowWidth
        self.window.windowHeight = self.windowHeight
        self.window.geometry("{}x{}".format(self.window.windowWidth, self.window.windowHeight))
        self.window.resizable(0, 0)

        # Window Column Config
        self.window.columnconfigure(0, weight=1)
        
        # Window Window Elements
        self.label = ttk.Label(self.window, text="Name:")
        self.label.grid(column=0, row=0, pady=10)

        self.input_name = ttk.Entry(self.window)
        self.input_name.grid(column=0, row=1, pady=10)

        # Window Window Elements
        self.label = ttk.Label(self.window, text="Description:")
        self.label.grid(column=0, row=2, pady=10)

        self.input_desc = ttk.Entry(self.window)
        self.input_desc.grid(column=0, row=3, pady=10, ipadx=20, ipady=40)

        button = ttk.Button(self.window, text="Create", command=self.createPreset)
        button.grid(column=0, row=4, pady=10, ipadx=30)
        
        InputDialog.center_window(self)

    def createPreset(self):
        pmgr.create_preset(self.input_name.get(), self.input_desc.get())
        self.destroyWindow()

    def destroyWindow(self):
        self.valueToReturn = "created"
        self.label.config(text = "value: {}".format(self.var))
        self.window.destroy()

    def show(self):
        path = (Path(__file__).parent / "Lib\\site-packages\\sv_ttk\\sv.tcl").resolve()
        self.window.tk.call("source", str(path))
        self.window.tk.call("set_theme", "light")
        self.window.mainloop()
        self.window.deiconify()
        self.window.wait_window()
        return self.valueToReturn