from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def camera_register(request):
    return render(request, "cam.html")

def camera_test(request):
    return None
