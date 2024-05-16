from django.db import models
from app.models.abstract_models import BaseModel


class LearningMaterial(BaseModel):
    title = models.CharField(max_length=40, null=False)
    price = models.IntegerField(null=False)
    description = models.CharField(max_length=400, default='', null=False)

    file_path = models.CharField(max_length=2048, null=True) # 크롬에서 지원하는 URL 길이 = 2083자
    original_filename = models.CharField(max_length=255, null=True) # VARCHAR2 = 가변형 문자열 (기본 255)
    stored_filename = models.CharField(max_length=255, null=True) # VARCHAR2 = 가변형 문자열 (기본 255)
    extension = models.CharField(max_length=4, null=True)
    file_size = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'learning_material'

    def __str__(self):
        return f'{self.title} ({self.original_filename})'