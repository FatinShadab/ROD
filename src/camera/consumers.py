# consumers.py
import cv2
import numpy as np
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #if User.objects.filter(email=self.scope["user"].email, is_active=True).exists():
        await self.accept()
        #else:
        #    self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            print("Rcv !")
            np_data = np.frombuffer(bytes_data, np.uint8)
            frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            
            # Process the frame (example: convert to grayscale)
            processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            _, jpeg = cv2.imencode('.jpg', processed_frame)
            await self.send(bytes_data=jpeg.tobytes())