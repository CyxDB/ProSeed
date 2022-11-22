import tkinter as tk
from tkinter import ttk
class Navbar(tk.Frame): ...
class Toolbar(tk.Frame): ...
class Statusbar(tk.Frame): ...
class Main(tk.Frame):
    def __init__(self, parent,*args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.p1_name = tk.StringVar(name="p1_name")
        self.p2_name = tk.StringVar(name="p2_name")
        self.p1_score = tk.IntVar(value=0)
        self.p2_score = tk.IntVar(value=0)
        
        # Top Row
        # Player 1 
        tk.Entry(self, textvariable=self.p1_name).grid(row=0, column=0)
        tk.Spinbox(self, textvariable=self.p1_score, width=3, from_=-99, to=99).grid(row=0, column=1)
        
        # Switch Players
        tk.Button(self, text='<->', command=self.switch_players).grid(row=0, column=2)
        
        # Player 2
        tk.Spinbox(self, textvariable=self.p2_score, width=3, from_=-99, to=99).grid(row=0, column=3)
        tk.Entry(self, textvariable=self.p2_name).grid(row=0, column=4)
        
        
        # Middle Row
        choices = ["Extav", "Cyxie"] #array of player names to select from Comboboxes. This should be blank normally.
        # P1 Listbox of names
        self.lb1 = ttk.Combobox(self, values = choices)
        self.lb1.grid(row=1, column=0, columnspan=2)
        
        # Entry box for the current tournament phase. (Winners R1, Losers R2, Winners-Final...)
        self.phase = tk.StringVar()
        tk.Entry(self, textvariable=self.phase).grid(row=1, column=2)
        
        self.lb2 = ttk.Combobox(self, values = choices)
        self.lb2.grid(row=1, column=3, columnspan=2)
        
        #Bottom Row
        self.btn_update = tk.Button(self, text="Update Files", command=self.update_files)
        self.btn_update.grid(row=2, column=1, columnspan=3)
        
    
    def switch_players(self):
        # Retrieve names
        p1n = self.p1_name.get()
        p2n = self.p2_name.get()
        # Retrieve scores
        p1s = self.p1_score.get()
        p2s = self.p2_score.get()
        
        #Swap names and scores
        self.p1_name.set(p2n)
        self.p2_name.set(p1n)
        self.p1_score.set(p2s)
        self.p2_score.set(p1s)
        
        #Logging to console the action for now
        print("Swapped player names & scores")
        
    def update_files(self):
        files = {
            "p1name.txt": self.p1_name.get(),
            "p2name.txt": self.p1_name.get(),
            "p1score.txt": str(self.p1_score.get()),
            "p2score.txt": str(self.p2_score.get()),
            "phase.txt": self.phase.get()
        }
        for e in files:
            f = open(e, "w")
            f.write(files[e])
            f.close()

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.statusbar = Statusbar(self)
        self.toolbar = Toolbar(self)
        self.navbar = Navbar(self)
        self.main = Main(self, width=500, height=500, bg='red')

        self.statusbar.pack(side="bottom", fill="x")
        self.toolbar.pack(side="top", fill="x")
        self.navbar.pack(side="left", fill="y")
        self.main.pack(side="right", fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("ProSeed")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()