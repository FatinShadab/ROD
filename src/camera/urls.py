from django.urls import path
from .views import *

urlpatterns = [
    path('test/<str:cname>', camera_test, name="camera_test_view"),
    path('test-device-cam/<int:camid>', device_camera_test, name="device_camera_test"),
    path('register', camera_register, name="camera_register_view"),
    path('register-asgi-adjusted', camera_register_asgi, name="camera_register_view_asgi"),
    path('get-cameras', retrieve_camera, name="retrieve_camera_view"),
]