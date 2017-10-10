#apparent dip calculator
import tkinter as tk
from tkinter import ttk
import math

HEADER_FONT = ('Arial', 12, 'bold')
NORMAL_FONT = ('Arial', 10)


root = tk.Tk()
root.title('Apparent Dip Calculator')

header = tk.Label(root, text='Apparent Dip Calculator', font=HEADER_FONT)
header.grid(row=0, columnspan=2)

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
root.cv.grid(row=6, column=2)

def calc_appdip():
    def redirector(inputStr):  # permits printing on GUI
        textbox.insert(tk.INSERT, inputStr)  # permits printing on GUI
    tk.sys.stdout.write = redirector  # permits printing on GUI
    
    x = float(DipDir_entry.get())
    y = float(Dip_entry.get())
    z = float(Cs_entry.get())
    
    if x >360:
        print('invalid input')
    elif y >90:
        print('invalid input')
    elif z >360:
        print('invalid input')
    else:
        if z > 180: # calculate strike
            z = z - 180 # calculate strike
        if x < 270:
            strike = x + 90
        else:
            strike = x - 270
        # calculate apparent dip
        appdip = math.degrees(math.atan(math.sin(math.radians(z - strike)) * math.tan(math.radians(y))))
        if appdip > 0:
            appdip = 90 - appdip
        else:
            appdip = 90 + appdip*-1
    
        # print(realdip)
        print('apparent dip: ', round(appdip, 1), '°')
        #graphical representation of angle
        root.cv.create_arc(10, 10, 190, 190, start=90, extent=-appdip, dash=(7,4), fill='white')
        root.cv.create_arc(10, 10, 190, 190, start=90, extent= 360 - appdip, dash=(7,4), fill='#f0f0f0')
        root.cv.create_oval(10, 10, 190, 190)
        root.cv.create_line(100, 0, 100, 30, width=3)

Go_button = ttk.Button(root, text='GO', command=calc_appdip)
Go_button.grid(row=4, columnspan=2)

expl_label = ttk.Label(root, text='resulting apparent dip is given as ° from vertical - clockwise')
expl_label.grid(pady = 10, row=5, columnspan = 2)

textbox = tk.Text(root, height = 20, width = 50)
textbox.grid(row=6, columnspan=2)

exitbutton = ttk.Button(root, text='Close', command = lambda: exit())
exitbutton.grid(columnspan = 2)

root.mainloop()












