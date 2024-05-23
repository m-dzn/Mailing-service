from django.urls import path

from app import apis, views

urlpatterns = [
    path('', apis.LearningMaterialViewSet.as_view({'get': 'list'}), name='home'),
    path('admin/', views.admin, name='admin'),
    path('logout/', views.logout_view, name='logout'),
]
