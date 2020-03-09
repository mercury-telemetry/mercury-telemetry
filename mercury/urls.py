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
    path("events/", events.CreateEventsView.as_view(), name="events"),
    path("events/delete/<uuid:event_uuid>", events.delete_event),
    path("events/update/<uuid:event_uuid>", events.update_event),
    path("pitcrew/", pitcrew.PitCrewView.as_view(), name="pitcrew"),
]
