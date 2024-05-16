from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required

from .cam import IPCamera

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@login_required(login_url='login_view')
def camera_register(request):
    return render(request, "cam.html")

@login_required(login_url='login_view')
def camera_test(request):
    video_source = 'http://192.168.0.100:8080/video'
    return StreamingHttpResponse(gen(IPCamera(video_source)), content_type='multipart/x-mixed-replace; boundary=frame')