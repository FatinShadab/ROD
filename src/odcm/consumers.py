import cv2
import numpy as np
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from ultralytics import YOLO, solutions

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        self.model = YOLO("yolov8n.pt")
        self.line_points = [(20, 400), (1080, 400)]  # line or region points
        self.classes_to_count = [0, 2]  # person and car classes for count
        self.counter = solutions.ObjectCounter(
            view_img=False,
            reg_pts=self.line_points,
            classes_names=self.model.names,
            draw_tracks=True,
            line_thickness=5,
        )
        
        self.process_interval = 2
        self.frame_count = 0

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            np_data = np.frombuffer(bytes_data, np.uint8)
            frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            frame = cv2.resize(frame, (240, 180))

            results = await asyncio.to_thread(self.model.track, frame, persist=True, show=False, classes=self.classes_to_count)
            frame = self.counter.start_counting(frame, results)
            self.draw_vertical_line(frame)
            # Encode the processed frame to JPEG format
            frame = cv2.resize(frame, (640, 480))

        _, jpeg = cv2.imencode('.jpg', frame)

        await self.send(bytes_data=jpeg.tobytes())

    def draw_vertical_line(self, frame):
        cv2.line(frame, (640, 0), (640, 480), (0, 255, 0), 2)  # Draw a vertical line at x=640

