"""When Motorsports is ready to add a new sensor, it should be added here
after it is added to models.py."""

from django.contrib import admin  # noqa f401

from .models import (
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
    EventCodeAccess,
)

admin.site.register(TemperatureSensor)
admin.site.register(AccelerationSensor)
admin.site.register(WheelSpeedSensor)
admin.site.register(SuspensionSensor)
admin.site.register(FuelLevelSensor)
admin.site.register(EventCodeAccess)
