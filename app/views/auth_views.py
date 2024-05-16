from django.shortcuts import render, redirect
from django.contrib.auth import logout

from app.models import LearningMaterial


def home(request):
    return render(request, 'home/home.html')


def admin(request):
    learning_materials = (
        LearningMaterial.objects.filter(is_deleted=False).all()
        .order_by('-id')
    )
    return render(request, 'admin/admin.html', {
        'learning_materials': learning_materials,
    })


def logout_view(request):
    logout(request)
    return redirect('/')
