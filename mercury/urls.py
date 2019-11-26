from django.urls import path
from .views import simulator, views, dashboard, can, timer

app_name = "mercury"
urlpatterns = [
    path("", views.EventAccess.as_view(), name="EventAccess"),
    path("index", views.HomePageView.as_view(), name="index"),
    path("simulator/", simulator.SimulatorView.as_view(), name="simulator"),
    path("dashboard/", dashboard.DashboardView.as_view(), name="dashboard"),
    path("api/can/", can.post, name="can-api"),
    path("can/", can.CANUI.as_view(), name="can-ui"),
    path("timer/", timer.TimerView.as_view(), name="timer"),
]
