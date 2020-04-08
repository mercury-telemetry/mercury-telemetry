from sense_hat import SenseHat
sense = SenseHat()

nyu_purple = (87, 46, 140)

#sense.show_message("MERCURY", text_colour=nyu_purple, scroll_speed=0.04)
sense.clear()

pressure = sense.get_pressure()
temperature = sense.get_temperature()
humidity = sense.get_humidity()

print(pressure)
print(temperature)
print(humidity)

acceleration = sense.get_accelerometer_raw()
x = acceleration["x"]
y = acceleration["y"]
z = acceleration["z"]
print("x={0}, y={1}, z={2}".format(x, y, z))

#while True:
o = sense.get_orientation()
pitch = o["pitch"]
roll = o["roll"]
yaw = o["yaw"]
print("pitch {0} roll {1} yaw {2}".format(pitch,roll,yaw))

#sense.set_pixel(2, 1, nyu_purple)
#sense.set_pixel(3, 1, nyu_purple)
#sense.set_pixel(4, 1, nyu_purple)
#sense.set_pixel(5, 1, nyu_purple)
#sense.set_pixel(1, 2, nyu_purple)
#sense.set_pixel(6, 2, nyu_purple)
#sense.set_pixel(0, 3, nyu_purple)
#sense.set_pixel(3, 3, nyu_purple)
#sense.set_pixel(4, 3, nyu_purple)
#sense.set_pixel(7, 3, nyu_purple)
#sense.set_pixel(2, 4, nyu_purple)
#sense.set_pixel(5, 4, nyu_purple)
#sense.set_pixel(1, 5, nyu_purple)
#sense.set_pixel(6, 5, nyu_purple)
#sense.set_pixel(3, 6, nyu_purple)
#sense.set_pixel(4, 6, nyu_purple)



#sense.clear(nyu_purple)
