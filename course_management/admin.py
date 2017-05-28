from django.contrib import admin

from .models import (Course, Subject, Chapter, Topic, ModuleData)
from annoying.functions import get_object_or_None
from .forms import (StreamForm, ChangeStreamForm, AddSubjectForm, ChangeSubjectForm, TopicForm, ChangeTopicForm,
                    AddChapterForm, ChangeChapterForm)
from constants.global_constant import GLOBAL_LIST_DISPLAY
# from classes.models import BoardCategory, ClassCategory

import uuid


def custom_queryset(self, request, _class):
    """
    Cutom query set for hidden on delete
    :param self:
    :param request:
    :param _class:
    :return:
    """
    qs = super(_class, self).get_queryset(request)
    if not request.user.is_superuser:
        qs = qs.filter(is_live=True)
    return qs


def get_initial_return(request, _class, _parent_class):
    """
    :return: A dict to set initial value on form for drop-down.
    """
    parent_key = request.session.get('LS:'+_class.__name__, False)
    if parent_key:
        if _parent_class == 'course':
            _obj = get_object_or_None(_class, pk=parent_key)
            return {
                'course': _obj.course.code if _obj else '',
            }
        elif _parent_class == 'subject':
            _obj = get_object_or_None(_class, pk=parent_key)
            return {
                'subject': _obj.subject.code if _obj else '',
            }
        elif _parent_class == 'chapter':
            _obj = get_object_or_None(_class, pk=parent_key)
            return {
                'chapter': _obj.chapter.code if _obj else '',
            }
        elif _parent_class == 'topic':
            _obj = get_object_or_None(_class, pk=parent_key)
            return {
                'topic': _obj.topic.code if _obj else '',
            }
        else:
            pass


@admin.register(Course)
class StreamAdmin(admin.ModelAdmin):
    list_display = GLOBAL_LIST_DISPLAY

    def get_form(self, request, obj=None, **kwargs):

        if obj:
            self.form = ChangeStreamForm
        else:
            self.form = StreamForm

        form = super(StreamAdmin, self).get_form(request, obj, **kwargs)
        return form

    def get_title(self, obj):
        return str(obj)

    def get_queryset(self, request):
        return custom_queryset(self, request, StreamAdmin)

    def save_model(self, request, obj, form, change):
        """
        User can select Multiple Grade:
        Add a new in form field as select_grade then loop on it and set obj grade
            and save obj in bulk.
        """
        grade_pk_list = form.data.getlist('select_grade')
        for grade_pk in grade_pk_list:
            obj.grade_id = grade_pk
            obj.owner = request.user.id
            if not change:
                obj.code = uuid.uuid4()
            obj.save()
    form = StreamForm


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = GLOBAL_LIST_DISPLAY

    def get_form(self, request, obj=None, **kwargs):

        if obj:
            self.form = ChangeSubjectForm
        else:
            self.form = AddSubjectForm

        form = super(SubjectAdmin, self).get_form(request, obj, **kwargs)
        return form

    def get_title(self, obj):
        return str(obj)

    def get_queryset(self, request):
        return custom_queryset(self, request, SubjectAdmin)

    def get_changeform_initial_data(self, request):
        """
        :param request:
        :return: set initial value on parent drop-down for all modules.
        """
        return get_initial_return(request, Subject, 'course')

    def save_model(self, request, obj, form, change):
        selected_grades_pk = form.data.getlist('select_grade')
        selected_stream_title = form.data.get('select_stream')
        stream_grade_list = Course.objects.filter(grade__pk__in=selected_grades_pk, title=selected_stream_title)

        for stream in stream_grade_list:
            obj.course = stream
            print(obj.title)
            if not change:
                obj.code = uuid.uuid4()
            obj.save()


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = GLOBAL_LIST_DISPLAY

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form = ChangeChapterForm
        else:
            self.form = AddChapterForm

        form = super(ChapterAdmin, self).get_form(request, obj, **kwargs)
        return form

    def get_title(self, obj):
        return str(obj)

    def get_queryset(self, request):
        return custom_queryset(self, request, ChapterAdmin)

    def get_changeform_initial_data(self, request):
        """
        :param request:
        :return: set initial value on parent drop-down for all modules.
        """
        return get_initial_return(request, Chapter, 'subject')

    def save_model(self, request, obj, form, change):
        selected_subject_pk = form.data.get('select_subject')
        obj.subject_id = selected_subject_pk
        if not change:
            obj.code = uuid.uuid4()
        obj.save()


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = GLOBAL_LIST_DISPLAY

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            self.form = ChangeTopicForm
        else:
            self.form = TopicForm

        form = super(TopicAdmin, self).get_form(request, obj, **kwargs)
        return form

    def get_title(self, obj):
        return str(obj)

    def get_queryset(self, request):
        return custom_queryset(self, request, TopicAdmin)

    def get_changeform_initial_data(self, request):
        """
        :param request:
        :return: set initial value on parent drop-down for all modules.
        """
        return get_initial_return(request, Topic, 'chapter')

    def save_model(self, request, obj, form, change):
        """
        Add owner value on every user object.
        """
        # obj.owner = request.user.id
        selected_chapter_pk = form.data.get('select_chapter')
        obj.chapter_id = selected_chapter_pk
        if not change:
            obj.code = uuid.uuid4()
        super(TopicAdmin, self).save_model(request, obj, form, change)


@admin.register(ModuleData)
class ModuleDataAdmin(admin.ModelAdmin):
    list_display = GLOBAL_LIST_DISPLAY

    def get_title(self, obj):
        return str(obj)

    def get_queryset(self, request):
        return custom_queryset(self, request, ModuleDataAdmin)

    def get_changeform_initial_data(self, request):
        """
        :param request:
        :return: set initial value on parent drop-down for all modules.
        """
        return get_initial_return(request, ModuleData, 'topic')


# Register your models here.
