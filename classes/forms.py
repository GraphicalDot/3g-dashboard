from django import forms

# from django.shortcuts import get_object_or_404
from country_state.models import (Country)
from .models import (ClassCategory, BoardCategory)
from course_management.models import (Course, Subject, Chapter, Topic)
# from utils import (refile_form_from_hidden_fields, set_drop_downs_in_form)

from constants.global_constant import MULTI_SELECT_GRADE_HELP

GLOBAL_FORM_HIDE_LIST = ('is_live',)


def get_grade_with_unique_title():
    """
    To get distinct grade title to show on form.
    :return:
    """
    # cc_list = ClassCategory.objects.values_list('title', flat=True).distinct()
    # return [(cc, cc) for cc in cc_list]
    return []


class BasicFilterField(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="--- Select One ---")
    select_state = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]))
    select_board = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]))

    def select_grade_clean(self, select_grade_list):
        while '' in select_grade_list:
            select_grade_list.remove('')
        return select_grade_list

    def _check_stream_grade_uniqueness(self, select_grade_list):
        error_on_grade = []
        select_grade_list = self.select_grade_clean(select_grade_list)
        for grade_pk in select_grade_list:
            try:
                title = self.data.get('title')
                Course.objects.get(title=title.lower(), grade__code=grade_pk)
            except Course.DoesNotExist as e:
                pass
            else:
                error_on_grade.append(ClassCategory.objects.get(pk=grade_pk).title)

        return error_on_grade

    def _check_grade_course_subject_title_uniqueness(self):
        selected_grades = self.data.getlist('select_grade')
        selected_grades = self.select_grade_clean(selected_grades)
        stream_title = self.data.get('select_stream')
        subject_title = self.data.get('title')
        error_on_grade = []
        for grade_pk in selected_grades:
            try:
                Subject.objects.get(title=subject_title.lower(), course__title=stream_title.lower(),
                                    course__grade__pk=grade_pk)
            except Subject.DoesNotExist as e:
                print(e.args)
            else:
                grade_title = ClassCategory.objects.values_list('title', flat=True).get(pk=grade_pk)
                error_on_grade.append(grade_title)
        if error_on_grade:
            raise forms.ValidationError('This title already exist with stream(s)- "{0}" '
                                        'and grade(s)- "{1}"'.format(stream_title, ','.join(error_on_grade)))

    def _check_grade_course_subject_chapter_title_uniqueness(self):
        """Chapter name will not be repeated in the same grade in same subject."""
        selected_grade_pk = self.data.get('select_grade')
        subject_pk = self.data.get('select_subject')
        title = self.data.get('title')
        try:
            Chapter.objects.get(title=title, subject__pk=subject_pk, subject__course__grade__pk=selected_grade_pk)
        except Chapter.DoesNotExist as e:
            print(e.args)
        else:
            raise forms.ValidationError("Chapter already exist with this title, board and subject.")

    def _unique_topic_form_title(self):
        """Concept name will not be repeated in the same chapter."""
        title = self.data.get('title')
        chapter_pk = self.data.get('select_chapter')
        try:
            Topic.objects.get(title=title, chapter__pk=chapter_pk)
        except Topic.DoesNotExist as e:
            print(e.args)
        else:
            raise forms.ValidationError("Concept already exist with this title in Chapter.")

    def get_options_from_hidden_filed(self, value_str):
        """
        return options = [('key', 'val'), ... .. ]
        Get options to add on form fields when error happen.
        """
        _options = []
        data_list = value_str.strip('||').split('||') if value_str else []
        data_list = self.select_grade_clean(data_list)
        for data in data_list:
            value = data.split(':')
            _options.append((value[0], value[1]))
        return _options

    def set_drop_downs_in_form_via_hidden(self, **kwargs):
        # print(kwargs)
        _field_list = self.fields.keys()
        print(_field_list)

        if 'select_state' in _field_list:
            SELECT_STATE_OPTIONS = self.get_options_from_hidden_filed(self.data.get('hidden_select_state'))
            self.fields['select_state'].widget = \
                forms.Select(choices=[('', '--- Select One ---')] + SELECT_STATE_OPTIONS)

        if 'select_board' in _field_list:
            SELECT_BOARD_OPTIONS = self.get_options_from_hidden_filed(self.data.get('hidden_select_board'))
            self.fields['select_board'].widget = \
                forms.Select(choices=[('', '--- Select One ---')] + SELECT_BOARD_OPTIONS)

        if 'select_stream' in _field_list:
            SELECT_STREAM_OPTIONS = self.get_options_from_hidden_filed(self.data.get('hidden_select_stream'))
            print(SELECT_STREAM_OPTIONS)
            self.fields['select_stream'].widget = \
                forms.Select(choices=[('', '--- Select One ---')] + SELECT_STREAM_OPTIONS)

        if 'select_grade' in _field_list:
            SELECT_GRADE_OPTIONS = self.get_options_from_hidden_filed(self.data.get('hidden_select_grade'))
            if 'grade' in kwargs.keys():
                if kwargs['grade']['type'] == 'multi_select':
                    self.fields['select_grade'].widget = \
                        forms.CheckboxSelectMultiple(choices=SELECT_GRADE_OPTIONS)
                elif kwargs['grade']['type'] == 'radio_select':
                    self.fields['select_grade'].widget = \
                        forms.RadioSelect(choices=SELECT_GRADE_OPTIONS)

                elif kwargs['grade']['type'] == 'drop_down_select':
                    self.fields['select_grade'].widget = \
                        forms.Select(choices=[('', '--- Select One ---')] + SELECT_GRADE_OPTIONS)
            else:
                self.fields['select_grade'].widget = \
                    forms.Select(choices=[('', '--- Select One ---')] + SELECT_GRADE_OPTIONS)

        if 'select_subject' in _field_list:
            SELECT_SUBJECT_OPTIONS = self.get_options_from_hidden_filed(self.data.get('hidden_select_subject'))
            print(SELECT_SUBJECT_OPTIONS)
            self.fields['select_subject'].widget = \
                forms.Select(choices=[('', '--- Select One ---')] + SELECT_SUBJECT_OPTIONS)

        if 'select_chapter' in _field_list:
            SELECT_CHAPTER_OPTIONS = self.get_options_from_hidden_filed(self.data.get('hidden_select_chapter'))
            print(SELECT_CHAPTER_OPTIONS)
            self.fields['select_chapter'].widget = \
                forms.Select(choices=[('', '--- Select One ---')] + SELECT_CHAPTER_OPTIONS)

    def set_drop_downs_in_form_via_data_set(self, **kwargs):
        _field_list = self.fields.keys()

        if 'select_state' in _field_list:
            self.fields['select_state'].widget = \
                forms.Select(choices=[('', '--- Select One ---')] + kwargs['SELECT_STATE_OPTIONS'])

        if 'select_board' in _field_list:
            self.fields['select_board'].widget = \
                forms.Select(choices=[('', '--- Select One ---')] + kwargs['SELECT_BOARD_OPTIONS'])

        if 'select_stream' in _field_list:
            self.fields['select_stream'].widget = \
                forms.Select(choices=[('', '--- Select One ---')] + kwargs['SELECT_STREAM_OPTIONS'])

        if 'select_subject' in _field_list:
            self.fields['select_subject'].widget = \
                forms.Select(choices=[('', '--- Select One ---')] + kwargs['SELECT_SUBJECT_OPTIONS'])

        if 'select_grade' in _field_list:
            if 'grade' in kwargs.keys():
                if kwargs['grade']['type'] == 'multi_select':
                    print('under chaeck box ...')
                    self.fields['select_grade'].widget = \
                        forms.CheckboxSelectMultiple(choices=kwargs['SELECT_GRADE_OPTIONS'])
                elif kwargs['grade']['type'] == 'radio_select':
                    self.fields['select_grade'].widget = \
                        forms.RadioSelect(choices=kwargs['SELECT_GRADE_OPTIONS'])

                elif kwargs['grade']['type'] == 'drop_down_select':
                    self.fields['select_grade'].widget = \
                        forms.Select(choices=[('', '--- Select One ---')] + kwargs['SELECT_GRADE_OPTIONS'])
            else:
                self.fields['select_grade'].widget = \
                    forms.Select(choices=[('', '--- Select One ---')] + kwargs['SELECT_GRADE_OPTIONS'])

        if 'select_chapter' in _field_list:
            self.fields['select_chapter'].widget = \
                forms.Select(choices=[('', '--- Select One ---')] + kwargs['SELECT_CHAPTER_OPTIONS'])


