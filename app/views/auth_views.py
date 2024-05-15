from django.shortcuts import render, redirect
from django.contrib.auth import logout


def home(request):
    return render(request, 'pages/pages.html')


def admin(request):
    return render(request, 'admin/admin.html')


def logout_view(request):
    logout(request)
    return redirect('/')
