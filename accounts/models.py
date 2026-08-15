from django.db import models
from django.core.validators import RegexValidator
from common.models import TimeStampedModel
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CafeModel(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to="cafes/logos/", null=True, blank=True)
    cover_image = models.ImageField(upload_to="cafes/covers/", null=True, blank=True)
    primary_color = models.CharField(
        max_length=7,
        default="#000000",
        validators=[
            RegexValidator(
                regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                message='Primary color must be a hex color code',
            )
        ]
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class CafeStaffModel(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "male", "مرد"
        FEMALE = "female", "زن"

    phone_number = models.CharField(
        max_length=11, blank=True, null=True,
        validators=[RegexValidator(r"^09\d{9}$", "Invalid phone number")],
    )
    national_code = models.CharField(
        max_length=10, blank=True, null=True, unique=True,
        validators=[RegexValidator(r"^\d{10}$", "National code must be 10 digit")],
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True, null=True)


class CafeMembership(TimeStampedModel):
    class StaffRole(models.TextChoices):
        MANAGER = "manager", "Manager"
        ADMIN = "admin", "Admin"
        STAFF = "staff", "Staff"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    cafe = models.ForeignKey("accounts.CafeModel", on_delete=models.CASCADE, related_name="members")
    role = models.CharField(max_length=20, choices=StaffRole.choices, default=StaffRole.STAFF)

    class Meta:
        unique_together = ("user", "cafe")