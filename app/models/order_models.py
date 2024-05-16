from django.db import models

from .abstract_models import BaseModel


class Order(BaseModel):
    total_price = models.IntegerField(null=False)
