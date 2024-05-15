from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.list import ListView

from app.models import LearningMaterial


def learning_materials_ajax(request):
    if request.method == 'GET':
        page = request.GET.get('page', '1')

        learning_materials_data = (
            LearningMaterial.objects.filter(is_deleted=False).all()
            .order_by('-id')
        )
        paginator = Paginator(learning_materials_data, 1) # 페이지당 10개씩 보여주기

        try:
            learning_materials = paginator.get_page(page)
        except PageNotAnInteger:
            learning_materials = paginator.page(1)
        except EmptyPage:
            learning_materials = paginator.page(paginator.num_pages)

        context = {'learning_materials': learning_materials}
        return render(request, 'pages/learning-materials-ajax.html', context)


class LearningMaterialView(ListView):
    model = LearningMaterial
    paginate_by = 2
    context_object_name = 'learning_materials'
    template_name = 'pages/pages.html'
    ordering = ['-id']

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(is_deleted=False)
