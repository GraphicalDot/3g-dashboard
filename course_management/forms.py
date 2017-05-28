from .models import (Chapter, Topic, Course, Subject)
from django import forms
from classes.models import (ClassCategory, BoardCategory)
from classes.forms import (BasicCountryStateFilterForm, ChangeBasicCountryStateFilterForm)

from constants.global_constant import (MULTI_SELECT_GRADE_HELP, PRE_SELECT_GRADE_MSG)

# from utils import (refile_form_from_hidden_fields, set_drop_downs_in_form)

GLOBAL_FORM_HIDE_LIST = ('is_live',)


# class BasicCountryStateFilterForm(forms.ModelForm):
#     country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False, empty_label="--- Select One ---")
#     state = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
#
#     board = forms.CharField(required=False, widget=forms.Select(choices=[('', '--- Select One ---')]))
#
#     class Meta:
#         exclude = GLOBAL_FORM_HIDE_LIST


class BasicFilterWithGrade(BasicCountryStateFilterForm):
    select_grade = forms.CharField(widget=forms.CheckboxSelectMultiple,
                                   help_text='Please select above fields')


class BasicChangeFormWithGrade(ChangeBasicCountryStateFilterForm):
    select_grade = forms.CharField(widget=forms.CheckboxSelectMultiple,
                                   help_text='Please select above fields')


class StreamForm(BasicCountryStateFilterForm):
    title = forms.CharField(required=True)
    select_grade = forms.CharField(widget=forms.CheckboxSelectMultiple, help_text=MULTI_SELECT_GRADE_HELP)

    class Meta:
        model = Course
        fields = ['country', 'select_state', 'select_board', 'select_grade', 'title', 'description']

    def clean_select_grade(self):
        select_grade_list = self.data.getlist('select_grade')
        select_grade_list = self.select_grade_clean(select_grade_list)
        error_on_grade = self._check_stream_grade_uniqueness(select_grade_list)

        if error_on_grade:
            raise forms.ValidationError("Stream already exists for {0}".format(', '.join(error_on_grade)))
        return select_grade_list

    def clean(self):
        cleaned_data = super(StreamForm, self).clean()
        # refile_form_from_hidden_fields(self, grade_type={'type': 'multi_select'})
        self.set_drop_downs_in_form_via_hidden(**{'grade': {'type': 'multi_select'}})
        title = self.data.get('title')
        select_grade_list = self.select_grade_clean(self.data.getlist('select_grade'))
        if not (select_grade_list or title):
            raise forms.ValidationError("Please select {0} or Fill {1} field.".format('Grade Checkbox', 'title'))
        return cleaned_data


class ChangeStreamForm(ChangeBasicCountryStateFilterForm):
    title = forms.CharField(required=True)
    # select_grade = forms.CharField(widget=forms.CheckboxSelectMultiple, help_text=MULTI_SELECT_GRADE_HELP)
    select_grade = forms.CharField(widget=forms.RadioSelect(), help_text='')

    def __init__(self, *args, **kwargs):
        """
        Change Form: If dict has instance means its a change form.So, you can set initial value.
        and have fun
        """
        if 'instance' in kwargs:
            stream_obj = kwargs['instance']
            selected_grade = stream_obj.grade
            selected_board = selected_grade.board
            selected_state = selected_board.state
            selected_country = selected_state.country

            initial = {'select_state': selected_state.id,
                       'title': stream_obj.title, 'country': selected_country.id,
                       'select_board': str(selected_board.code),
                       'select_grade': str(selected_grade.code),
                       }

            kwargs['initial'] = initial
        super(ChangeStreamForm, self).__init__(*args, **kwargs)
        # /// Common Functions
        country_state = selected_board.get_country_state_list()
        board_list = list(BoardCategory.objects.filter_by_state(selected_state))
        # //// .......
        avail_grades_in_selected_board = ClassCategory.objects.filter_by_board(selected_board)
        print(avail_grades_in_selected_board)

        _set_data = {'SELECT_STATE_OPTIONS': country_state.get('state_list', []), 'SELECT_BOARD_OPTIONS': board_list,
                     'SELECT_GRADE_OPTIONS': list(avail_grades_in_selected_board),
                     'grade': {'type': 'radio_select'}
                     }

        self.fields['select_grade'].help_text = PRE_SELECT_GRADE_MSG.format(selected_grade)
        self.set_drop_downs_in_form_via_data_set(**_set_data)
        # set_drop_downs_in_form(self, **_set_data)

    class Meta:
        model = Course
        fields = ['country', 'select_state', 'select_board', 'select_grade', 'title', 'description']

    def clean_select_grade(self):
        select_grade_list = self.data.getlist('select_grade')
        select_grade_list = self.select_grade_clean(select_grade_list)
        error_on_grade = []
        for grade_pk in select_grade_list:
            if Course.objects.filter(title=self.data.get('title'), grade__code=grade_pk).exists():
                error_on_grade.append(ClassCategory.objects.get(pk=grade_pk).title)

        if error_on_grade:
            raise forms.ValidationError("Stream already exists for {0}".format(', '.join(error_on_grade)))
        return select_grade_list

    def clean(self):
        cleaned_data = super(ChangeStreamForm, self).clean()
        title = self.data.get('title')
        select_grade_list = self.select_grade_clean(self.data.getlist('select_grade'))
        if not (select_grade_list or title):
            raise forms.ValidationError("Please select {0} or Fill {1} field.".format('Grade Checkbox', 'title'))
        return cleaned_data


