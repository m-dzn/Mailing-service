from django.urls import path

from app.apis import get_or_create_learning_materials, update_or_delete_learning_material

urlpatterns = [
    # http://localhost:8000/api/learning-materials
    path('learning-materials', get_or_create_learning_materials),
    # http://localhost:8000/api/learning-materials/1
    path('learning-materials/<int:learning_material_id>', update_or_delete_learning_material),
]
