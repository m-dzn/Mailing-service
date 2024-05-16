from django.db import models
from app.models.abstract_models import BaseModel


class LearningMaterial(BaseModel):
    title = models.CharField(max_length=40, null=False)
    price = models.IntegerField(null=False)
    description = models.CharField(max_length=400, default='', null=True)

    file_path = models.CharField(max_length=2048, null=True)
    original_filename = models.CharField(max_length=255, null=True)
    stored_filename = models.CharField(max_length=255, null=True)
    extension = models.CharField(max_length=4, null=True)
    file_size = models.BigIntegerField(null=True)

    class Meta:
        db_table = 'learning_material'

    def __str__(self):
        return self.original_filename