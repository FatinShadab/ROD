from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView

from django.conf import settings
from .forms import SignUpForm, UserLoginForm, PassResetForm, CustomSetPasswordForm


# Create your views here.
def home(request):
    return render(request, "home.html")

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home_view')
        messages.error(request, "<span style='font-size: 22px;'>👮</span>: Unsuccessful registration. Invalid information.")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home_view')
            else:
                messages.error(request, "<span style='font-size: 22px;'>👮</span>: Login Unsuccessful. Invalid information.")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

def password_reset_request_view(request):
    if request.method == "POST":
        password_reset_form = PassResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            user = password_reset_form.get_user() # Generate a password reset token
            token = default_token_generator.make_token(user) # Generate uid based on user id
            uid = urlsafe_base64_encode(str(user.pk).encode()) # Build the password reset link
            protocol = 'https' if request.is_secure() else 'http'
            domain = get_current_site(request).domain
            reset_link = reverse_lazy('password_reset_confirm_view', kwargs={'uidb64': uid, 'token': token,})
            reset_email_subject = 'Password Reset Request Response @R.O.D' # Send the password reset email
            reset_email_body = render_to_string('password_reset_email.html', {'reset_link': reset_link, 'protocol': protocol, 'domain': domain})
            
            try:
                send_mail(
                    reset_email_subject,
                    None,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                    html_message=reset_email_body
                )
                messages.success(request, "<span style='font-size: 22px;'>👮</span>: Please Check Your Email For Reset Link.")
            except Exception as e:
                print(e)
                messages.error(request, "<span style='font-size: 26px;'>👮</span>: Internal Server Error Please Try Again Later !")
        else:
             messages.error(request, "<span style='font-size: 26px;'>👮</span>: Didn't Find Any Active Account With This Email !")
    
    password_reset_form = PassResetForm()

    return render(request, 'forgetpass.html', {'form': password_reset_form})

@login_required(login_url='login_view')
def logout_view(request):
    logout(request)
    return redirect('login_view')

@login_required(login_url='login_view')
def user_dashboard(request):
    return render(request, "dashboard.html")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete_view')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'pass_reset_complete.html'