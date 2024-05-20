import cv2

class IPCamera:
    def __init__(self, video_source):
        self.video = cv2.VideoCapture(video_source)
        #self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            raise ValueError("Failed to open video source")

    def __del__(self):
        if self.video.isOpened():
            print("Done")
            self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if success:
            _, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        else:
            return None