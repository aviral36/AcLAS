import tkinter as tk
import os
import threading
import keyboard
from keyboard_event_recorders import make_list
from keyboard_event_recorders import tracer
from positioning import center


def set_password():
        os.startfile('set_password.py')

def trainer_file():
        os.startfile('train_model.py')
                    
def call_set_password():
        t1 = threading.Thread(target = set_password)
        t2 = threading.Thread(target = tracer)
        t1.start()
        t2.start()
	

root = tk.Tk()
tk.Label(root, text = "\n\nWelcome to AcLAS.", fg = 'red').pack()
tk.Label(root, text = "\nPlease enter your password to continue.", fg = 'black').pack()
tk.Label(root, text = "\n\n", fg = 'black').pack()
tk.Button(root, text='Set Password', bg = 'red', fg = 'white' , width=25, command=call_set_password).pack()
tk.Label(root, text = '\n')
tk.Button(root, text = 'Train Model', width = 25, command = trainer_file).pack()
tk.Label(root, text = '\n')
tk.Button(root, text='TERMINATE ROOT', width=25, command=root.destroy).pack()
tk.Label(root, text = "\n\n", fg = 'black').pack()
tk.Label(root, text = "YOU ARE UNDER SURVEILLANCE.", fg = 'white', bg = 'red').pack()
center(root)

root.mainloop()
