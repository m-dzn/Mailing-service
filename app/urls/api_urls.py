from django.urls import path, include

from app import apis
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('orders', apis.OrderViewSet, basename='orders')

urlpatterns = [
    # http://localhost:8000/api/learning-materials
    path('learning-materials/', apis.get_or_create_learning_materials),
    # http://localhost:8000/api/learning-materials/1
    path('learning-materials/<int:learning_material_id>', apis.update_or_delete_learning_material),
    path('orders/<int:order_id>/check-payment', apis.check_order_payment),
    path('orders/<int:order_id>/cancel', apis.cancel_order),
    path('', include(router.urls)),
]
