from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home_view"),
    path('camera-register', camera_register, name="camera_register_view"),
    path('camera-test', camera_test, name="camera_test_view"),
]