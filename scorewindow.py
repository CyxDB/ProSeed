import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import proseed_functions as psf

class Scoreframe(tk.Frame):

    choices = ['Extav', 'Cyxie'] #array of player names to select from Comboboxes. This should be blank normally.
    
    def __init__(self, parent,*args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.p1_name = tk.StringVar(name='p1_name')
        self.p2_name = tk.StringVar(name='p2_name')
        self.p1_score = tk.IntVar(name='p1_score', value=0)
        self.p2_score = tk.IntVar(name='p2_score', value=0)
        self.phase = tk.StringVar(name='phase')

        self.p1_id = 0
        self.p2_id = 0
        self.owner_id = parent.config["BAN20"]["owner_id"]
        self.event_id = parent.config["BAN20"]["event_id"]
        self.api_key = parent.config["BAN20"]["api_key"]
        self.pname_array, self.pID_array = psf.get_pIDs_and_pnames_from_eID(self.event_id, self.api_key)
        self.dF = pd.read_csv(parent.config["BAN20"]['cheat_df_filepath'])
        self.file_location = parent.config["BAN20"]["file_loc"]

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
        
        #tk.Label(self, text='Player 1').grid(row=0, column=0, sticky='w')
        self.p1_frame = tk.LabelFrame(self, text='Player 1', labelanchor='nw')
        self.p1_frame.grid(row=1, column=0, columnspan=2)
        self.lb1 = ttk.Combobox(self.p1_frame, values=self.pname_array.tolist(), textvariable=self.p1_name)
        self.p1_name.trace('w', self.set_p1_name)
        self.lb1.pack(padx=5, pady=5, side='left')
        self.p1_spinbox = tk.Spinbox(self.p1_frame, textvariable=self.p1_score, width=3, from_=-99, to=99, justify='center')
        self.p1_spinbox.pack(padx=5, side='left')
        
        
        # Switch Players
        self.swap_button = tk.Button(self, text='<->', command=self.switch_players)
        self.swap_button.grid(row=1, column=2, ipadx=5)
        
        
        # Player 2
        self.p2_frame = tk.LabelFrame(self, text='Player 2', labelanchor='ne')
        self.p2_frame.grid(row=1, column=3, columnspan=2)
        
        self.p2_spinbox = tk.Spinbox(self.p2_frame, textvariable=self.p2_score, width=3, from_=-99, to=99, justify='center')
        self.p2_spinbox.pack(padx=5, side='left')
        
        self.lb2 = ttk.Combobox(self.p2_frame, values=self.pname_array.tolist(), textvariable=self.p2_name)
        self.p2_name.trace('w', self.set_p2_name)
        self.lb2.pack(padx=5, pady=5, side='right')
        
        
        #Bottom Row
        #Entry box for the current tournament phase. (Winners R1, Losers R2, Winners-Final...)
        self.phase_frame = tk.LabelFrame(self, text='Phase/Round', labelanchor='w')
        self.phase_frame.grid(row=2, column=0, padx=5, pady=5)
        self.entry_phase = tk.Entry(self.phase_frame, textvariable=self.phase)
        self.entry_phase.pack()
        
        self.btn_update = tk.Button(self, text='Update Files', command=self.update_files)
        self.btn_update.grid(row=2, column=2, padx=5, pady=5)
        
    ############################################################
    def get_id_from_namestring(self, namestring):
        assert namestring in self.pname_array  # never pass invalid name to this
        return self.pID_array[np.nonzero(self.pname_array == namestring)][0]
    def set_p1_name(self, *args):
        name = self.p1_name.get()
        if name in self.pname_array: # check if valid before call
            self.p1_id = self.get_id_from_namestring(name)
        else:
            return None

    def set_p2_name(self, *args):
        name = self.p2_name.get()
        if name in self.pname_array: # check if valid before call
            self.p2_id = self.get_id_from_namestring(name)
        else:
            return None


    def set_dF(self, dF):
        self.dF = dF
        return None
    ###########################################################
    
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
        update_graphic_and_statpage_data(self.dF, self.p1_id, self.file_location, playernum=1)
        update_graphic_and_statpage_data(self.dF, self.p2_id, self.file_location, playernum=2)