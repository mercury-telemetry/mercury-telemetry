from django.urls import path
from .views import simulator, views, dashboard, can

app_name = "mercury"
urlpatterns = [
    path("", views.HomePageView.as_view(), name="index"),
    path("simulator/", simulator.SimulatorView.as_view(), name="simulator"),
    path("dashboard/", dashboard.DashboardView.as_view(), name="dashboard"),
    path("api/can/", can.post, name="can-api"),
]
