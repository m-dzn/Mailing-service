def get_ids_from_request(request):
    """
    HTTP 요청의 쿼리 스트링에서 ids 리스트를 추출합니다.
    """
    ids = request.GET.get('ids')

    if ',' in ids:
        return ids.split(',')
    else:
        return [ids]