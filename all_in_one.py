#Completed Client of The Fuel Monitor
#Completed GUI. Send data and retrieve data at same time.
#Troubbleshoot option is available.
#Author: Shangda Li
#Team: Denton Space Eagle
#Date: 4/28/2021
import requests #for API
from tkinter import * #for GUI
from PIL import ImageTk,Image #for adding pic to GUI
import subprocess #for running external program 
import re
from playsound import playsound #for audio warning
import atexit #for killing child process

#Buzzer
from gpiozero import Buzzer
buzzer = Buzzer(17)

#GUI design
window = Tk()
window.title("Fuel Monitor")
window.geometry('750x450')

label = Label(window, text='FUEL MONITOR', bg="green", fg="black", font=(None, 35))
label.grid(column=0,row=0)

image = Image.open("circle-cropped.png")
image = image.resize((70, 70), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)
canvas = Label(image = img)
canvas.grid(column=1,row=0)

#A function for retrieving data from Thingsboard
def get_telemetry():
    global ctr
    ctr += 1
    #Retrieve data ultilizing REST API
    #You need to get a JWT token first for authorization. See Thingsboard website for more info.
    url = 'http://10.42.0.1/api/plugins/telemetry/DEVICE/0ffbbf70-3a7a-11eb-ac02-ed7fb6ef43c9/values/timeseries?keys=temperature,air_pressure,fuel_level,v,fly_time,fly_distance,danger'
    headers = {'Accept': 'application/json', 'X-Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJzaGFuZ2RhbGlAbXkudW50LmVkdSIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwidXNlcklkIjoiMjM3MTUxNjAtMzQwMi0xMWViLTk5MGItMzllMTFmODAyZjcyIiwiZmlyc3ROYW1lIjoiU2hhbmdkYSIsImxhc3ROYW1lIjoiTGkiLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiZWI0MmNjYzAtMzQwMC0xMWViLTk5MGItMzllMTFmODAyZjcyIiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCIsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNjE5NzkyODkyLCJleHAiOjE2MTk4MDE4OTJ9.oddlwaHRFBkMGx5VTPT-yYTmH3RvslmH9rHa_n2dg52Qs_ol1BbeZls3eQsibBchYQzscszVg9X_n0WCKnNVrQ'}
    response = requests.get(url, headers=headers)
    print(response.text)

    #Regex for the telemetry names and values
    x = re.search("{\"(.*)\":\[{\"ts\":.*,\"value\":\"(.*)\"}\],"
    +"\"(.*)\":\[{\"ts\":.*,\"value\":\"(.*)\"}\],"
    +"\"(.*)\":\[{\"ts\":.*,\"value\":\"(.*)\"}\],"
    +"\"(.*)\":\[{\"ts\":.*,\"value\":\"(.*)\"}\],"
    +"\"(.*)\":\[{\"ts\":.*,\"value\":\"(.*)\"}\],"
    +"\"(.*)\":\[{\"ts\":.*,\"value\":\"(.*)\"}\],"
    +"\"(.*)\":\[{\"ts\":.*,\"value\":\"(.*)\"}\]}", response.text)
    print(x.group(1)+": "+x.group(2))
    print(x.group(3)+": "+x.group(4))
    print(x.group(5)+": "+x.group(6))
    print(x.group(7)+": "+x.group(8))
    print(x.group(9)+": "+x.group(10))
    print(x.group(11)+": "+x.group(12))
    print(x.group(13)+": "+x.group(14))
    
    if ctr == 1: #the first time need to creat a label
        global data_label
        data_label = Label(window, text="Temperature: %0.2f"%float(x.group(2))+"C\n"
        +"Pressure: %0.2f"%float(x.group(4))+"hPa\n"
        +"Fuel Level: %0.2f"%float(x.group(6))+"L\n"
        +"Speed: %0.2f"%float(x.group(8))+"m/s\n"
        +"Fly Time: %0.2f" %float(x.group(10))+"s\n"
        +"Fly Distance: %0.2f"%float(x.group(12))+"m", font=(None, 20))
        data_label.grid(column=0,row=1)
    else: #not first time need to modify the existing label
        data_label.config(text="Temperature: %0.2f"%float(x.group(2))+"C\n"
        +"Pressure: %0.2f"%float(x.group(4))+"hPa\n"
        +"Fuel Level: %0.2f"%float(x.group(6))+"L\n"
        +"Speed: %0.2f"%float(x.group(8))+"m/s\n"
        +"Fly Time: %0.2f"%float(x.group(10))+"s\n"
        +"Fly Distance: %0.2f"%float(x.group(12))+"m")

    #Audio
    '''
    if int(x.group(14))==1: #detect danger
        playsound('attention_attack.mp3')
        print("Danger!")
        if ctr == 1:
            global danger_label
            danger_label = Label(window, text='DANGER!', bg="red", fg="yellow", font=(None, 35))
            danger_label.grid(column=0,row=2)
            global labelON
            labelON = 1
        elif labelON == 0:
            danger_label = Label(window, text='DANGER!', bg="red", fg="yellow", font=(None, 35))
            danger_label.grid(column=0,row=2)
            labelON = 1
    else:
        print("OK!")
        if labelON == 1:
            danger_label.destroy()
            labelON = 0
            print("Destroied!")
    '''
    
    #Buzzer
    if int(x.group(14))==1: #detect danger
        buzzer.on()
        print("Danger!")
        if ctr == 1:
            global danger_label
            danger_label = Label(window, text='DANGER!', bg="red", fg="yellow", font=(None, 35))
            danger_label.grid(column=0,row=2)
            global labelON
            labelON = 1
        elif labelON == 0:
            danger_label = Label(window, text='DANGER!', bg="red", fg="yellow", font=(None, 35))
            danger_label.grid(column=0,row=2)
            labelON = 1        
    else:
        buzzer.off()
        print("OK!")
        if labelON == 1:
            danger_label.destroy()
            labelON = 0
            print("Destroied!")
    
    window.after(1000, get_telemetry)

def clicked():
    global child_send
    child_send.terminate()
    result = subprocess.run(['python3', 'troubleshoot.py'], stdout=subprocess.PIPE, text=True)
    tbs_label = Label(window,text=result.stdout, bg='blue', fg='white')
    tbs_label.grid(column=1, row=1)
    #label = Label(window,text="Troubleshooting Results", bg='blue', fg='white')
    #label.grid(column=0, row=3)
    #cls_btn = Button(window, text="Close Troubleshooting Results", bg='gray', fg='white', command=lambda:[cls_btn.destroy(),tbs_label.destroy()])
    cls_btn = Button(window, text="Close Troubleshooting Results", bg='gray', fg='white', command=lambda:[cls_btn.destroy(),tbs_label.destroy()])
    cls_btn.grid(column=1, row=4)
    child_send = subprocess.Popen(['python3', 'send.py'])


tbs_btn = Button(window, text="Troubleshoot", bg='gray', fg='blue', command=lambda: clicked())
tbs_btn.grid(column=0, row=4)

labelON = 0 #for recongininzing if the "danger" label on

#A counter for the infinity loop reconginizing if it's the first time
#if first time--> create labels
#if not first time--> reconfig labels
ctr = 0

#start to send data by running send.py as a child process
child_send = subprocess.Popen(['python3', 'send.py'])

get_telemetry() #call the retrieving data function

window.mainloop()

atexit.register(child_send.terminate()) #kill send.py when exit the program
