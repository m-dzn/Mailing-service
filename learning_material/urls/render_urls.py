from django.urls import path

from learning_material.views import LearningMaterialView

urlpatterns = [
    path('learning-materials/', LearningMaterialView.as_view(), name='learning-materials-ajax')
]
