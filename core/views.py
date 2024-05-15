from django.shortcuts import render, redirect
from django.contrib.auth import logout


def index(request):
    return render(request, 'home/home.html')


def logout_view(request):
    logout(request)
    return redirect('/')
