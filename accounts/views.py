from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    # FORCE LOGOUT EVERY TIME LOGIN PAGE OPENS
    logout(request)

    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('/upload/')
        return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email', '')

        if not username or not password:
            messages.error(request, 'Username and password are required')
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        # doctors are normal users (not staff)
        user.is_staff = False
        user.save()

        messages.success(request, 'Account created. Please log in.')
        return redirect('/login/')

    return render(request, 'register.html')
