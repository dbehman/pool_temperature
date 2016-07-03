import subprocess
import time
# The W1ThermSensor class constructor of this package will ensure the proper kernel mods are loaded
from w1thermsensor import W1ThermSensor
from ISStreamer.Streamer import Streamer

pi_temp_file = "/sys/class/thermal/thermal_zone0/temp"
delay = 30

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

def send_data_to_InitialState( sensor_name, data, streamer ):
   streamer.log( sensor_name, data )
   streamer.flush()


def main():
   sensor = W1ThermSensor()

   pool_streamer = Streamer( bucket_name="Pool Temperature", access_key="PFphNne4eMOAMQ6EiIW5DT0BNWEIunAT", bucket_key="RPSVL4LX8S7H")
   pi_streamer = Streamer( bucket_name="Pi Temperature", access_key="PFphNne4eMOAMQ6EiIW5DT0BNWEIunAT", bucket_key="8YXAKKXW348W")

   try:
      while True:
         pi_temp = read_pi_temp()
         send_data_to_InitialState( "Onboard Pi Temperature", pi_temp, pi_streamer )
         print( "Pi onboard temperature is %.2f" % ( pi_temp ) )

         temp_in_fahrenheit = sensor.get_temperature( W1ThermSensor.DEGREES_F )
         send_data_to_InitialState( "Pool Temperature Sensor", temp_in_fahrenheit, pool_streamer )
         print( "Sensor %s has temperature %.2f" % ( sensor.id, temp_in_fahrenheit ) )

         time.sleep( delay )

   except KeyboardInterrupt:
      pool_streamer.close()
      pi_streamer.close()


if __name__ == "__main__":
	main()