class BasicCountryStateFilterForm(BasicFilterField):
    """
    Hidden fields use to get save state of form on clean method.
    So, we can show it as a prepopulated fields with pre. filled values
    """
    hidden_select_state = forms.CharField(widget=forms.HiddenInput())
    hidden_select_board = forms.CharField(widget=forms.HiddenInput())
    hidden_select_grade = forms.CharField(widget=forms.HiddenInput())

    title = forms.CharField(required=False, help_text="<b style='color:blue'>Create a new</b>")

    def __init__(self, *args, **kwargs):
        """
        You can set initial value.
        """
        super(BasicCountryStateFilterForm, self).__init__(*args, **kwargs)

    class Meta:
        exclude = GLOBAL_FORM_HIDE_LIST
        help_texts = {
            'title': 'Group to which this message belongs to',
        }


class ChangeBasicCountryStateFilterForm(BasicFilterField):
    """
    Hidden fields use to get save state of form on clean method.
    So, we can show it as a prepopulated fields with pre. filled values
    """
    title = forms.CharField(required=False, help_text="<b style='color:blue'>Create a new</b>")

    def __init__(self, *args, **kwargs):
        """
        You can set initial value.
        """
        super(ChangeBasicCountryStateFilterForm, self).__init__(*args, **kwargs)

    class Meta:
        exclude = GLOBAL_FORM_HIDE_LIST
        help_texts = {
            'title': 'Group to which this message belongs to',
        }


