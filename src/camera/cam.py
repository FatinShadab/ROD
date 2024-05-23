import cv2


class Camera:
    def __init__(self):
        self.video = None

    def __del__(self):
        if self.video:
            if self.video.isOpened():
                print("Done")
                self.video.release()

    def get_frame(self):
        if self.video:
            success, frame = self.video.read()
            if success:
                _, jpeg = cv2.imencode('.jpg', frame)
                return jpeg.tobytes()
            else:
                return None


class IPCamera(Camera):
    def __init__(self, video_source):
        self.video = cv2.VideoCapture(video_source)
        if not self.video.isOpened():
            raise ValueError("Failed to open video source")
        
# For testing
class InDeviceCamera(Camera):
    def __init__(self, cameraID=0):
        self.video = cv2.VideoCapture(cameraID)
        if not self.video.isOpened():
            raise ValueError("Failed to open video source")