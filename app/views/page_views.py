from django.shortcuts import render, redirect

from app.models import LearningMaterial


def admin(request):
    if not request.user.is_superuser:
        return redirect('/')

    learning_materials = (
        LearningMaterial.objects.filter(is_deleted=False).all()
        .order_by('-id')
    )
    return render(request, 'admin/admin.html', {
        'learning_materials': learning_materials,
    })