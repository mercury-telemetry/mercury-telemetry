from django.urls import path
from . import views

app_name = "simulator"
urlpatterns = [
    path("", views.home, name="home"),
]