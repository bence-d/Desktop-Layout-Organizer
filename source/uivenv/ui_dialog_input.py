class InputDialog:
    # root window is the window that called this class
    @staticmethod
    def center_window(rootWindow):
        x = (rootWindow.window.winfo_screenwidth() // 2) - (rootWindow.window.windowWidth // 2)
        y = (rootWindow.window.winfo_screenheight() // 2) - (rootWindow.window.windowHeight // 2) -50
        rootWindow.window.geometry('{}x{}+{}+{}'.format(rootWindow.window.windowWidth, rootWindow.window.windowHeight, x, y))
