from sense_hat import SenseHat
import json
from datetime import datetime
from sensehat_reader import *

sense = SenseHat()
nyu_purple = (87, 46, 140)
sense.show_message("MERCURY", text_colour=nyu_purple, scroll_speed=0.04)
sense.clear()

json_temperature  = temperature(sense)
json_pressure     = pressure(sense)
json_humidity     = humidity(sense)
json_acceleration = acceleration(sense)
json_orientation  = orientation(sense)

#print(json_temperature)
#print(json_pressure)
#print(json_humidity)
#print(json_acceleration)
#print(json_orientation)


