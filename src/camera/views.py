from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import json

from .forms import CameraRegForm
from .models import Camera
from .cam import IPCamera, InDeviceCamera


def gen(camera):
    try:
        while True:
            frame = camera.get_frame()
            if frame is None:
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        print(f"Error: {e}")
        yield b''

@login_required(login_url='login_view')
def camera_register(request):
    if request.method ==  "POST":
        reg_form = CameraRegForm(request.POST)
        if reg_form.is_valid():
            cam_data = reg_form.save(commit=False)
            cam_data.selected = False
            cam_data.user = request.user
            cam_data.save()
            messages.success(request, "Camera registered successfully.")
        
    cameras = Camera.objects.filter(user=request.user)
    reg_form = CameraRegForm()

    return render(request, "cam.html", {'form':reg_form, 'cameras': cameras})

def retrieve_camera(request):
    if request.method == 'GET':
        cameras = Camera.objects.filter(user=request.user)
        camera_data = [camera.serialize() for camera in cameras]  # Serialize all cameras
        return HttpResponse(json.dumps(camera_data), content_type='application/json')
    else:
        return HttpResponseBadRequest('GET request required for camera retrieval.')

@login_required(login_url='login_view')
def remvoe_camera_data(request, cname):
    #ToDo
    pass

@login_required(login_url='login_view')
def update_camera_data(request, cname):
    #ToDo
    pass

@login_required(login_url='login_view')
def camera_test(request, cname):
    testing_camera = get_object_or_404(Camera, cname=cname)
    video_source = f'http://{testing_camera.cip}:{testing_camera.cport}/video'

    try:
        camera = IPCamera(video_source)
        frame = gen(camera)
        return StreamingHttpResponse(frame, content_type='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        return HttpResponse(f"Failed to load video stream: {e}", status=503)

@login_required(login_url='login_view')
def device_camera_test(request, camid):
    try:
        camera = InDeviceCamera(camid)
        frame = gen(camera)
        return StreamingHttpResponse(frame, content_type='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        return HttpResponse(f"Failed to load video stream: {e}", status=503)