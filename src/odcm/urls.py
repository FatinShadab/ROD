from django.urls import path
from .views import *

urlpatterns = [
    path('', land_view, name="odcm_land_view"),
]