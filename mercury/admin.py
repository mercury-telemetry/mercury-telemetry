from django.contrib import admin  # noqa f401

# Register your models here.
from .models import SimulatedData

admin.site.register(SimulatedData)