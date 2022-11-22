import tkinter as tk
from tkinter import ttk
import gui_components as gc

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.statusbar = gc.Statusbar(self)
        self.toolbar = gc.Toolbar(self)
        self.navbar = gc.Navbar(self)
        self.main = gc.Main(self, width=500, height=500, bg='red')

        self.statusbar.pack(side="bottom", fill="x")
        #self.toolbar.pack(side="top", fill="x")
        self.navbar.pack(side="left", fill="y")
        self.main.pack(side="right", fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    menubar = gc.Toolbar(root)
    root.title("ProSeed")
    root.config(menu=menubar)
    
    MainApplication(root).pack(side="top", fill="both", expand=True)
    
    root.mainloop()