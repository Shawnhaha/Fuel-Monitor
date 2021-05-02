#This code is for testing ultrasonic sensor
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

print ("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)

def distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    start_time = time.time()
    end_time = time.time()

    while GPIO.input(ECHO)==0:
        start_time = time.time()
    while GPIO.input(ECHO)==1:
        end_time = time.time()
        
    duration = end_time - start_time
    distance = duration * 17150
    #distance = round(distance, 2)
    
    return distance

try:
    while True:
        dist = distance()
        print("Distance:",dist,"cm")
        time.sleep(0.5)
    
finally:
    GPIO.cleanup()
