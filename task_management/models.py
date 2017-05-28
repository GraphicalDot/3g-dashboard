from django.db import models
from django.utils import timezone

from datetime import datetime

from content_uploader.models import Uploader, MyUser
from course_management.models import ModuleData


default_uuid = 'fd395736-523c-43bf-9653-cfe5ddd23528'
status_fields = [('PENDING', 'pending'), ('COMPLETE', 'complete'), ('UNDER REVIEW', 'under review'),
                 ('WORKING', 'working')]


class Task(models.Model):
    """
    Task model for assigning taskto the content uploader.
    """
    # title, description, progress_status, assigned_by, assigned_to
    title = models.CharField(max_length=250, blank=False)
    description = models.TextField(max_length=1000, blank=False)
    status = models.CharField(choices=status_fields, max_length=20, default='PENDING', blank=False)
    assign_to = models.ForeignKey(Uploader, blank=True)
    assigned_by = models.ForeignKey(MyUser, default=11, blank=False)
    assigned_on = models.DateTimeField(default=timezone.now, blank=True)
    due_date = models.DateField(default=timezone.now, blank=True)
    module_permission = models.ForeignKey(ModuleData, blank=True, default=default_uuid)

    def __str__(self):
        return self.title
