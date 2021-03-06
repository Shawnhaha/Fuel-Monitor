#This code is for testing fuel monitor locally
import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_bmp280
import adafruit_fxos8700


GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)


# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)

bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
#sensor = adafruit_fxos8700.FXOS8700(i2c)
sensor = adafruit_fxos8700.FXOS8700(i2c, accel_range=adafruit_fxos8700.ACCEL_RANGE_4G)


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
    
    return distance

try:
    while True:
        dist = distance()
        print("\nDistance: %0.3f cm" % dist)
        print("Temperature: %0.3f C" % bmp280.temperature)
        print("Pressure: %0.3f hPa" % bmp280.pressure)
        # Read acceleration
        accel_x, accel_y, accel_z = sensor.accelerometer
        print("Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(accel_x, accel_y, accel_z))
        time.sleep(1)
    
finally:
    GPIO.cleanup()