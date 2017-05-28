from django.db import models
import uuid

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, m2m_changed, pre_delete
import global_signal
from .signals import *
from django.contrib.admin.models import LogEntry
from content_uploader.models import MyUser, Uploader

from utils import (name_definition, add_current_objects_parent_to_request_session, uuid_name_definition)

default_uuid = 'fd395736-523c-43bf-9653-cfe5ddd23528'
# ---Global MSG---
# Code is primary field
# Order by created date


class CommonInfo(models.Model):
    """
    Abstract class for reduce size of lines .. ;)
    """
    title = models.TextField(blank=False, max_length=100)
    slug = models.SlugField(editable=False, max_length=150)
    description = models.TextField(max_length=1500)
    is_live = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    # Add a manager to override functionality of get_query set
    # objects = HideDeletedObjectListFilterManager()

    def str_code(self):
        return str(self.code)

    def clean(self):
        self.title = self.title.lower()

    def delete(self):
        if self.is_live:
            self.is_live = False
            self.save()
            Permission.objects.get(name=self.code).delete()

    class Meta:
        abstract = True
        ordering = ('title',)


class CourseManager(models.Manager):
    def get_distinct_stream_via_board(self, board_pk):
        return self.values_list('title', 'title').filter(grade__board__pk=board_pk).order_by('title', '-created').distinct('title')


class Course(CommonInfo):
    """
    Course class for CRUD
    """
    grade = models.ForeignKey('classes.ClassCategory', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objects = CourseManager()

    class Meta(CommonInfo.Meta):
        verbose_name_plural = "1. Stream"
        verbose_name = "Stream"
        unique_together = ['title', 'grade']
        ordering = ('grade__title', 'title',)

    def __str__(self):
        """Return slug and first 8 char"""
        return name_definition(self.title, self.grade)

    def get_uuid_name_definition(self):
        return uuid_name_definition(self.grade, str(self.code))

    def chained_relation(self):
        print('Hello gaurav ...')
        return self.item_set.filter(is_present=True)


class SubjectManager(models.Manager):
    def get_distinct_stream_via_grade(self, stream_title, grade_pk):
        return self.values_list('code', 'title').filter(course__title=stream_title, course__grade__pk=grade_pk)


class Subject(CommonInfo):
    """
    Subject class for CRUD
    """
    course = models.ForeignKey('Course', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    objects = SubjectManager()

    class Meta(CommonInfo.Meta):
        verbose_name_plural = "2. Subject"
        unique_together = ['title', 'course']
        ordering = ('-course__grade__title', 'title',)

    def __str__(self):
        """
        Return slug and first 8 char
        """
        return name_definition(self.title, self.course)

    def get_uuid_name_definition(self):
        return uuid_name_definition(self.course, str(self.code))


class Chapter(CommonInfo):
    """
    Chapter class for CRUD
    """
    subject = models.ForeignKey('Subject', default=default_uuid)
    chapter_number = models.PositiveIntegerField()
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(CommonInfo.Meta):
        verbose_name_plural = "3. Chapter"
        unique_together = ['title', 'subject']
        ordering = ('-subject__course__grade__title', 'title',)

    def __str__(self):
        """Return slug and first 8 char"""
        return name_definition(self.title, self.subject)

    def get_uuid_name_definition(self):
        return uuid_name_definition(self.subject, str(self.code))


class Topic(CommonInfo):
    """
    Topic class for CRUD
    """
    chapter = models.ForeignKey('Chapter', default=default_uuid)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(CommonInfo.Meta):
        verbose_name = "Concept"
        verbose_name_plural = "4. Concept"
        unique_together = ['title', 'chapter']
        ordering = ('-chapter__subject__course__grade__title', 'title',)

    def __str__(self):
        """
        Return slug and first 8 char
        """
        return name_definition(self.title, self.chapter)

    def get_uuid_name_definition(self):
        return uuid_name_definition(self.chapter, str(self.code))


class ModuleData(CommonInfo):
    """
    ModuleData class for CRUD
    """
    topic = models.ForeignKey('Topic', default=default_uuid, related_name='parent')
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta(CommonInfo.Meta):
        verbose_name_plural = "5. Module(s) Data"
        unique_together = ['title', 'topic']
        ordering = ('-topic__chapter__subject__course__grade__title', 'title',)

    def __str__(self):
        """
        Return slug and first 8 char
        """
        return name_definition(self.title, self.topic)

    def get_uuid_name_definition(self):
        return uuid_name_definition(self.topic, str(self.code))


for sender in [Course, Subject, Chapter, Topic, ModuleData]:
    """
    Calls pre-save function to create the slug field, add_selection_to_sessio and delete permission of object
    """
    pre_save.connect(pre_save_create_slug, sender=sender)
    pre_save.connect(add_current_objects_parent_to_request_session, sender=sender)
    # pre_save.connect(global_signal.update_permission_if_obj_update, sender=sender)
    pre_delete.connect(delete_object_permission, sender=sender)


# Connect global_signals with models here ...
pre_save.connect(global_signal.change_log_msg, sender=LogEntry)
pre_save.connect(create_topic, sender=Topic)

post_save.connect(create_course, sender=Course)
post_save.connect(create_subject, sender=Subject)
post_save.connect(create_chapter, sender=Chapter)
post_save.connect(create_topic, sender=Topic)
post_save.connect(create_module, sender=ModuleData)

pre_save.connect(global_signal.change_user_type, sender=MyUser)
pre_delete.connect(global_signal.delete_uploader, sender=Uploader)

# User permissions edit
m2m_changed.connect(global_signal.update_user, sender=User.user_permissions.through)
# m2m_changed.connect(global_signal.update_user_group, sender=User.groups.through)
post_save.connect(global_signal.send_mail_on_user_create, sender=User)
