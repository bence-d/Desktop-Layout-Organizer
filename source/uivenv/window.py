import tkinter as tk
import tkinter.ttk as ttk
import sv_ttk
from pathlib import Path
from dlo_library import presetmanager as pmgr

class CreatePresetDialog():
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

class ChangePresetDialog():
    windowWidth = 250
    windowHeight = 150

    def center_window(self):
        x = (self.window.winfo_screenwidth() // 2) - (self.windowWidth // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.windowHeight // 2) -50
        self.window.geometry('{}x{}+{}+{}'.format(self.windowWidth, self.windowHeight, x, y))

    valueToReturn = ""

    def __init__(self):
        # Elements
        self.window = tk.Tk(className="Change Preset")

        # Window Configuration
        self.window.title("Preset Selector")
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
        self.value_inside = tk.StringVar(self.window, " ")

        preset_menu = ttk.OptionMenu(self.window, self.value_inside, *presetListNames)

        if not self.presetsSaved:
            presetListNames = []
            presetListNames.append("<no presets saved>   ")
            preset_menu = ttk.OptionMenu(self.window, self.value_inside, *presetListNames)
            preset_menu.configure(state="disabled")

        preset_menu.grid(column=0, row=1, pady=10)

        button = ttk.Button(self.window, text="OK", command=self.destroyWindow)
        button.grid(column=0, row=2, pady=10, ipadx=30)
        
        InputDialog.center_window(self)

    def destroyWindow(self):
        self.valueToReturn = self.value_inside.get()
        self.label.config(text = "value: {}".format(self.var))
        self.window.destroy()

    def show(self):
        path = (Path(__file__).parent / "Lib\\site-packages\\sv_ttk\\sv.tcl").resolve()
        self.window.tk.call("source", str(path))
        self.window.tk.call("set_theme", "light")
        self.window.deiconify()
        self.window.wait_window()
        print("RETURNING: " + self.valueToReturn)
        return self.valueToReturn

class DeletePresetDialog():
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

class InputDialog():
    windowWidth = 250
    windowHeight = 150

    def center_window(self):
        x = (self.window.winfo_screenwidth() // 2) - (self.windowWidth // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.windowHeight // 2) -50
        self.window.geometry('{}x{}+{}+{}'.format(self.windowWidth, self.windowHeight, x, y))

    valueToReturn = ""

    def __init__(self):
        # Elements
        self.window = ttk.Tk(className="New Preset")

        # Window Configuration
        self.window.title("Input Dialog")
        self.var = tk.StringVar()
        self.window.windowWidth = 250
        self.window.windowHeight = 400
        self.window.geometry("{}x{}".format(self.window.windowWidth, self.window.windowHeight))
        self.window.resizable(0, 0)
        sv_ttk.set_theme("dark")

        # Window Column Config
        self.window.columnconfigure(0, weight=1)
        
        # Window Window Elements
        self.label = ttk.Label(self.window, text="Enter preset name:")
        self.label.grid(column=0, row=0, pady=10)

        self.inputfield = ttk.Entry(self.window)
        self.inputfield.grid(column=0, row=1, pady=10)

        button = ttk.Button(self.window, text="OK", command=self.destroyWindow)
        button.grid(column=0, row=2, pady=10, ipadx=30)
        #self.label.pack(side="top", fill="x")
        #self.inputfield.pack(side="top")
        #button.pack()
        
        InputDialog.center_window(self)

    def destroyWindow(self):
        self.valueToReturn = self.inputfield.get()
        self.label.config(text = "value: {}".format(self.var))
        self.window.destroy()

    def show(self):
        self.window.deiconify()
        self.window.wait_window()
        return self.valueToReturn

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
        #btn_pr_add.pack()

        btn_pr_ch = ttk.Button(text="Change Preset", width=15, command=self.change_preset)
        btn_pr_ch.grid(column=1, row=1, pady=10)
        #btn_pr_ch.pack()

        btn_pr_del = ttk.Button(text="Delete Preset", width=15, command=self.delete_preset)
        btn_pr_del.grid(column=1, row=2, pady=10)
        #btn_pr_del.pack()

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
        # print("-> creating new preset...")
        res = CreatePresetDialog().show()
        # print("-> recieved input: " + res)
        self.currentPreset = res
        self.refreshPresetLabel()

    def change_preset(self):
        # print("-> selecting preset...")
        res = ChangePresetDialog().show()
        # print("-> recieved input: " + res)
        if res != "[preset]" and res != "<no presets saved>   ":
            self.currentPreset = res
            self.refreshPresetLabel()
        else:
            self.currentPreset = "default"
            self.refreshPresetLabel()

    def delete_preset(self):
        # print("-> deleting preset...")
        res = DeletePresetDialog().show()
        # print("-> recieved input: " + res)
        if res == self.currentPreset:
            self.currentPreset = "default"
            self.refreshPresetLabel()

    def load_preset(self):
        # print("-> loading preset...")
        if self.currentPreset != "default":
            pmgr.load_preset(self.currentPreset)
            # print("-> loaded preset...")

    def save_preset(self):
        # print("-> saving preset...")
        if self.currentPreset != "default":
            pmgr.save_preset(self.currentPreset)
            # print("-> saved preset...")

    def refreshPresetLabel(self):
        if self.currentPreset == "default":
            self.label1.config(text="keine Vorlage ausgewählt")
        else:
            self.label1.config(text="Current Preset: " + self.currentPreset)

GUI()