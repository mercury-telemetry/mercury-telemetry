from django.urls import path
from .views import simulator, views, dashboard, can, stopwatch

app_name = "mercury"
urlpatterns = [
    path("", views.EventAccess.as_view(), name="EventAccess"),
    path("index", views.HomePageView.as_view(), name="index"),
    path("simulator/", simulator.SimulatorView.as_view(), name="simulator"),
    path("dashboard/", dashboard.DashboardView.as_view(), name="dashboard"),
    path("api/can/", can.post, name="can-api"),
    path("can/", can.CANUI.as_view(), name="can-ui"),
    path("stopwatch/", stopwatch.StopwatchView.as_view(), name="stopwatch"),
]
