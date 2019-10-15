from django.urls import path
from . import views

app_name = 'mercury'
urlpatterns = [
               path('', views.HomePageView.as_view()),
               path('about/', views.AboutPageView.as_view()),
               ]
