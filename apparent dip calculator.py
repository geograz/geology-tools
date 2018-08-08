# tool for calculation of the apparent dip
# background info: https://en.wikipedia.org/wiki/Strike_and_dip
import tkinter as tk
from tkinter import ttk
from math import degrees, atan, sin, radians, tan

HEADER_FONT = ('Arial', 12, 'bold')

root = tk.Tk()
root.title('Apparent Dip Calculator')

header = tk.Label(root, text='Apparent Dip Calculator', font=HEADER_FONT)
header.grid(row=0, columnspan = 4)

DipDir_label = ttk.Label(root, text='real dip direction:')
DipDir_label.grid(row=1, column=0, sticky='E')
DipDir_entry = ttk.Entry(root)
DipDir_entry.grid(row=1, column=1, sticky='W')

Dip_label = ttk.Label(root, text='real dip:')
Dip_label.grid(row=2, column=0, sticky='E')
Dip_entry = ttk.Entry(root)
Dip_entry.grid(row=2, column=1, sticky='W')

Cs_label = ttk.Label(root, text='orientation of \ncross section:')
Cs_label.grid(row=3, column=0, sticky='E')
Cs_entry = ttk.Entry(root)
Cs_entry.grid(row=3, column=1, sticky='W')

root.cv = tk.Canvas(root, width = 200, height = 200)
root.cv.grid(row=7, column=3)

def graphics(appdip): #creates graphical representation of apparent dip angle
    root.cv.create_arc(10, 10, 190, 190, 
                       start=90, 
                       extent = -appdip, 
                       dash=(7,4), 
                       fill='white')
    root.cv.create_arc(10, 10, 190, 190, 
                       start=90, 
                       extent = 360 - appdip, 
                       dash=(7,4), 
                       fill='#f0f0f0')
    root.cv.create_oval(10, 10, 190, 190)
    root.cv.create_line(100, 0, 100, 30, 
                        width=3)

def calc_appdip(graphics):
    def redirector(inputStr):  # permits printing on GUI
        textbox.insert(tk.INSERT, inputStr)  # permits printing on GUI
    tk.sys.stdout.write = redirector  # permits printing on GUI
    
    try: # input validation
        x = float(DipDir_entry.get())
        y = float(Dip_entry.get())
        z = float(Cs_entry.get())
    except ValueError:
        print ('invalid input')       
    if x > 360 or z > 360 or y > 90:
        print('invalid input')
    
    else: # calculate apparent dip
        strike = x + 90
        appdip = degrees(atan(sin(radians(z - strike)) * tan(radians(y))))
        if appdip > 0:
            appdip = 90 - appdip
        else:
            appdip = 90 + appdip*-1
    
        print('apparent dip: ', round(appdip, 1), '°')

        graphics(appdip)

Go_button = ttk.Button(root, text='GO', command= lambda: calc_appdip(graphics))
Go_button.grid(row=5, columnspan=2)

expl_label = ttk.Label(root, text = 'resulting apparent dip is given as ° from vertical (clockwise)')
expl_label.grid(pady = 10, row=6, columnspan = 2)

textbox = tk.Text(root, height = 20, width = 40)
textbox.grid(row=7, columnspan = 2)

scrollb = tk.Scrollbar(width = 15, command = textbox.yview)
scrollb.grid(row = 7, column = 2, sticky = 'NS')

clear_button = (ttk.Button(root, text = 'Clear', command = lambda: textbox.delete(1.0, tk.END)))
clear_button.grid(columnspan = 2)

exit_button = ttk.Button(root, text='Close app', command = lambda: exit())
exit_button.grid(columnspan = 2)

root.mainloop()
