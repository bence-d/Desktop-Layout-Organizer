import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from dlo_library import presetmanager as pmgr
from ui_dialog_input import InputDialog

class ChangePreset():
    response = ""

    def __init__(self):
        # Elements
        self.window = tk.Tk(className="Change Preset")

        # Window Configuration
        self.window.title("Preset Selector")
        self.var = tk.StringVar()
        self.window.windowWidth = 250
        self.window.windowHeight = 150
        self.window.geometry("{}x{}".format(self.window.windowWidth, self.window.windowHeight))
        self.window.resizable(0, 0)

        # Window Column Config
        self.window.columnconfigure(0, weight=1)
        
        # Window Window Elements
        self.label = ttk.Label(self.window, text="Choose your preset:")
        self.label.grid(column=0, row=0, pady=10)

        # Getting preset list

        presetList = pmgr.get_all_entries()

        # turning it only to a list of names...
        presetListNames = []

        presetListNames.append("[preset]   ")
        self.presetsSaved = True
        if presetList:
            for actPres in presetList:
                presetListNames.append(actPres.name)
        else:
            self.presetsSaved = False

        # variable that holds value of selection in preset_menu
        self.selectedOption = tk.StringVar(self.window, " ")

        preset_menu = ttk.OptionMenu(self.window, self.selectedOption, *presetListNames)

        if not self.presetsSaved:
            presetListNames = []
            presetListNames.append("<no presets saved>   ")
            preset_menu = ttk.OptionMenu(self.window, self.selectedOption, *presetListNames)
            preset_menu.configure(state="disabled")

        preset_menu.grid(column=0, row=1, pady=10)

        button = ttk.Button(self.window, text="OK", command=self.destroyWindow)
        button.grid(column=0, row=2, pady=10, ipadx=30)
        
        InputDialog.center_window(self)

    def destroyWindow(self):
        self.response = self.selectedOption.get()
        self.label.config(text = "value: {}".format(self.var))
        self.window.destroy()

    def show(self):
        path = (Path(__file__).parent / "Lib\\site-packages\\sv_ttk\\sv.tcl").resolve()
        self.window.tk.call("source", str(path))
        self.window.tk.call("set_theme", "light")
        self.window.deiconify()
        self.window.wait_window()
        print("RETURNING: " + self.response)
        return self.response