class CreateGradeFilterForm(BasicCountryStateFilterForm):
    select_grade = forms.CharField(
        required=False, widget=forms.CheckboxSelectMultiple,
        help_text=MULTI_SELECT_GRADE_HELP)
        
    class Meta:
        model = ClassCategory
        fields = ['country', 'select_state', 'select_board', 'select_grade', 'title']

    def clean(self):
        cleaned_data = super(CreateGradeFilterForm, self).clean()
        self.set_drop_downs_in_form_via_hidden(**{'grade': {'type': 'multi_select'}})
        title = self.data.get('title')
        select_grade_list = self.data.getlist('select_grade')
        if not (select_grade_list or title):
            raise forms.ValidationError("Please select {0} or Fill {1} field.".format('Grade Checkbox', 'title'))
        return cleaned_data


class ChangeGradeFilterForm(ChangeBasicCountryStateFilterForm):

    def __init__(self, *args, **kwargs):
        """
        Change Form: If dict has instance means its a change form. So, you can set initial value.
        and have fun
        """
        if 'instance' in kwargs:
            grade_obj = kwargs['instance']
            selected_board = grade_obj.board
            selected_state = selected_board.state
            initial = {'select_state': selected_state.id,
                       'title': grade_obj.title, 'country': '1',
                       'select_board': str(selected_board.code)
                       }
            kwargs['initial'] = initial

        super(ChangeGradeFilterForm, self).__init__(*args, **kwargs)
        # /// Common functions ...
        country_state = selected_board.get_country_state_list()
        board_list = list(BoardCategory.objects.filter_by_state(selected_state))
        # /// ....------
        set_data = {'SELECT_STATE_OPTIONS': country_state.get('state_list', []), 'SELECT_BOARD_OPTIONS': board_list,
                    'SELECT_GRADE_OPTIONS': [], 'grade': {'type': 'multi_select'}}
        self.set_drop_downs_in_form_via_data_set(**set_data)
        # set_drop_downs_in_form(self, **set_data)

    class Meta:
        model = ClassCategory
        fields = ['country', 'select_state', 'select_board', 'title']

    def clean(self):
        cleaned_data = super(ChangeGradeFilterForm, self).clean()
        title = self.data.get('title', None)
        board_pk = self.data.get('select_board', None)

        if title:
            if board_pk:
                try:
                    ClassCategory.objects.get(board__pk=board_pk, title=title)
                except ClassCategory.DoesNotExist:
                    pass
                else:
                    raise forms.ValidationError("Grade already exist with this title and board.")
        else:
            raise forms.ValidationError("Please select {0} or Fill {1} field.".format('Grade Checkbox', 'title'))

        return cleaned_data



