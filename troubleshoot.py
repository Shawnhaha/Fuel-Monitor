#This code is for troubleshooting all sensors
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
    #distance = round(distance, 2)
    
    return distance

try:
    print("Start troubleshooting...")
    dist = distance()
    #print("\nDistance: %0.3f cm" % dist)
    if dist > 0 and dist < 38:
        print("Ultrasonic sensor status: GOOD")
    else:
        print("Ultrasonic sensor status: BAD")
        
    #print("Temperature: %0.3f C" % bmp280.temperature)
    if bmp280.temperature > -40 and bmp280.temperature < 85:
        print("Temperature sensor status: GOOD")
    else:
        print("Temperature sensor status: BAD")
        
    #print("Pressure: %0.3f hPa" % bmp280.pressure)
    if bmp280.pressure > 300 and bmp280.pressure < 1100:
        print("Pressure sensor status: GOOD")
    else:
        print("Pressure sensor status: BAD")
        
    # Read acceleration
    accel_x, accel_y, accel_z = sensor.accelerometer
    #print("Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(accel_x, accel_y, accel_z))
    if accel_x > -39.2 and accel_x < 39.2 and accel_y > -39.2 and accel_y < 39.2 and accel_z > -39.2 and accel_z < 39.2:
        print("Accelerometer sensor status: GOOD")
    else:
        print("Accelerometer sensor status: BAD")
    
    print("Troubleshooting done!")
      
finally:
    GPIO.cleanup()
