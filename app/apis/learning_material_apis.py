import urllib.parse
from http import HTTPStatus
from django.http import JsonResponse, Http404, HttpResponse
from django.db.models import Prefetch, Count, Case, When, IntegerField
from django.shortcuts import render
from django.utils import timezone
from rest_framework import decorators, filters, pagination, permissions, views, viewsets


from app.models import LearningMaterial, Order
from app.serializers import LearningMaterialSerializer
from app.thread import send_learning_material_email_async
from app.utils import upload_file, remove_file, get_file, convert_files_into_zip


LEARNING_MATERIAL_STATIC_DIRECTORY = 'learning-material'


class LearningMaterialViewSet(viewsets.ModelViewSet):
    serializer_class = LearningMaterialSerializer
    pagination_class = pagination.PageNumberPagination
    permission_classes = [permissions.AllowAny]

    filter_backends = [filters.OrderingFilter]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)

        purchased = request.GET.get('purchased', 'none').lower()

        return render(request, 'home/home.html', {
            'learning_materials': serializer.data,
            'purchased': purchased,
        })

    def get_queryset(self):
        is_superuser = self.request.user.is_superuser
        is_home = self.request.path == '/'

        # 현재 로그인 된 유저 처리
        current_user = self.request.user if not self.request.user.is_anonymous else None

        if is_superuser and not is_home:
            queryset = LearningMaterial.objects.all()
        else:
            queryset = LearningMaterial.objects.filter(is_deleted=False)

            # 유저 주문 필터링
            order_queryset = Order.objects.filter(user=current_user)
            prefetch = Prefetch('orders', queryset=order_queryset)
            queryset = queryset.prefetch_related(prefetch)

            queryset = queryset.annotate(
                num_paid_orders=Count(
                    Case(When(orders__status='PAID', order__user=current_user, then=1), output_field=IntegerField())),
                num_requested_orders=Count(
                    Case(When(orders__status='REQUESTED', order__user=current_user, then=1), output_field=IntegerField()))
            )

            # 구매 여부 필터링
            purchased = self.request.query_params.get('purchased', None)
            if purchased == 'purchased':
                queryset = queryset.filter(num_paid_orders__gt=0)
            elif purchased == 'unpurchased':
                queryset = queryset.filter(num_paid_orders=0, num_requested_orders=0)
            elif purchased == 'requested':
                queryset = queryset.filter(num_requested_orders__gt=0)

        return queryset

    def create(self, request, *args, **kwargs):
        # 필수 값(required)
        title = request.POST.get('title')
        price = request.POST.get('price')

        if not title:
            return JsonResponse(status=400, data=dict(error='title is required'))
        if not price:
            return JsonResponse(status=400, data=dict(error='price is required'))

        file = request.FILES['file']
        uploaded_file_info = upload_file(file, LEARNING_MATERIAL_STATIC_DIRECTORY)

        # 비 필수 값(optional)
        description = request.POST.get('description')

        learning_material = LearningMaterial.objects.create(
            title=title,
            description=description,
            price=price,
            file_path=uploaded_file_info.get('file_path'),
            original_filename=uploaded_file_info.get('original_filename'),
            stored_filename=uploaded_file_info.get('stored_filename'),
            extension=uploaded_file_info.get('extension'),
            file_size=uploaded_file_info.get('file_size'),
        )
        return JsonResponse(status=HTTPStatus.CREATED,
                            data=dict(id=learning_material.id, title=learning_material.title))


