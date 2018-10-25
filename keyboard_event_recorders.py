import keyboard

def make_list(event):

        #This function makes list of all keyboard entries captured.
        key_names = list()
        down_times = list()
        up_times = list()
        hold_times = list()
        
        bypass = ['shift', 'right shift', 'backspace', 'tab', 'enter', 'esc', 'ctrl', 'right ctrl', 'left', 'right', 'up', 'down', 'caps lock']

        for e in event:
                if e.name in bypass:
                        pass
                else:
                        if e.event_type == 'down':
                                key_names.append(e.name)
                                down_times.append(e.time)
                        else:
                                up_times.append(e.time)

        for reg in range(len(up_times)):
                hold_times.append(up_times[reg]-down_times[reg])
        
#        print('keys:', key_names)
#        print('down_times:',down_times)
#        print('uptimes:', up_times)
#        print("hold time:", hold_times)
#        print([len(key_names),len(up_times),len(down_times)])
        return [key_names, up_times, down_times, hold_times]


def tracer():
        event = keyboard.record(until = 'enter')
#        for e in event:
#            print("Key Name is:", e.name)
#            print("Type of press:", e.event_type)
#            print("Time of press:", e.time)
#            print(e.scan_code)
#            print("+++++")
        m = make_list(event)
#        print(m)
        return m
