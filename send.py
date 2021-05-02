import pycurl, json
from io import StringIO
import time
##################################################
# put token here
#access_token = "yvmei4GumXkttc4vHV3X"
access_token = "zdSv7iD9au2DFVeBg0bv"
#put web address here
#website = "http://192.168.1.2/"
#website = "http://10.8.0.1/"
website = "http://10.42.0.1/"
##################################################

# sets the send the website to POST to
url = website + "api/v1/" + access_token + "/telemetry"

def sendData(*arguments):
	global url

	if(len(arguments) % 2 != 0):
		print("Not an even number of arguments sent\nCheck that the dataname and the value was passed on all inputs")
		return -1

	values = {}
	i=0
	while(i<len(arguments)):
		values[arguments[i]] = arguments[i+1]

		i += 2

	data = {"ts": int(time.time() * 1000), "values": values}


# data not looking right?
# uncomment the next two lines and see what it looks like
	#print (values)
	#print (data)

	# sets up packet
	crl = pycurl.Curl()
	crl.setopt(crl.URL, url)
	crl.setopt(crl.HTTPHEADER, ['Content-Type:application/json'])

	# converts data to jason format
	data = json.dumps(data)
	crl.setopt(crl.POSTFIELDS, data)

	# to see the details of the data being sent
#	crl.setopt(pycurl.VERBOSE, 1)

	# this is what sends the data
	crl.perform()

	# checks the status code sent from the server
	status_code = crl.getinfo(crl.RESPONSE_CODE)
	if(status_code != 200):
		print ("ERROR: HTTP code {}".format(status_code))
		# might want to put an exit statement here if in a loop because none of the data will be sent

	# this else can go away if desired, it is just here to confirm that the data was sent without error
#	else:
#		print ("No error")

	# closes the connection
	crl.close()

	return 0

##################################################
	
###########
import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_bmp280
import adafruit_fxos8700


GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24
vx = 0
vy = 0
vz = 0
v = 0

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
    #sent inital data
    dist = distance()
    accel_x, accel_y, accel_z = sensor.accelerometer
    if(sendData("vx", vx, "vy", vy, "vz", vz, "v", v, "distance", dist, "temperature", bmp280.temperature, "air_pressure", bmp280.pressure, "accel_x", accel_x, "accel_y", accel_y, "accel_z", accel_z, "delta_x", accel_x, "delta_y", accel_y, "delta_z", accel_z) == -1):
        print("ERROR")
    else: 
        print("No error")
    #time.sleep(1)

    while True:
        dist = distance()
        print("\nDistance: %0.3f cm" % dist)
        print("Temperature: %0.3f C" % bmp280.temperature)
        print("Pressure: %0.3f hPa" % bmp280.pressure)
        # Read acceleration
        accel_x, accel_y, accel_z = sensor.accelerometer
        print("Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(accel_x, accel_y, accel_z))
        
        if(sendData("distance", dist, "temperature", bmp280.temperature, "air_pressure", bmp280.pressure, "accel_x", accel_x, "accel_y", accel_y, "accel_z", accel_z) == -1):
            print("ERROR")
        else:
            print("No error")
        time.sleep(1)
    
finally:
    GPIO.cleanup()
