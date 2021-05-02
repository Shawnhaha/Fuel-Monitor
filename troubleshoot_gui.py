#A GUI calling the troubleshoot program
from tkinter import *
import subprocess

window = Tk()

window.title("Fuel Monitor")

window.geometry('350x200')


lbl = Label(window, text="Click the button to start troubleshooting!")

lbl.grid(column=0, row=0)

lbl = Label(window, text="Click the button !")

lbl.grid(column=0, row=1)

#fuel_data = subprocess.run(['python3', 'fuel_monitor.py'], stdout=subprocess.PIPE, text=True)
#lbl.configure(text=fuel_data.stdout)

def clicked():
    ts = subprocess.run(['python3', 'troubleshoot.py'], stdout=subprocess.PIPE, text=True)
    lbl.configure(text=ts.stdout)
    
btn = Button(window, text="Troubleshoot", command=clicked)

btn.grid(column=0, row=2)

window.mainloop()