class AddSubjectForm(BasicFilterWithGrade):
    hidden_select_stream = forms.CharField(widget=forms.HiddenInput())
    select_stream = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]))
    title = forms.CharField(required=True)

    grade_type = 'multi_select'

    class Meta:
        model = Subject
        fields = ['country', 'select_state', 'select_board', 'select_stream', 'select_grade', 'title', 'description']

    def clean_title(self):
        print('under clean ...')
        self._check_grade_course_subject_title_uniqueness()
        return self.data['title']

    def clean(self):
        cleaned_data = super(AddSubjectForm, self).clean()
        print(cleaned_data)
        self.set_drop_downs_in_form_via_hidden(**{'grade': {'type': self.grade_type}})
        return cleaned_data


class ChangeSubjectForm(BasicChangeFormWithGrade):
    select_stream = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]))
    title = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            subject_obj = kwargs['instance']
            selected_stream = subject_obj.course
            selected_grade = selected_stream.grade
            selected_board = selected_grade.board
            selected_state = selected_board.state
            selected_country = selected_state.country
            print(selected_stream)
            initial = {'select_state': selected_state.id,
                       'title': subject_obj.title,
                       'country': selected_country.id,
                       'select_board': str(selected_board.code),
                       'select_grade': str(selected_grade.code),
                       'select_stream': str(selected_stream.title),
                       }

            kwargs['initial'] = initial
        super(ChangeSubjectForm, self).__init__(*args, **kwargs)
        # /// Common Functions
        country_state = selected_board.get_country_state_list()
        board_list = list(BoardCategory.objects.filter_by_state(selected_state))
        # //// .......
        avail_grades_in_selected_board = ClassCategory.objects.filter_by_board(selected_board)
        avail_stream_in_selected_board = Course.objects.get_distinct_stream_via_board(selected_board.pk)

        print(avail_stream_in_selected_board)

        _set_data = {
                     'SELECT_STATE_OPTIONS': country_state.get('state_list', []),
                     'SELECT_BOARD_OPTIONS': board_list,
                     'SELECT_GRADE_OPTIONS': list(avail_grades_in_selected_board),
                     'SELECT_STREAM_OPTIONS': list(avail_stream_in_selected_board),
                     'grade': {'type': 'radio_select'}
                     }

        self.fields['select_grade'].help_text = PRE_SELECT_GRADE_MSG.format(selected_grade)
        self.set_drop_downs_in_form_via_data_set(**_set_data)
        # set_drop_downs_in_form(self, **_set_data)

    class Meta:
        model = Subject
        fields = ['country', 'select_state', 'select_board', 'select_stream', 'select_grade', 'title', 'description']

    def clean_title(self):
        print('under clean ...')
        self._check_grade_course_subject_title_uniqueness()
        return self.data['title']

    def clean(self):
        cleaned_data = super(ChangeSubjectForm, self).clean()
        # self.set_drop_downs_in_form_via_hidden(**{'grade': {'type': 'multi_select'}})
        return cleaned_data


