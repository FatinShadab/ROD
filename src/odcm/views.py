from django.shortcuts import render

# Create your views here.
def land_view(request):
    return render(request, 'monitor.html')