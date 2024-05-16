from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home_view"),
    path('login', login_view, name="login_view"),
    path('sign_up', sign_up, name="sign_up_view"),
    path('dashboard', user_dashboard, name="dashboard_view"),
    path('logout', logout_view, name="logout_view")
]