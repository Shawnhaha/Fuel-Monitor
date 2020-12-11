from tkinter import *
import os
import subprocess

window = Tk()

window.title("Fuel Monitor")

window.geometry('350x200')

lbl = Label(window, text="Click the button to start troubleshooting!")

lbl.grid(column=0, row=0)

def clicked():
    #lbl.configure(text="Button was clicked !!")
    #os.system("python3 troubleshoot.py")
    result = subprocess.run(['python3', 'troubleshoot.py'], stdout=subprocess.PIPE, text=True)
    lbl.configure(text=result.stdout)
    
btn = Button(window, text="Troubleshoot", command=clicked)

btn.grid(column=0, row=1)

window.mainloop()