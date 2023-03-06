import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from dlo_library import presetmanager as pmgr
from ui_dialog_inputdialog import InputDialog

class DeletePreset():
    windowWidth = 250
    windowHeight = 150

    def center_window(self):
        x = (self.window.winfo_screenwidth() // 2) - (self.windowWidth // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.windowHeight // 2) -50
        self.window.geometry('{}x{}+{}+{}'.format(self.windowWidth, self.windowHeight, x, y))

    valueToReturn = ""

    def __init__(self):
        # Elements
        self.window = tk.Tk(className="Delete Preset")

        # Window Configuration
        self.window.title("Deleting Preset")
        self.var = tk.StringVar()
        self.window.windowWidth = 250
        self.window.windowHeight = 400
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
        self.value_inside = tk.StringVar(self.window)
        
        # Set the default value of the variable
        self.value_inside.set("[default]")

        preset_menu = ttk.OptionMenu(self.window, self.value_inside, *presetListNames)
        if not self.presetsSaved:
            presetListNames = []
            presetListNames.append("<no presets saved>   ")
            preset_menu = ttk.OptionMenu(self.window, self.value_inside, *presetListNames)
            preset_menu.configure(state="disabled")

        preset_menu.grid(column=0, row=1, pady=10)

        button = ttk.Button(self.window, text="OK", command=self.delete_selected_preset)
        button.grid(column=0, row=2, pady=10, ipadx=30)
        
        InputDialog.center_window(self)

    def delete_selected_preset(self):
        ## delete preset
        if self.value_inside != "[default]":
            pmgr.delete_preset(self.value_inside.get())

        ## destroy window
        self.destroyWindow()

    def destroyWindow(self):
        self.valueToReturn = self.value_inside.get()
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