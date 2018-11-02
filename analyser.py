import tkinter as tk
import pickle
import base64
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from collections import OrderedDict
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

#setting display parameters
np.set_printoptions(precision = 20)
pd.set_option("display.precision", 20)


def decode(key, enc):               #Vigenere cipher decryption
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

f = open("passkeys.txt",'r')        #password retrieval
encoded_passkey = f.read()
passkey = decode('A', encoded_passkey)
f.close()

#records retrieval from file
f = open('training_data.txt','rb')
data = []
while True:
    try:
        data.append(pickle.load(f))
    except EOFError:
        print("retrieval successful!")
        break
f.close()

#creating empty dataframe
temp_list = []
df = pd.DataFrame(temp_list)

instance = 0
for record in data:
    key_names = record[0]
    up_times = np.array(record[1], dtype = np.float)
    down_times = np.array(record[2], dtype = np.float)
    hold_times =  np.array(record[3], dtype = np.float)
    temp = [0,]
    for t in range(1, len(key_names)):
        iat = down_times[t] - up_times[t-1]
        temp.append(iat)
    inter_arrival_times = np.array(temp)
    record.append([instance for _ in range(len(key_names))])
    string = str()
    up_times = up_times/min(up_times)
    down_times = down_times/min(down_times)
    for key in key_names:
        string = string + key
    if string == passkey:
        print("Record valid. Taken into consideration.")
        d = OrderedDict([('character', [_ for _ in range(1,len(key_names)+1)]), ('up_times', up_times), ('down_times', down_times), ('hold_times', hold_times), ('inter_arrival_times', inter_arrival_times), ('instance',record[-1])])
        s = pd.DataFrame.from_records(d)
        df = df.append(s)
        instance = instance+1        
    else:
        print("Record invalid. Excluded from analysis.")
        del data[data.index(record)]

df.set_index('instance', inplace = True)
df.groupby(df.index)


#data analysis using pandas
l = len(set(df.index))

def iat_plot():
    for i in range(l):
        plt.plot(df.loc[i]['character'],df.loc[i]['inter_arrival_times'])
    plt.title("Inter-Arrival Time Analysis")
    plt.show()
def hold_plot():
    for i in range(l):
        plt.plot(df.loc[i]['character'],df.loc[i]['hold_times'])
    plt.title("Hold Time Analysis")
    plt.show()


def uptime_plot():
    for i in range(l):
        plt.plot(df.loc[i]['character'],df.loc[i]['up_times'])
    plt.title("Up Time Analysis")
    plt.show()


def downtime_plot():
    for i in range(l):
        plt.plot(df.loc[i]['character'],df.loc[i]['down_times'])
    plt.title("Down Time Analysis")
    plt.show()

def df_show():
    print(df.to_string())

    
root = tk.Tk()

root.title("Model Analysis")
tk.Label(root, text = '\nChoose a plot to visualize\n').pack()
tk.Button(root, text = 'Up-Time Analysis', width = 25, command = uptime_plot).pack()
tk.Button(root, text = 'Down-Time Analysis', width = 25, command = downtime_plot).pack()
tk.Button(root, text = 'Hold-Time Analysis', width = 25, command = hold_plot).pack()
tk.Button(root, text = 'Inter-Arrival Time Analysis', width = 25, command = iat_plot).pack()
tk.Button(root, text = 'Print DataFrame', width = 25, command = df_show).pack()
tk.Label(root, text = '\n').pack()
tk.Button(root, text = 'Close', width = 25, fg = 'white', bg = 'red', command = root.destroy).pack()


root.mainloop()
