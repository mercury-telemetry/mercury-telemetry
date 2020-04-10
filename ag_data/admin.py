from django.contrib import admin  # noqa f401

from .models import (
    AGVenue,
    AGEvent,
    AGSensorType,
    AGSensor,
    AGMeasurement,
)

admin.site.register(AGVenue)
admin.site.register(AGEvent)
admin.site.register(AGSensorType)
admin.site.register(AGSensor)
admin.site.register(AGMeasurement)
