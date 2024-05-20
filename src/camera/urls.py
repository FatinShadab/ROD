from django.urls import path
from .views import *

urlpatterns = [
    path('test/<str:cname>', camera_test, name="camera_test_view"),
    path('register', camera_register, name="camera_register_view"),
]