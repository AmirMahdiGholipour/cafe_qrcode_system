from django.db import models
from rest_framework.validators import rege

class CafeModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    logo = models.ImageField(upload_to='cafe_logo', null=True, blank=True)
