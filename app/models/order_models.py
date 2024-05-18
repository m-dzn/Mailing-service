from django.db import models

from .abstract_models import BaseModel
from .user_models import CustomUser


class Order(BaseModel):
    ORDER_STATUS_CHOICES = {
        'REQUESTED': 'REQUESTED',
        'PAID': 'PAID',
        'CANCELED': 'CANCELED',
    }

    total_price = models.IntegerField()
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS_CHOICES.get('REQUESTED'))
    paid_at = models.DateTimeField(null=True)
    canceled_at = models.DateTimeField(null=True)

    learning_materials = models.ManyToManyField('LearningMaterial')
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='orders', null=False)

    class Meta:
        db_table = 'order'
