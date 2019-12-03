import logging
from .models import (
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)


class CANMapper:
    """This class takes the result of decoded CAN data (from the
    CAN Decode class, and maps the value from the CAN ID field
    to a Model."""

    def __init__(self, can_data):
        self.can_data = can_data
        self.sensor_map = dict()
        self._register_sensors()

    def _register_sensors(self):
        """When a new sensor needs to be add, update the
        mappings here from "can_id" to the Sensor."""

        log.debug("Registering Sensors.")
        self.sensor_map[1] = TemperatureSensor
        self.sensor_map[2] = AccelerationSensor
        self.sensor_map[3] = WheelSpeedSensor
        self.sensor_map[4] = SuspensionSensor
        self.sensor_map[5] = FuelLevelSensor

    def get_sensor_from_id(self):
        """If an unmapped CAN ID is passed, None is returned, because we
        don't know what sensor to map it to."""

        can_id = self.can_data.get("can_id")
        sensor = self.sensor_map.get(can_id)
        log.debug("Mapped can_id {} to Sensor {}.".format(can_id, sensor))
        return sensor
