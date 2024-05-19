from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home_view"),
    path('dashboard', user_dashboard, name="dashboard_view"),
    path('login', login_view, name="login_view"),
    path('sign_up', sign_up, name="sign_up_view"),
    path('logout', logout_view, name="logout_view"),
    path('pass_reset/', password_reset_request_view, name='password_reset_view'),
    path('pass_reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm_view'),
    path('pass_reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete_view'),
]