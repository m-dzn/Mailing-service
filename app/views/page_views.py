from django.shortcuts import render
from django.views.generic.list import ListView

from app.models import LearningMaterial


class LearningMaterialView(ListView):
    model = LearningMaterial
    paginate_by = 2
    context_object_name = 'learning_materials'
    template_name = 'home/home.html'
    ordering = ['-id']

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(is_deleted=False)


def admin(request):
    learning_materials = (
        LearningMaterial.objects.filter(is_deleted=False).all()
        .order_by('-id')
    )
    return render(request, 'admin/admin.html', {
        'learning_materials': learning_materials,
    })