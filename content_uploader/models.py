from django.db import models
from django.conf import settings

from django.db.models.signals import pre_save
from .signal import create_user_to_uploader
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    """
    Customize user with some extra employee fields ...
    """
    owner = models.IntegerField(null=True)
    department = models.CharField(max_length=200, help_text="Required. Max 200 characters for department name.")
    employee_number = models.CharField(max_length=100, help_text="Required. Max 100 characters for employee number.")
    employee_designation = models.CharField(max_length=300, help_text="Required.  Max"
                                                                      " 300 characters for employee number.")
    type = models.CharField(choices=[('DEFAULT', 'default',), ('STUDENT', 'student',), ('TEACHER', 'teacher',),
                                     ('UPLOADER', 'uploader'), ('ADMIN', 'admin',),
                                     ('SUPER-ADMIN', 'super-admin')], max_length=20, default='DEFAULT', editable=False)
    # REQUIRED_FIELDS = ['owner']

    class Meta:
        verbose_name_plural = "1. User"


class Uploader(models.Model):
    """
    Uploader model for handle CRUD on uploading.
    """
    # TODO: Add some extra fields
    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name_plural = "2. Uploader"

    def __str__(self):
        return self.user.username

pre_save.connect(create_user_to_uploader, sender=Uploader)
# Create your models here.
