from django.urls import path
from .views import *

urlpatterns = [
    path('test/<str:cname>', camera_test, name="camera_test_view"),
    path('test-device-cam/<int:camid>', device_camera_test, name="device_camera_test"),
    path('register', camera_register, name="camera_register_view"),
]