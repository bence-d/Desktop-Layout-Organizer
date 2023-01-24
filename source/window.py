import tkinter as tk
import tkinter.ttk as ttk

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
        self.window.title("Change Preset")
        self.var = tk.StringVar()
        self.window.windowWidth = 250
        self.window.windowHeight = 400
        self.window.geometry("{}x{}".format(self.window.windowWidth, self.window.windowHeight))
        self.window.resizable(0, 0)

        # Window Column Config
        self.window.columnconfigure(0, weight=1)
        
        # Window Window Elements
        self.label = tk.Label(self.window, text="Enter preset name:")
        self.label.grid(column=0, row=0, pady=10)

        self.inputfield = tk.Entry(self.window)
        self.inputfield.grid(column=0, row=1, pady=10)

        button = tk.Button(self.window, text="OK", command=self.destroyWindow)
        button.grid(column=0, row=2, pady=10, ipadx=30)
        
        InputDialog.center_window(self)

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
        self.window = tk.Tk(className="New Preset")

        # Window Configuration
        self.window.title("Input Dialog")
        self.var = tk.StringVar()
        self.window.windowWidth = 250
        self.window.windowHeight = 400
        self.window.geometry("{}x{}".format(self.window.windowWidth, self.window.windowHeight))
        self.window.resizable(0, 0)

        # Window Column Config
        self.window.columnconfigure(0, weight=1)
        
        # Window Window Elements
        self.label = tk.Label(self.window, text="Enter preset name:")
        self.label.grid(column=0, row=0, pady=10)

        self.inputfield = tk.Entry(self.window)
        self.inputfield.grid(column=0, row=1, pady=10)

        button = tk.Button(self.window, text="OK", command=self.destroyWindow)
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
    def __init__(self):

        # Elements
        self.window = tk.Tk(className="Main Window")
        self.windowWidth = 250
        self.windowHeight = 400
        self.window.geometry("{}x{}".format(self.windowWidth, self.windowHeight))
        self.window.resizable(0, 0)

        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)

        btn_pr_add = tk.Button(text="New Preset", height=2,width=15,command=self.new_preset)
        btn_pr_add.grid(column=1, row=0, pady=10)
        #btn_pr_add.pack()

        btn_pr_ch = tk.Button(text="Change Preset", height=2,width=15)
        btn_pr_ch.grid(column=1, row=1, pady=10)
        #btn_pr_ch.pack()

        btn_pr_del = tk.Button(text="Delete Preset", height=2,width=15)
        btn_pr_del.grid(column=1, row=2, pady=10)
        #btn_pr_del.pack()

        btn_pr_load = tk.Button(text="Load Preset", height=2, width=15)
        btn_pr_load.grid(column=1, row=3, pady=10)

        btn_pr_sv = tk.Button(text="Save Preset", height=2, width=15)
        btn_pr_sv.grid(column=1, row=4, pady=10)

        inputField = tk.Entry()

        self.label1 = tk.Label(text="Current Preset: Default")
        self.label1.grid(column=1, row=5, pady=10)

        self.center_window()
        self.window.mainloop()
    
    def center_window(self):
        x = (self.window.winfo_screenwidth() // 2) - (self.windowWidth // 2)
        y = (self.window.winfo_screenheight() // 2) - (self.windowHeight // 2) -50

        self.window.geometry('{}x{}+{}+{}'.format(self.windowWidth, self.windowHeight, x, y))

    def new_preset(self):
        print("-> creating new preset...")
        res = InputDialog().show()
        print("-> recieved input: " + res)
        self.label1.configure(text="Current Preset: " + res)

GUI()