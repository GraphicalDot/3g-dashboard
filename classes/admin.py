
from django.contrib import admin
from django.contrib import messages
from django.utils.safestring import mark_safe

from .models import ClassCategory, BoardCategory
from .forms import CreateGradeFilterForm, ChangeGradeFilterForm

import uuid

# admin.site.register(ClassCategory)
admin.site.register(BoardCategory)


def custom_queryset(self, request, _class):
    """
    Custom query set for hidden on delete
    """
    qs = super(_class, self).get_queryset(request)
    if not request.user.is_superuser:
        qs = qs.filter(is_live=True)
    return qs


@admin.register(ClassCategory)
class BoardCategoryAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        """
        Separate form for add and edit functionality
        """
        if obj:
            self.form = ChangeGradeFilterForm
            form = super(BoardCategoryAdmin, self).get_form(request, obj, **kwargs)
        else:
            self.form = CreateGradeFilterForm
            form = super(BoardCategoryAdmin, self).get_form(request, obj, **kwargs)
        return form

    def get_title(self, obj):
        return str(obj)

    def get_queryset(self, request):
        return custom_queryset(self, request, BoardCategoryAdmin)

    def save_model(self, request, obj, form, change):
        """
        User can select Multiple Grade:
        Add a new in form field as select_grade then loop on it and set obj grade
            and save obj in bulk.
        """
        print(change)
        obj.board_id = form.data.getlist('select_board')[0]
        grade_pk_list = form.data.getlist('select_grade')
        grade_title_list = [ClassCategory.objects.get(pk=grade_pk).title for grade_pk in grade_pk_list]
        msg = mark_safe('The Grade "{0}" was added successfully. You may add another Grade below.')
        if obj.title:
            grade_title_list.append(obj.title)
        for grade_title in set(grade_title_list):
            obj.title = grade_title
            if not change:
                obj.code = uuid.uuid4()
            obj.save()
            messages.add_message(request, messages.INFO, msg.format(str(obj)))


