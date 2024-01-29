from django.urls import path
from profile_analyzer import views

urlpatterns = [
    path("", views.home, name="home"),
]