# Program that queries two sensors on my Raspberry Pi:
# 1) the DS18B20 waterproof temperature sensor connected through the Pi's GPIO
# 2) the Pi's onboard temperature sensor since the Pi sits outside in the summer heat
# The data is then sent to the IBM IoT Foundation services where my Bluemix application consumes them
#
# Author: Dan Behman
# July 16, 2016
#
#
import subprocess
import time
import ibmiotf.device
# The W1ThermSensor class constructor of this package will ensure the proper kernel mods are loaded
from w1thermsensor import W1ThermSensor

pi_temp_file = "/sys/class/thermal/thermal_zone0/temp"
delay = 10

# Include these here to show how else DS18B20 temp can be read
# temperature_in_celsius = sensor.get_temperature()
# temperature_in_all_units = sensor.get_temperatures([
#    W1ThermSensor.DEGREES_C,
#    W1ThermSensor.DEGREES_F,
#    W1ThermSensor.KELVIN])

def read_pi_temp():
   cat_data = subprocess.Popen( ['cat', pi_temp_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
   out, err = cat_data.communicate()
   temp = float( out ) / 1000
   return temp

def main():
   sensor = W1ThermSensor()

   try:
      options = ibmiotf.device.ParseConfigFile( "/home/pi/working/WatsonIoT/device.cfg" )
      client = ibmiotf.device.Client( options )
      client.connect()

   except ibmiotf.ConnectionException  as e:
      print( "Got exception when connecting to IBM IOTF." )

   try:
      while True:
         pi_temp = read_pi_temp()
         pool_temp_in_fahrenheit = sensor.get_temperature( W1ThermSensor.DEGREES_F )

         print( "Pi onboard temperature is %.2f" % ( pi_temp ) )
         print( "Sensor %s has temperature %.2f" % ( sensor.id, pool_temp_in_fahrenheit ) )

         sensor_data = {"pi_temp" : pi_temp, "pool_temp" : pool_temp_in_fahrenheit}

         client.publishEvent( "status", "json", sensor_data )

         time.sleep( delay )

   except KeyboardInterrupt:
      client.disconnect()


if __name__ == "__main__":
	main()

