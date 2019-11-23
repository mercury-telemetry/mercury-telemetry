from collections import defaultdict
import logging
from .models import (
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class CANMapper:
    """This class takes the result of decoded CAN data and maps the CAN
    ID to a Model."""

    def __init__(self, can_data):
        self.can_data = can_data
        self.map = defaultdict(None)
        self._register_sensors()

    def _register_sensors(self):
        """When a new sensor needs to be add, update the
        mappings here from "can_id" to the Sensor."""
        log.debug("Registering Sensors.")
        self.map[1] = TemperatureSensor
        self.map[2] = AccelerationSensor
        self.map[3] = WheelSpeedSensor
        self.map[4] = SuspensionSensor
        self.map[5] = FuelLevelSensor

    def get_sensor_from_id(self):
        """If an unmapped CAN ID is passed, None is returned"""
        sensor = self.map[self.can_data["can_id"]]
        log.debug(
            "Mapped can_id {} to Sensor {}.".format(self.can_data["can_id"], sensor)
        )
        return sensor
