import tkinter as tk
from tkinter import ttk

class Main(tk.Frame):

    choices = ['Extav', 'Cyxie'] #array of player names to select from Comboboxes. This should be blank normally.
    
    def __init__(self, parent,*args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.p1_name = tk.StringVar(name='p1_name')
        self.p2_name = tk.StringVar(name='p2_name')
        self.p1_score = tk.IntVar(name='p1_score', value=0)
        self.p2_score = tk.IntVar(name='p2_score', value=0)
        self.phase = tk.StringVar(name='phase')

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=2)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        
        
        # Top Row
        # Player 1
        tk.Label(self, text='Player 1').grid(row=0, column=0, sticky='w')
        self.lb1 = ttk.Combobox(self, values=self.choices, textvariable=self.p1_name)
        self.lb1.grid(row=1, column=0, padx=5, pady=5)
        tk.Spinbox(self, textvariable=self.p1_score, width=3, from_=-99, to=99, justify='center').grid(row=1, column=1, padx=5)
        
        # Switch Players
        tk.Button(self, text='<->', command=self.switch_players).grid(row=1, column=2, ipadx=5)
        
        # Player 2
        tk.Spinbox(self, textvariable=self.p2_score, width=3, from_=-99, to=99, justify='center').grid(row=1, column=3, padx=5)
        self.lb2 = ttk.Combobox(self, values=self.choices, textvariable=self.p2_name)
        self.lb2.grid(row=1, column=4, padx=5, pady=5)
        
        # Entry box for the current tournament phase. (Winners R1, Losers R2, Winners-Final...)
        tk.Entry(self, textvariable=self.phase).grid(row=2, column=0, padx=5, pady=5)
        
        #Bottom Row
        self.btn_update = tk.Button(self, text='Update Files', command=self.update_files)
        self.btn_update.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
        
    
    def switch_players(self):
        """Swaps the values of Name and Score variables for player1 & player2"""
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
        print('Swapped player names & scores')
        
    def update_files(self):
        """Dumps the values of the variables to indiviual .txt files."""
        files = {
            'p1name.txt': self.p1_name.get(),
            'p2name.txt': self.p2_name.get(),
            'p1score.txt': str(self.p1_score.get()),
            'p2score.txt': str(self.p2_score.get()),
            'phase.txt': self.phase.get()
        }
        
        try:
            for e in files:
                f = open(e, 'w')
                f.write(files[e])
                f.close()
        except:
            Exception ('File I/O Error: Error while attempting to write .txt files')