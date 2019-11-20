from django.contrib import admin  # noqa f401

# Register your models here.
from .models import (
    SimulatedData,
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
    EventCodeAccess,
)

admin.site.register(SimulatedData)

admin.site.register(TemperatureSensor)
admin.site.register(AccelerationSensor)
admin.site.register(WheelSpeedSensor)
admin.site.register(SuspensionSensor)
admin.site.register(FuelLevelSensor)
admin.site.register(EventCodeAccess)
