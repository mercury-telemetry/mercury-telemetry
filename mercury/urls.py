from django.urls import path
from .views import (
    simulator,
    views,
    dashboard,
    can,
    stopwatch,
    event,
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
    path("simulator/", simulator.SimulatorView.as_view(), name="simulator"),
    path("dashboard/", dashboard.DashboardView.as_view(), name="dashboard"),
    path("stopwatch/", stopwatch.StopwatchView.as_view(), name="stopwatch"),
    path("api/can/", can.post, name="can-api"),  # CAN API Ingestion endpoint
    path("can/", can.CANUI.as_view(), name="can-ui"),  # CAN Decoder UI endpoint
    path("event/", event.CreateEventView.as_view(), name="event"),
    path("sensor/", sensor.CreateSensorView.as_view(), name="sensor"),
    path("sensor/delete_sensor/<int:sensor_id>", sensor.delete_sensor),
    path("sensor/delete_type/<int:type_id>", sensor.delete_sensor_type),
    path("sensor/update_sensor/<int:sensor_id>", sensor.update_sensor),
    path("sensor/update_type/<int:type_id>", sensor.update_sensor_type),
    path("events/", events.CreateEventsView.as_view(), name="events"),
    path("events/delete/<uuid:event_uuid>", events.delete_event),
    path("events/update/<uuid:event_uuid>", events.update_event),
    path("events/updatevenue/<uuid:venue_uuid>", events.update_venue),
    path("events/export/<uuid:event_uuid>", events.export_event_two),
    path("pitcrew/", pitcrew.PitCrewView.as_view(), name="pitcrew"),
    path("gfconfig/", gf_config.GFConfigView.as_view(), name="gfconfig"),
    path("gfconfig/delete/<int:gf_id>", gf_config.delete_config),
    path("gfconfig/update/<int:gf_id>", gf_config.update_config),
]
