from django.db import models


# Auditing: 생성/업데이트 날짜 or 사람을 DB에 기록하는 것을 Auditing이라고 합니다.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey()
    updated_at = models.DateTimeField(auto_now=True)
    # updated_by = models.ForeignKey(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True
