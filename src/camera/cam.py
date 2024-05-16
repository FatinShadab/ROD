import cv2

class IPCamera:
    def __init__(self, video_source):
        self.video = cv2.VideoCapture(video_source)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            return None
        
        _, jpeg = cv2.imencode('.jpg', frame)
        
        return jpeg.tobytes()