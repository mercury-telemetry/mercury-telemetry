from django.urls import path
from .views import (
    views,
    sensor,
    events,
    pitcrew,
    gf_config,
)

app_name = "mercury"
urlpatterns = [
    path("", views.EventAccess.as_view(), name="EventAccess"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("index", views.HomePageView.as_view(), name="index"),
    path("sensor/", sensor.CreateSensorView.as_view(), name="sensor"),
    path(
        "sensor/delete_sensor/<int:sensor_id>",
        sensor.delete_sensor,
        name="delete_sensor",
    ),
    path(
        "sensor/delete_type/<int:type_id>",
        sensor.delete_sensor_type,
        name="delete_sensor_type",
    ),
    path(
        "sensor/update_sensor/<int:sensor_id>",
        sensor.update_sensor,
        name="update_sensor",
    ),
    path(
        "sensor/update_type/<int:type_id>",
        sensor.update_sensor_type,
        name="update_type",
    ),
    path("events/", events.CreateEventsView.as_view(), name="events"),
    path("events/delete/<uuid:event_uuid>", events.delete_event),
    path("events/update/<uuid:event_uuid>", events.update_event),
    path("events/updatevenue/<uuid:venue_uuid>", events.update_venue),
    path("events/export/<uuid:event_uuid>/csv", events.export_event),
    path("events/export/<uuid:event_uuid>/json", events.export_event),
    path("pitcrew/", pitcrew.PitCrewView.as_view(), name="pitcrew"),
    path("gfconfig/", gf_config.GFConfigView.as_view(), name="gfconfig"),
    path(
        "gfconfig/delete/<int:gf_id>", gf_config.delete_config, name="gfconfig_delete"
    ),
    path(
        "gfconfig/update/<int:gf_id>", gf_config.update_config, name="gfconfig_update"
    ),
    path("gfconfig/update_dashboard/<int:gf_id>", gf_config.update_dashboard,
         name="gfconfig_update_dashboard")
]
