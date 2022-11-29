import tkinter as tk
from tkinter import StringVar, ttk
from configparser import ConfigParser
import configwriter
import os.path
import scorewindow
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.config = ConfigParser()
        
        self.scoreframe = scorewindow.Main(self)
        
        self.scoreframe.pack(side="right", fill="both", expand=True)
        
def show_prefs():
    config = ConfigParser()
    config.read('./settings.ini')
    user_prefs = config['User']
    api_key = tk.StringVar()
    api_key.set(user_prefs['api_key'])
    
    print('show prefs------------------------')
    for k in user_prefs:
        print(k + ':' + user_prefs[k])
    
    top = tk.Toplevel()
    tk.Label(top, text='Api Key').pack()
    tk.Entry(top, textvariable=api_key).pack()
    tk.Button(top, text='Apply', command=write_prefs(user_prefs)).pack()
    
def write_prefs(user_prefs):
    print('write prefs------------------------')
    for k in user_prefs:
        print(k + ':' + user_prefs[k])
        
class Menubar(tk.Menu):
    def __init__(self, parent,*args, **kwargs):
        tk.Menu.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.filemenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='Quit', command=self.parent.quit)
        #self.filemenu.add_separator()
        
        self.editmenu = tk.Menu(self, tearoff=0)
        self.add_cascade(label='Edit', menu=self.editmenu)
        self.editmenu.add_command(label='Preferences', command=show_prefs)
        

if __name__ == "__main__":
    root = tk.Tk()
    menubar = Menubar(root)
    
    root.title('ProSeed')
    root.config(menu=menubar)
    root.geometry('500x250')
    
    #Create a settings.ini file with default blank values
    if not (os.path.exists('./settings.ini')):
       #print("writing init configs")
       configwriter.init_configs()

    MainApplication(root).pack(side="top", fill="both", expand=True)
    
    root.mainloop()