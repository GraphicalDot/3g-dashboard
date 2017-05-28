from rest_framework import serializers
from .models import *


class CourseSerializer(serializers.ModelSerializer):
    """
    Course object serializer.
    """
    class Meta:
        model = Course
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    """
    Subject object serializer.
    """
    class Meta:
        model = Subject
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):
    """
    Chapter object serializer.
    """
    class Meta:
        model = Chapter
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    """
    Topic object serializer.
    """
    class Meta:
        model = Topic
        fields = '__all__'


class ModuleDataSerializer(serializers.ModelSerializer):
    """
    Module-Data object serializer.
    """
    class Meta:
        model = ModuleData
        fields = '__all__'
