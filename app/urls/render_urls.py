from django.urls import path

from app import views

urlpatterns = [
    path('', views.LearningMaterialView.as_view(), name='home'),
    path('admin/', views.admin, name='admin'),
    path('logout/', views.logout_view, name='logout'),
]
