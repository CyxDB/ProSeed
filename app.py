import tkinter as tk

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
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()