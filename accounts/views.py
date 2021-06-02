from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model

from .forms import UserRegisterModelForm, UserLoginModelForm

User = get_user_model()


def home_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login_attempt')
    context = {
        'title': 'Home'
    }
    return render(request, 'accounts/home.html', context)


def register_attempt(request):
    if request.POST:
        form = UserRegisterModelForm(request.POST)
        if form.is_valid():
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.create(first_name=first_name,
                                       last_name=last_name,
                                       email=email)
            user.set_password(password)
            user.save()
            return redirect('accounts:login_attempt')
    context = {
        'title': 'Register'
    }
    return render(request, 'accounts/register.html', context)


def login_attempt(request):
    context = {}
    if request.POST:
        form = UserLoginModelForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('accounts:home')
    else:
        form = UserLoginModelForm()
    context = {
        'title': 'Login',
        'form': form
    }
    return render(request, 'accounts/login.html', context)
