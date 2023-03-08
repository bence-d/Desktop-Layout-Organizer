import tkinter as tk
import tkinter.ttk as ttk
import sv_ttk
from pathlib import Path
from presetmanager import presetmanager as pmgr
from ui_dialog_input import InputDialog
from ui_dialog_createpreset import CreatePreset
from ui_dialog_changepreset import ChangePreset
from ui_dialog_deletepreset import DeletePreset


class GUI():
    currentPreset = "default"
    def __init__(self):

        # Config
        self.window = tk.Tk(className="DLO")
        self.window.title("DLO")
        self.windowWidth = 250
        self.windowHeight = 400
        self.window.geometry("{}x{}".format(self.windowWidth, self.windowHeight))
        self.window.resizable(0, 0)
        sv_ttk.set_theme("light")

        # Grid
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)

        # Elements
        btn_pr_add = ttk.Button(text="New Preset", width=15, command=self.new_preset)
        btn_pr_add.grid(column=1, row=0, pady=10)

        btn_pr_ch = ttk.Button(text="Change Preset", width=15, command=self.change_preset)
        btn_pr_ch.grid(column=1, row=1, pady=10)

        btn_pr_del = ttk.Button(text="Delete Preset", width=15, command=self.delete_preset)
        btn_pr_del.grid(column=1, row=2, pady=10)

        btn_pr_load = ttk.Button(text="Load Preset", width=15, command=self.load_preset)
        btn_pr_load.grid(column=1, row=3, pady=10)

        btn_pr_sv = ttk.Button(text="Save Preset", width=15, command=self.save_preset)
        btn_pr_sv.grid(column=1, row=4, pady=10)

        inputField = ttk.Entry()

        self.label1 = ttk.Label(text="keine Vorlage ausgewählt")
        self.label1.grid(column=1, row=5, pady=10)

        self.center_window()
        self.window.mainloop()
    
    def center_window(self):
        x = (self.window.winfo_screenwidth() // 2) - (self.windowWidth // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.windowHeight // 2) -50

        self.window.geometry('{}x{}+{}+{}'.format(self.windowWidth, self.windowHeight, x, y))

    def new_preset(self):
        res = CreatePreset().show()
        self.currentPreset = res
        self.refreshPresetLabel()

    def change_preset(self):
        res = ChangePreset().show()
        if res != "[preset]" and res != "<no presets saved>   ":
            self.currentPreset = res
            self.refreshPresetLabel()
        else:
            self.currentPreset = "default"
            self.refreshPresetLabel()

    def delete_preset(self):
        res = DeletePreset().show()
        if res == self.currentPreset:
            self.currentPreset = "default"
            self.refreshPresetLabel()

    def load_preset(self):
        if self.currentPreset != "default":
            pmgr.load_preset(self.currentPreset)

    def save_preset(self):
        if self.currentPreset != "default":
            pmgr.save_preset(self.currentPreset)

    def refreshPresetLabel(self):
        if self.currentPreset == "default":
            self.label1.config(text="keine Vorlage ausgewählt")
        else:
            self.label1.config(text="Current Preset: " + self.currentPreset)

GUI()