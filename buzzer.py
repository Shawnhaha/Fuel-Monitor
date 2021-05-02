#This code is for testing buzzer
from gpiozero import Buzzer
from time import sleep
buzzer = Buzzer(17)
high_temp = 0
high_ap = 0
low_fuel = 0


while True:
    if high_temp == 1 or high_ap == 1 or low_fuel == 1:
        buzzer.on()
    else:
        buzzer.off()
    sleep(1)
    
'''    while True:
        buzzer.on()
        sleep(.5)
        buzzer.off()
        sleep(.5)
'''
    