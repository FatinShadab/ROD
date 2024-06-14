from django.urls import re_path
from odcm import consumers

websocket_urlpatterns = [
    re_path(r'ws/odcm/v0/', consumers.VideoConsumer.as_asgi()),
]
