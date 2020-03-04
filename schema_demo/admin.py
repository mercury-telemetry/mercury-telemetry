from django.contrib import admin

# Register your models here.
from .models import (
    Events,
    Sensor,
    Field,
    General_data,
)

admin.site.register(Events)
admin.site.register(Sensor)
admin.site.register(Field)
admin.site.register(General_data)