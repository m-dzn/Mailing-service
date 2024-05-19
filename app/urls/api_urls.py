from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app import apis

# 라우터
router = DefaultRouter()
router.register('learning-materials', apis.LearningMaterialViewSet, basename='learning-materials')
router.register('orders', apis.OrderViewSet, basename='orders')

urlpatterns = [
    # http://localhost:8000/api/learning-materials/1
    path('learning-materials/<int:learning_material_id>', apis.LearningMaterialDetailView.as_view()),
    path('learning-materials/download', apis.download_learning_materials),
    path('learning-materials/send-mail', apis.send_learning_materials_by_email),
    path('orders/check-payment', apis.check_order_payment),
    path('orders/cancel', apis.cancel_order),
    path('', include(router.urls)),
]
