from common.models import BaseModel
from django.db import models


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to="images")
    rotate_duration = models.FloatField(default=0)
    modified = models.BooleanField(default=False)
