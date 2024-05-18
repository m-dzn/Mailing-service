from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    avatar = models.URLField(null=True, blank=True)
    file_receiving_email = models.EmailField(null=False)