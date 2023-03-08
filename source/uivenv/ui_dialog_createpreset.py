import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from presetmanager import presetmanager as pmgr
from ui_dialog_input import InputDialog

class CreatePreset():
    response = ""

    def __init__(self):
        # Elements
        self.window = tk.Tk(className="Create Preset")

        # Window Configuration
        self.window.title("New Preset")
        self.var = tk.StringVar()
        self.window.windowWidth = 250
        self.window.windowHeight = 300
        self.window.geometry("{}x{}".format(self.window.windowWidth, self.window.windowHeight))
        self.window.resizable(0, 0)

        # Window Column Config
        self.window.columnconfigure(0, weight=1)
        
        # Window Window Elements
        self.label = ttk.Label(self.window, text="Name:")
        self.label.grid(column=0, row=0, pady=10)

        self.input_presName = ttk.Entry(self.window)
        self.input_presName.grid(column=0, row=1, pady=10)

        # Window Window Elements
        self.label = ttk.Label(self.window, text="Description:")
        self.label.grid(column=0, row=2, pady=10)

        self.input_desc = ttk.Entry(self.window)
        self.input_desc.grid(column=0, row=3, pady=10, ipadx=20, ipady=40)

        button = ttk.Button(self.window, text="Create", command=self.createPreset)
        button.grid(column=0, row=4, pady=10, ipadx=30)
        
        InputDialog.center_window(self)

    def createPreset(self):
        pmgr.create_preset(self.input_presName.get(), self.input_desc.get())
        self.destroyWindow()

    def destroyWindow(self):
        self.response = "created"
        self.label.config(text = "value: {}".format(self.var))
        self.window.destroy()

    def show(self):
        path = (Path(__file__).parent / "Lib\\site-packages\\sv_ttk\\sv.tcl").resolve()
        self.window.tk.call("source", str(path))
        self.window.tk.call("set_theme", "light")
        self.window.mainloop()
        self.window.deiconify()
        self.window.wait_window()
        return self.response