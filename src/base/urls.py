from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home_view"),
    path('camera-setup', camera_setup, name="camera_setup_view"),
]