class AddChapterForm(AddSubjectForm):
    select_grade = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]), help_text='')
    select_subject = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]),
                                     help_text='Please select above fields')
    hidden_select_subject = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.grade_type = 'drop_down_select'
        super(AddChapterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Chapter
        fields = ['country', 'select_state', 'select_board', 'select_stream', 'select_grade', 'select_subject',
                  'title', 'chapter_number', 'description']

    def clean_title(self):
        self._check_grade_course_subject_chapter_title_uniqueness()
        return self.data['title']


class ChangeChapterForm(ChangeSubjectForm):
    select_grade = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]), help_text='')
    select_subject = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]))

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            chapter_obj = kwargs['instance']
            subject_obj = chapter_obj.subject
            selected_stream = subject_obj.course
            selected_grade = selected_stream.grade
            selected_board = selected_grade.board
            selected_state = selected_board.state
            selected_country = selected_state.country

            initial = {'select_state': selected_state.id,
                       'title': chapter_obj.title,
                       'country': selected_country.id,
                       'select_board': str(selected_board.code),
                       'select_grade': str(selected_grade.code),
                       'select_stream': str(selected_stream.title),
                       'select_subject': str(subject_obj.code)
                       }

            kwargs['initial'] = initial
        super(ChangeSubjectForm, self).__init__(*args, **kwargs)
        # /// Common Functions
        country_state = selected_board.get_country_state_list()
        board_list = list(BoardCategory.objects.filter_by_state(selected_state))
        # //// .......
        avail_grades_in_selected_board = ClassCategory.objects.filter_by_board(selected_board)
        avail_stream_in_selected_board = Course.objects.get_distinct_stream_via_board(selected_board.pk)
        avail_subject_in_selected_chapter = Subject.objects.\
            get_distinct_stream_via_grade(selected_stream.title, selected_grade.pk)

        print(avail_subject_in_selected_chapter)
        _set_data = {
                     'SELECT_STATE_OPTIONS': country_state.get('state_list', []),
                     'SELECT_BOARD_OPTIONS': board_list,
                     'SELECT_GRADE_OPTIONS': list(avail_grades_in_selected_board),
                     'SELECT_STREAM_OPTIONS': list(avail_stream_in_selected_board),
                     'SELECT_SUBJECT_OPTIONS': list(avail_subject_in_selected_chapter),
                     'grade': {'type': 'drop_down_select'}
                     }

        self.fields['select_grade'].help_text = PRE_SELECT_GRADE_MSG.format(selected_grade)
        self.set_drop_downs_in_form_via_data_set(**_set_data)

    def clean_title(self):
        self._check_grade_course_subject_chapter_title_uniqueness()
        return self.data['title']

    class Meta:
        model = Chapter
        fields = ['country', 'select_state', 'select_board', 'select_stream', 'select_grade', 'select_subject',
                  'title', 'chapter_number', 'description']


class TopicForm(AddChapterForm):
    select_chapter = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]))
    hidden_select_chapter = forms.CharField(widget=forms.HiddenInput())

    def clean_title(self):
        """Concept name will not be repeated in the same chapter."""
        self._unique_topic_form_title()
        return self.data['title']

    class Meta:
        model = Topic
        fields = ['country', 'select_state', 'select_board', 'select_stream', 'select_grade', 'select_subject',
                  'select_chapter', 'title', 'description']


class ChangeTopicForm(BasicChangeFormWithGrade):
    title = forms.CharField(required=True)
    select_stream = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]))
    select_subject = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]))
    select_chapter = forms.CharField(widget=forms.Select(choices=[('', '--- Select One ---')]))

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            topic_obj = kwargs['instance']
            chapter_obj = topic_obj.chapter
            subject_obj = chapter_obj.subject
            selected_stream = subject_obj.course
            selected_grade = selected_stream.grade
            selected_board = selected_grade.board
            selected_state = selected_board.state
            selected_country = selected_state.country

            initial = {
                       'select_state': selected_state.id,
                       'title': topic_obj.title,
                       'country': selected_country.id,
                       'select_board': str(selected_board.code),
                       'select_grade': str(selected_grade.code),
                       'select_stream': str(selected_stream.title),
                       'select_subject': str(subject_obj.code),
                       'select_chapter': str(chapter_obj.code)
                       }

            kwargs['initial'] = initial
        super(ChangeTopicForm, self).__init__(*args, **kwargs)
        # /// Common Functions
        country_state = selected_board.get_country_state_list()
        board_list = list(BoardCategory.objects.filter_by_state(selected_state))
        # //// .......
        avail_grades_in_selected_board = ClassCategory.objects.filter_by_board(selected_board)
        avail_stream_in_selected_board = Course.objects.get_distinct_stream_via_board(selected_board.pk)
        avail_subject_in_selected_chapter = Subject.objects.\
            get_distinct_stream_via_grade(selected_stream.title, selected_grade.pk)

        avail_chapter_in_selected_subject = Chapter.objects.values_list('code', 'title').filter(subject__pk=subject_obj.code)

        _set_data = {
                     'SELECT_STATE_OPTIONS': country_state.get('state_list', []),
                     'SELECT_BOARD_OPTIONS': board_list,
                     'SELECT_GRADE_OPTIONS': list(avail_grades_in_selected_board),
                     'SELECT_STREAM_OPTIONS': list(avail_stream_in_selected_board),
                     'SELECT_SUBJECT_OPTIONS': list(avail_subject_in_selected_chapter),
                     'SELECT_CHAPTER_OPTIONS': list(avail_chapter_in_selected_subject),
                     'grade': {'type': 'drop_down_select'}
                     }

        self.fields['select_grade'].help_text = PRE_SELECT_GRADE_MSG.format(selected_grade)
        self.set_drop_downs_in_form_via_data_set(**_set_data)

    def clean_title(self):
        """Concept name will not be repeated in the same chapter."""
        self._unique_topic_form_title()
        return self.data['title']

    class Meta:
        model = Topic
        fields = ['country', 'select_state', 'select_board', 'select_stream', 'select_grade', 'select_subject',
                  'select_chapter', 'title', 'description']


