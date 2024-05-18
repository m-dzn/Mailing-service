import os
from http import HTTPStatus
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import decorators, filters, pagination, permissions, viewsets

from app.models import Order, LearningMaterial
from app.serializers import OrderSerializer
from app.thread import send_email_async, send_learning_material_email_async
from app.utils import get_file


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.OrderingFilter]

    ordering = ['-id']

    def get_queryset(self):
        is_superuser = self.request.user.is_superuser
        if is_superuser:
            return Order.objects
        else:
            return Order.objects.filter(
                user=self.request.user,
                is_deleted=False
            )

    def create(self, request, *args, **kwargs):
        # 총 가격 계산
        learning_materials = LearningMaterial.objects.filter(id__in=request.POST.getlist('learning_materials[]'))
        total_price = sum(learning_material.price for learning_material in learning_materials)

        # 새 주문 생성
        order = Order.objects.create(
            total_price=total_price,
            user=request.user,
        )

        # 주문 된 학습 자료 추가
        for learning_material in learning_materials:
            order.learning_materials.add(learning_material)

        return JsonResponse(status=HTTPStatus.CREATED, data=dict(id=order.id))


def get_order(order_id, user):
    # 업데이트 결과 조회
    try:
        return (Order.objects.prefetch_related('learning_materials')
                .get(id=order_id, user=user, is_deleted=False))
    except ObjectDoesNotExist:
        return None
    except MultipleObjectsReturned:
        return None


@decorators.api_view(['PATCH'])
def check_order_payment(request, order_id):
    if request.method == 'PATCH':
        # 데이터 조회
        order = get_order(order_id, request.user)

        if order is None:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data=dict(error=f'Order {order_id} not found'))

        Order.objects.filter(id=order_id).update(
            status=Order.ORDER_STATUS_CHOICES.get('PAID'),
            paid_at=timezone.now()
        )

        learning_materials = order.learning_materials.all()

        file_list = []
        for learning_material in learning_materials:
            file = get_file(learning_material.stored_filename, 'learning-material')
            file_list.append((learning_material.original_filename, file))

        send_learning_material_email_async(
            [request.user.file_receiving_email],
            file_list,
        )

        return JsonResponse(status=200, data=dict(result='OK'))


@decorators.api_view(['PATCH'])
def cancel_order(request, order_id):
    if request.method == 'PATCH':
        # 데이터 조회
        order = get_order(order_id, request.user)

        if order is None:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data=dict(error=f'Order {order_id} not found'))

        Order.objects.filter(id=order_id).update(
            status=Order.ORDER_STATUS_CHOICES.get('CANCELED'),
            canceled_at=timezone.now(),
        )
        return JsonResponse(status=200, data=dict(result='OK'))
