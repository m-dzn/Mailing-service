from django.urls import path

from app import views

urlpatterns = [
    path('', views.home, name='pages'),
    path('admin/', views.admin, name='admin'),
    path('logout/', views.logout_view, name='logout'),
    path('learning-materials/', views.LearningMaterialView.as_view(), name='learning-materials-ajax')
]
