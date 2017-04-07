from django.db import models
import uuid
from utils import (name_definition, uuid_name_definition)
# from country_state.models import State


class BoardCategory(models.Model):
    """
    Manage Category Of avail.. Boards.
    """
    title = models.CharField(max_length=100, unique=True)
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.ForeignKey('country_state.State')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = "Board Categories"

    def __str__(self):
        """Return course title and first 8 char"""
        return self.title
    
    def get_uuid_name_definition(self):
        return str(self.code)
    
    def clean(self):
        self.title = self.title.lower()


class ClassCategory(models.Model):
    """
    Manage Category Of classes.
    """
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.ForeignKey(BoardCategory)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = "Grades"
        verbose_name = "Grade"
        unique_together = ('board', 'title')
        
    def __str__(self):
        """Return course title and first 8 char"""
        return name_definition(self.title, self.board)

    def get_uuid_name_definition(self):
        return uuid_name_definition(self.board, str(self.code))

    def clean(self):
        self.title = self.title.lower()

# Create your models here.
