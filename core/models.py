from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey()
    updated_at = models.DateTimeField(auto_now=True)
    # updated_by = models.ForeignKey(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True
