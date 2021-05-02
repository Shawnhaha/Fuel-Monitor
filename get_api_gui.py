#Client of The Fuel Monitor
#Get the data from Thingsboard by using API
#Author: Shangda Li
#Team: Denton Space Eagle
import requests
from tkinter import *
from PIL import ImageTk,Image
#import os
import subprocess
import re
from playsound import playsound

#Buzzer
from gpiozero import Buzzer
buzzer = Buzzer(17)

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


def get_telemetry():
    global ctr
    ctr += 1
    #url = 'https://demo.thingsboard.io/api/plugins/telemetry/DEVICE/4adbb550-8c05-11eb-93db-895db613ca88/values/timeseries?keys=temperature,air_pressure,fuel_level,v,fly_time,fly_distance,danger'
    #url = 'https://demo.thingsboard.io/api/plugins/telemetry/DEVICE/4adbb550-8c05-11eb-93db-895db613ca88/values/timeseries?keys=temperature,air_pressure,fuel_level'
    #headers = {'Accept': 'application/json', 'X-Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJzaGFuZ2RhbGVlQGdtYWlsLmNvbSIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwidXNlcklkIjoiM2FiZDk0NDAtOGMwNS0xMWViLTkzZGItODk1ZGI2MTNjYTg4IiwiZmlyc3ROYW1lIjoiU2hhd24iLCJsYXN0TmFtZSI6IkxpIiwiZW5hYmxlZCI6dHJ1ZSwicHJpdmFjeVBvbGljeUFjY2VwdGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiM2E0YzgyZjAtOGMwNS0xMWViLTkzZGItODk1ZGI2MTNjYTg4IiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCIsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNjE2NTI1MjE5LCJleHAiOjE2MTgzMjUyMTl9.H-PDnM7b8JTWICgGFsTy5vTI4B9rUY5QTiLCLsRk31mb2e5_3KlFLquVH0iap4AnFyimNhFC19vkJH4sPJwepQ'}
    url = 'http://10.42.0.1/api/plugins/telemetry/DEVICE/0ffbbf70-3a7a-11eb-ac02-ed7fb6ef43c9/values/timeseries?keys=temperature,air_pressure,fuel_level,v,fly_time,fly_distance,danger'
    headers = {'Accept': 'application/json', 'X-Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJzaGFuZ2RhbGlAbXkudW50LmVkdSIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwidXNlcklkIjoiMjM3MTUxNjAtMzQwMi0xMWViLTk5MGItMzllMTFmODAyZjcyIiwiZmlyc3ROYW1lIjoiU2hhbmdkYSIsImxhc3ROYW1lIjoiTGkiLCJlbmFibGVkIjp0cnVlLCJpc1B1YmxpYyI6ZmFsc2UsInRlbmFudElkIjoiZWI0MmNjYzAtMzQwMC0xMWViLTk5MGItMzllMTFmODAyZjcyIiwiY3VzdG9tZXJJZCI6IjEzODE0MDAwLTFkZDItMTFiMi04MDgwLTgwODA4MDgwODA4MCIsImlzcyI6InRoaW5nc2JvYXJkLmlvIiwiaWF0IjoxNjE5NTU3ODEwLCJleHAiOjE2MTk1NjY4MTB9.sLG1azqHk1zQXt7pbq1brEUf-s3D0YSmg-TSSk1s2Db0HU7yeAOYGC4daEGA2o5DDR682M79qiSaxFL9psZzyQ'}
    response = requests.get(url, headers=headers)
    print(response.text)

    #Regex for telemetry names and values
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
    
    if ctr == 1:
        global data_label
        data_label = Label(window, text="Temperature: "+x.group(2)+"C\n"
        +"Pressure: "+x.group(4)+"hPa\n"
        +"Fuel Level: "+x.group(6)+"L\n"
        +"Speed: "+": "+x.group(8)+"m/s\n"
        +"Fly Time: "+": "+x.group(10)+"s\n"
        +"Fly Distance: "+": "+x.group(12)+"m", font=(None, 20))
        data_label.grid(column=0,row=1)
    else:
        data_label.config(text="Temperature: "+x.group(2)+"C\n"
        +"Pressure: "+x.group(4)+"hPa\n"
        +"Fuel Level: "+x.group(6)+"L\n"
        +"Speed: "+": "+x.group(8)+"m/s\n"
        +"Fly Time: "+": "+x.group(10)+"s\n"
        +"Fly Distance: "+": "+x.group(12)+"m")

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
    result = subprocess.run(['python3', 'troubleshoot.py'], stdout=subprocess.PIPE, text=True)
    tbs_label = Label(window,text=result.stdout, bg='blue', fg='white')
    tbs_label.grid(column=1, row=1)
    #label = Label(window,text="Troubleshooting Results", bg='blue', fg='white')
    #label.grid(column=0, row=3)
    cls_btn = Button(window, text="Close Troubleshooting Results", bg='gray', fg='white', command=lambda:[cls_btn.destroy(),tbs_label.destroy()])
    cls_btn.grid(column=1, row=4)


tbs_btn = Button(window, text="Troubleshoot", bg='gray', fg='blue', command=lambda: clicked())
tbs_btn.grid(column=0, row=4)

labelON = 0
ctr = 0
get_telemetry()

window.mainloop()
