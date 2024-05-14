from django.db import models
from core.models import BaseModel


class LearningMaterial(BaseModel):
    title = models.CharField(max_length=40, null=False)
    price = models.IntegerField(null=False)
    description = models.CharField(max_length=400, default='', null=True)

    file_path = models.CharField(max_length=2048, null=False)
    original_filename = models.CharField(max_length=255, null=False)
    stored_filename = models.CharField(max_length=255, null=False)
    extension = models.CharField(max_length=4, null=False)
    file_size = models.BigIntegerField(null=False)

    class Meta:
        db_table = 'learning_material'

    def __str__(self):
        return self.original_filename