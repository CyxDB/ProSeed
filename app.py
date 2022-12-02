import tkinter as tk
from tkinter import StringVar, ttk
from configparser import ConfigParser
import configwriter
import os
import os.path
import scorewindow
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.config = ConfigParser()
        self.config.read('./settings.ini')
        
        self.scoreframe = scorewindow.Scoreframe(self)
        
        self.scoreframe.pack(side='top', expand=True)
        
def show_prefs():
    config = ConfigParser()
    config.read('./settings.ini')
    user_prefs = config['BAN20']      # NOTE for 1st release
    api_key = tk.StringVar()
    api_key.set(user_prefs['api_key'])
    
    print('show prefs------------------------')
    for k in user_prefs:
        print(k + ':' + user_prefs[k])
    
    top = tk.Toplevel()
    tk.Label(top, text='Api Key').pack()
    tk.Entry(top, textvariable=api_key).pack()
    tk.Button(top, text='Apply').pack()
        
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
    
    #Create a settings.ini file with default blank values
    if not (os.path.exists('./settings.ini')):
       #print("writing init configs")
       configwriter.init_configs()
    
    dir_array = ['./statspage/onscreen_p1/',
                 './statspage/onscreen_p2/',
                 './statspage/slideshow_p1/',
                 './statspage/slideshow_p2/',
                 './statspage/newplayer1/',
                 './statspage/newplayer2/']
    for path in dir_array:
        os.makedirs(os.path.dirname(path), exist_ok=True)


    MainApplication(root).pack(side='top', fill="both", expand=True)
    
    root.mainloop()
    # EXTAVS COMMENTS WILL REIGN SUPREME
    # I cannot be defeated