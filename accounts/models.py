from django.db import models
from django.core.validators import RegexValidator

class CafeModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    logo = models.ImageField(upload_to='cafes/logos', null=True, blank=True)
    cover_image = models.ImageField(upload_to='cafes/covers', null=True, blank=True)
    primary_color = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                message='Primary color must be a hex color code',
            )
        ]
    )

    def __str__(self):
        return self.name
