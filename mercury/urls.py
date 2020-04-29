from django.urls import path
from .views import (
    views,
    sensor,
    events,
    gf_config,
    measurement,
    sensor_data,
)

app_name = "mercury"
urlpatterns = [
    path("", views.EventAccess.as_view(), name="EventAccess"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("index", views.HomePageView.as_view(), name="index"),
    path("sensor/", sensor.CreateSensorView.as_view(), name="sensor"),
    path(
        "sensor/delete_sensor/<sensor_name>",
        sensor.delete_sensor,
        name="delete_sensor",
    ),
    path(
        "sensor_data_exists/<int:sensor_id>", sensor_data.get, name="sensor_data_exists"
    ),
    path("events/", events.CreateEventsView.as_view(), name="events"),
    path("events/delete/<uuid:event_uuid>", events.delete_event, name="delete_event"),
    path("events/update/<uuid:event_uuid>", events.update_event, name="update_event"),
    path(
        "events/updatevenue/<uuid:venue_uuid>", events.update_venue, name="update_venue"
    ),
    path(
        "events/activateevent/<uuid:event_uuid>",
        events.activate_event,
        name="activate_event",
    ),
    path(
        "events/deactivateevent/<uuid:event_uuid>",
        events.deactivate_event,
        name="deactivate_event",
    ),
    path("events/export/<uuid:event_uuid>/csv", events.export_event, name="export_csv"),
    path("events/export/all/csv", events.export_all_event, name="export_all_csv"),
    path(
        "events/export/<uuid:event_uuid>/json", events.export_event, name="export_json"
    ),
    path("events/export/all/json", events.export_all_event, name="export_all_json"),
    path("gfconfig/", gf_config.GFConfigView.as_view(), name="gfconfig"),
    path(
        "gfconfig/delete/<int:gf_id>", gf_config.delete_config, name="gfconfig_delete"
    ),
    path(
        "gfconfig/update/<int:gf_id>", gf_config.update_config, name="gfconfig_update"
    ),
    path(
        "gfconfig/configure/<int:gf_id>",
        gf_config.configure_dashboard,
        name="gfconfig_configure",
    ),
    path(
        "gfconfig/configure/update_dashboard/<int:gf_id>",
        gf_config.update_dashboard,
        name="gfconfig_update_dashboard",
    ),
    path(
        "gfconfig/configure/reset_dashboard/<int:gf_id>",
        gf_config.reset_dashboard,
        name="gfconfig_reset_dashboard",
    ),
    path(
        "gfconfig/configure/delete_dashboard/<int:gf_id>",
        gf_config.delete_dashboard,
        name="gfconfig_delete_dashboard",
    ),
    path(
        "gfconfig/configure/create_dashboard/<int:gf_id>",
        gf_config.create_dashboard,
        name="gfconfig_create_dashboard",
    ),
    path("measurement/", measurement.MeasurementView.as_view(), name="measurement",),
]
