import os
from hardware.Utils.utils import get_logger, get_sensor_keys
from utils import date_str_with_current_timezone

# Conditional import for sense hat and emulator
try:
    if not os.environ["EMULATE_SENSE_HAT"]:
        from sense_hat import SenseHat
    else:
        raise ImportError("Import emulator")
except ImportError:
    from sense_emu import SenseHat

sensor_keys = get_sensor_keys()


class SensePi:
    def __init__(self, log_file_name=None, sensor_ids=None):
        nyu_purple = (87, 46, 140)
        self.sense = SenseHat()
        self.sense.show_message("MERCURY", text_colour=nyu_purple, scroll_speed=0.04)
        self.sense.clear()

        if log_file_name is None:
            self.logging = get_logger("SENSE_HAT_LOG_FILE")
        else:
            self.logging = get_logger(log_file_name, log_file_name)

        if sensor_ids is None:
            self.sensor_ids = {}
            self.sensor_ids[sensor_keys["TEMPERATURE"]] = 1
            self.sensor_ids[sensor_keys["PRESSURE"]] = 2
            self.sensor_ids[sensor_keys["HUMIDITY"]] = 3
            self.sensor_ids[sensor_keys["ACCELERATION"]] = 4
            self.sensor_ids[sensor_keys["ORIENTATION"]] = 5
        else:
            self.sensor_ids = sensor_ids

    def factory(self, type):
        data = {}
        if type in sensor_keys:
            sensor_data = {
                sensor_keys["TEMPERATURE"]: self.sense.get_temperature(),
                sensor_keys["PRESSURE"]: self.sense.get_pressure(),
                sensor_keys["HUMIDITY"]: self.sense.get_humidity(),
                sensor_keys["ACCELERATION"]: self.sense.get_accelerometer_raw(),
                sensor_keys["ORIENTATION"]: self.sense.get_orientation(),
            }

            if type == "ALL":
                # ToDo: implement all sensor data access
                data["values"] = sensor_data
            elif sensor_keys[type] in sensor_data:
                key = sensor_keys[type]
                id = self.sensor_ids[key]
                data["sensor_id"] = id
                data["values"] = {}
                data["values"][key] = sensor_data[key]

            data["date"] = date_str_with_current_timezone()
        return data

    def get_all(self):
        return self.factory("ALL")

    def get_temperature(self):
        return self.factory("TEMPERATURE")

    def get_pressure(self):
        return self.factory("PRESSURE")

    def get_humidity(self):
        return self.factory("HUMIDITY")

    def get_acceleration(self):
        return self.factory("ACCELERATION")

    def get_orientation(self):
        return self.factory("ORIENTATION")
