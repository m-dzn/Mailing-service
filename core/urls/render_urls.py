from django.urls import path

from core import views
from learning_material.urls import learning_material_render_urls

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logout_view, name='logout'),
] + learning_material_render_urls