class LearningMaterialDetailView(views.APIView):
    def get_object(self, pk):
        try:
            return LearningMaterial.objects.get(pk=pk)
        except LearningMaterial.DoesNotExist:
            raise Http404

    def patch(self, request, learning_material_id, format=None):
        # 데이터 조회
        learning_material = self.get_object(learning_material_id)

        if learning_material is None:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST,
                                data=dict(error=f'Learning material {learning_material_id} not found'))

        if 'file' in request.FILES:
            # 이미 저장된 파일이 있으면 삭제한 뒤 업로드합니다.
            if learning_material.stored_filename:
                remove_file(learning_material.stored_filename, LEARNING_MATERIAL_STATIC_DIRECTORY)
            uploaded_file_info = upload_file(request.FILES['file'], LEARNING_MATERIAL_STATIC_DIRECTORY)
        else:
            uploaded_file_info = dict()

        LearningMaterial.objects.filter(id=learning_material_id).update(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            **uploaded_file_info
        )
        return JsonResponse(status=200, data=dict(result='OK'))

    def delete(self, request, learning_material_id, format=None):
        # 데이터 조회
        learning_material = self.get_object(learning_material_id)

        if learning_material is None:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST,
                                data=dict(error=f'Learning material {learning_material_id} not found'))

        # 소프트 딜리트
        LearningMaterial.objects.filter(id=learning_material_id).update(
            is_deleted=True,
            deleted_at=timezone.now(),
            file_path=None,
            original_filename=None,
            stored_filename=None,
            extension=None,
            file_size=None,
        )

        remove_file(learning_material.stored_filename, LEARNING_MATERIAL_STATIC_DIRECTORY)
        return JsonResponse(status=HTTPStatus.OK, data=dict(result='OK'))


# 파일 다운로드 API 관련 함수
def check_learning_material_paid(learning_material, user):
    if user.is_superuser:
        return True
    else:
        orders = learning_material.orders.filter(user=user).all()
        return any(order.status == 'PAID' for order in orders)


def get_learning_material_file(learning_material_id, user):
    learning_material = LearningMaterial.objects.get(pk=learning_material_id)

    is_paid = check_learning_material_paid(learning_material, user)

    if is_paid:
        filename = learning_material.original_filename
        file = get_file(learning_material.stored_filename, LEARNING_MATERIAL_STATIC_DIRECTORY)
        return (filename, file), is_paid
    else:
        return (), is_paid


def get_learning_material_file_list(learning_material_ids, user):
    """
    학습자료 파일 목록을 가져옵니다.
    """
    file_list = []
    for id in learning_material_ids:
        file_tuple, is_paid = get_learning_material_file(id, user)

        if is_paid is False:
            return [], JsonResponse(status=HTTPStatus.BAD_REQUEST, data=dict(error=f'Learning Material {id} is not allowed'))

        file_list.append(file_tuple)

    return file_list, None


def get_ids_from_query(request):
    """
    HTTP 요청의 쿼리 스트링에서 ids 리스트를 추출합니다.
    """
    learning_material_ids = request.GET.get('ids')

    if ',' in learning_material_ids:
        return learning_material_ids.split(',')
    else:
        return [learning_material_ids]


@decorators.api_view(['GET'])
def download_learning_materials(request):
    # 학습 자료 아이디 처리
    learning_material_ids = get_ids_from_query(request)

    # 파일 목록 가져오기
    file_list, error_response = get_learning_material_file_list(learning_material_ids, request.user)
    if error_response:
        return error_response

    # Response 구성
    if len(file_list) == 1:
        file = file_list[0]
        filename = file[0]
        response = HttpResponse(file, content_type='application/pdf;')
    else:
        zip_file = convert_files_into_zip(file_list)
        filename = f'학습자료_{timezone.now().strftime("%Y-%m-%d_%H%M%S")}.zip'
        response = HttpResponse(zip_file, content_type='application/zip')

    encoded_filename = urllib.parse.quote(filename)
    response['Content-Disposition'] = f'attachment; filename={encoded_filename}'
    response['X-Filename'] = encoded_filename

    return response


@decorators.api_view(['GET'])
def send_learning_materials_by_email(request):
    # 학습 자료 아이디 처리
    learning_material_ids = get_ids_from_query(request)

    # 파일 목록 가져오기
    file_list, error_response = get_learning_material_file_list(learning_material_ids, request.user)
    if error_response:
        return error_response

    send_learning_material_email_async(
        [request.user.file_receiving_email],
        file_list,
    )

    return JsonResponse(status=HTTPStatus.OK, data=dict(result='OK'))