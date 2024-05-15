import json

from http import HTTPStatus
from django.http import JsonResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from core.utils import CustomJSONEncoder, upload_file, remove_file
from learning_material.models import LearningMaterial


LEARNING_MATERIAL_STATIC_DIRECTORY = 'learning-material'


def get_or_create_learning_materials(request):
    if request.method == 'GET':
        learning_materials = (
            LearningMaterial.objects.filter(is_deleted=False).all()
            .order_by('-id')
        )

        return JsonResponse(
            status=HTTPStatus.OK,
            data=list(learning_materials),
            encoder=CustomJSONEncoder,
            json_dumps_params={'ensure_ascii': False},
            safe=False,
        )

    elif request.method == 'POST':
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
        return JsonResponse(status=HTTPStatus.CREATED, data=dict(id=learning_material.id, title=learning_material.title))

    else:
        return JsonResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, data=dict(error='Method not allowed'))


def get_learning_material(learning_material_id):
    # 업데이트 결과 조회
    try:
        return LearningMaterial.objects.get(id=learning_material_id, is_deleted=False)
    except ObjectDoesNotExist:
        return None
    except MultipleObjectsReturned:
        return None


def update_or_delete_learning_material(request, learning_material_id):
    if request.method == 'PATCH':
        # 데이터 조회
        learning_material = get_learning_material(learning_material_id)

        if learning_material is None:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data=dict(error=f'Learning material {learning_material_id} not found'))

        body = json.loads(request.body)
        LearningMaterial.objects.filter(id=learning_material_id).update(**body)
        return JsonResponse(status=200, data=dict(result='OK'))

    elif request.method == 'DELETE':
        # 데이터 조회
        learning_material = get_learning_material(learning_material_id)

        if learning_material is None:
            return JsonResponse(status=HTTPStatus.BAD_REQUEST, data=dict(error=f'Learning material {learning_material_id} not found'))

        # 소프트 딜리트
        LearningMaterial.objects.filter(id=learning_material_id).update(is_deleted=True, deleted_at=timezone.now())

        remove_file(learning_material.stored_filename, LEARNING_MATERIAL_STATIC_DIRECTORY)
        return JsonResponse(status=HTTPStatus.OK, data=dict(result='OK'))

    else:
        return JsonResponse(status=HTTPStatus.METHOD_NOT_ALLOWED, data=dict(error='Method not allowed'))
