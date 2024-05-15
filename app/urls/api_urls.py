from django.urls import path

from app.apis import get_or_create_learning_materials, update_or_delete_learning_material

urlpatterns = [
    path('learning-materials', get_or_create_learning_materials),
    path('learning-materials/<int:learning_material_id>', update_or_delete_learning_material),
]
