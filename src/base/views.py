from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, UserLoginForm

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
        messages.error(request, "Unsuccessful registration. Invalid information.")
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
                messages.error(request, "Login Unsuccessful. Invalid information.")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

@login_required(login_url='login_view')
def logout_view(request):
    logout(request)
    return redirect('login_view')

@login_required(login_url='login_view')
def user_dashboard(request):
    return render(request, "dashboard.html")
