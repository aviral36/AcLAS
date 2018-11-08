#importing necessary libraries
import tkinter as tk                                            #for tkinter GUI
from PIL import ImageTk, Image                                  #to display AcLAS logo on window
import pickle                                                   #for writing binary data into file
import numpy as np                                              #data science
import pandas as pd                                             #data science  
import matplotlib                                               #plot
import matplotlib.pyplot as plt                                 #plot
from positioning import center                                  #to bring tkinter window into center of screen
import threading                                                #run processes in parallel
from collections import OrderedDict                             #not necessary - just keeps my dictionary in order
from keyboard_event_recorders import tracer                     #records keystroke events

#setting display parameters
np.set_printoptions(precision = 20)
pd.set_option("display.precision", 20)

#sets the training string that will be used for keystroke analysis.
train_text = 'mathematics'

#clears the txt file containing past records. 
#Called by the tkinter button "CLEAR ALL RECORDS".
def clear_records():
    open("human_typing_analysis_data.txt", 'w').close()
    print("All records have been deleted.")

#starts recording keystrokes. Runs in background while the user types on window.
def start_recording():
    print("<<<Recording>>>")
    start_recording.traces = tracer()
    start_recording.traces.append(username)
    print(start_recording.traces)                           #statement has no purpose apart from visual verification

#Gets the string input by user. Called when person presses the "Enter" key.    
def get_string(e):
    string = e.widget.get()
    if string == train_text:                                #checks whether input equals train text
        print("Your entry has been recorded!")
        f = open("human_typing_analysis_data.txt",'ab')
        pickle.dump(start_recording.traces, f)
        f.close()
    else:                                                   #discard input if input word does not match train text
        print("You made a mistake while recording :(!")
    
def input_window():
    window = tk.Tk()
    window.geometry('500x200')
    window.focus_force()
    window.wm_title("Input Window")
    tk.Label(window, text = 'Please enter the following string in the input box:', fg = 'grey').pack()
    tk.Label(window, text = train_text, height = 5).pack()
    
    e = tk.Entry(window, width = 30)
    e.pack()
    e.bind("<Return>", get_string)
    
    tk.Label(window, text = '\n').pack()
    tk.Label(window, text = 'Typing the entire string without errors will only count.', bg = 'yellow', fg = 'red').pack()
    center(window)
    window.mainloop()
    
def start_thread():
        t1 = threading.Thread(target = start_recording)
        t2 = threading.Thread(target = input_window)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        
def get_name(e):
    global username
    username = e.widget.get()
    print(username)


def sum_calculator(list1, list2):
    n1 = np.array(list1)
    n2 = np.array(list2)
    return list(n1+n2)

def avg_calculator(arr, occurences):
    narray = np.array(arr)
    return list(narray/float(occurences))

def analyse_data():
    #records retrieval from file
    f = open("human_typing_analysis_data.txt",'rb')
    data = []
    while True:
        try:
            data.append(pickle.load(f))
        except EOFError:
            print("retrieval successful!")
            break
    f.close()
#    print(data)
    #creating empty dataframe
    temp_list = []
    df = pd.DataFrame(temp_list)
    colors = {0: '#46a346', 1:'#e9c8ba', 2: '#f0dad1', 3: '#ffdb99', 4: '#d6d9ff', 5: '#ffff4c'}
    user_list = []
    user_occurences = []
    total_uptimes = []
    total_downtimes = []
    total_iat = []
    total_holdtimes = []
    for record in data:
#        instance = 0
        up_times = np.array(record[1], dtype = np.float)
        down_times = np.array(record[2], dtype = np.float)
        hold_times =  np.array(record[3], dtype = np.float)
        temp = [0,]
        for t in range(1, len(up_times)):
            iat = down_times[t] - up_times[t-1]
            temp.append(iat)
        inter_arrival_times = np.array(temp)
#        record.append([instance for _ in range(len(key_names))])
        up_times = up_times/min(up_times)
        down_times = down_times/min(down_times)

        user = str(record[-1])
        print(user)
        if user in user_list:
            user_id = user_list.index(user)
            user_occurences[user_id] = user_occurences[user_id] + 1
            total_uptimes[user_id] = sum_calculator(total_uptimes[user_id], up_times)
            total_downtimes[user_id] = sum_calculator(total_downtimes[user_id], down_times)
            total_iat[user_id] = sum_calculator(total_iat[user_id], inter_arrival_times)
            total_holdtimes[user_id] = sum_calculator(total_holdtimes[user_id], hold_times)
        else:
            user_list.append(user)
            user_id = user_list.index(user)
            user_occurences.append(1)
            total_uptimes.append(up_times)
            total_downtimes.append(down_times)
            total_iat.append(inter_arrival_times)
            total_holdtimes.append(hold_times)


#    print( user_list, user_occurences, total_uptimes, total_downtimes, total_iat, total_holdtimes)

    for i in range(len(user_list)):
        print("Running analysis for", user_list[i])
        print("Occurences are", user_occurences[i])
        avg_uptimes = avg_calculator(total_uptimes[i], user_occurences[i])
        avg_downtimes = avg_calculator(total_downtimes[i], user_occurences[i])
        avg_holdtimes = avg_calculator(total_holdtimes[i], user_occurences[i])
        avg_iat = avg_calculator(total_iat[i], user_occurences[i])

#        print("avg uptimes:", avg_uptimes)
#        print("avg downtimes:", avg_downtimes)
#        print("avg holdtimes:", avg_holdtimes)
#        print("avg iat:", avg_iat)

                                                    
        d = OrderedDict([('up_times', avg_uptimes), ('down_times', avg_downtimes), ('hold_times', avg_holdtimes), ('inter_arrival_times', avg_iat)])
        s = pd.Series(d, name = str(user_list[i]))
        print(s)                #printing statistics

        plt.plot(s['inter_arrival_times'], color = colors[i], label = user_list[i])
    plt.legend(loc='upper right')
    plt.xlabel('character_id')
    plt.ylabel('inter-arrival times')
    plt.show()
    

#tkinter window
root = tk.Tk()

logo_path = "thumbnail/AcLAS_logo.png"
line_path = "thumbnail/line_bottom.png"

logo = ImageTk.PhotoImage(Image.open(logo_path))
line = ImageTk.PhotoImage(Image.open(line_path))
logo_panel = tk.Label(root, image = logo)
logo_panel.pack(side = 'top', fill = 'both', expand = 'yes')
line_panel = tk.Label(root, image = line)
line_panel.pack(side = 'bottom', fill = 'both', expand = 'yes')

tk.Label(root, text = 'Keyboard Input Analysis', fg = 'red').pack()
tk.Label(root, text = '\n').pack()
tk.Label(root, text = 'Before you start, please input your name:\n').pack()
n = tk.Entry(root, width = 30)
n.pack()
n.bind("<Return>", get_name)
tk.Label(root, text = 'Press enter to submit your name.\n', fg = 'grey').pack()
tk.Button(root, text = 'START', fg = 'white', bg = 'green', width = 18, command = start_thread).pack()
tk.Label(root, text = '\n', height = 1).pack()
tk.Button(root, text = 'Analyse', width = 18, command = analyse_data).pack()
tk.Label(root, text = '\n').pack()
tk.Button(root, text = 'CLEAR ALL RECORDS', fg = 'red', width = 18, command = clear_records).pack()
tk.Button(root, text = 'CLOSE', fg = 'white', bg = 'red', width = 18, command = root.destroy).pack()
center(root)
root.mainloop()
