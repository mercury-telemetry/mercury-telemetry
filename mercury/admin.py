"""When Motorsports is ready to add a new sensor, it should be added here
after it is added to models.py."""

from django.contrib import admin  # noqa f401

from .models import EventCodeAccess


admin.site.register(EventCodeAccess)
