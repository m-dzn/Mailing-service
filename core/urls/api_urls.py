from django.urls import path, include

from learning_material.urls import learning_material_api_urls

urlpatterns = [
    path('', include(learning_material_api_urls)),
]
