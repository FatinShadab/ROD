# routing.py

from django.urls import re_path
from camera import consumers

websocket_urlpatterns = [
    re_path(r'ws/video/', consumers.VideoConsumer.as_asgi()),
]
