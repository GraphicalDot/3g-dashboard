# from django.shortcuts import render
from constants.global_constant import PARENT_KEY_CHILD_VALUE
from django.http import JsonResponse
from django.template.loader import get_template
from django.template import Context
# from course_management.models import Course


def get_ajax_response(obj_list, file_path, key_name, value_name='title', html_add_on_id=None):
    """
    """
    tempo = [{'option_data': '', 'hidden_field_value': ''}]
    try:
        hidden_field_value = ''
        t = get_template(file_path)
        html = t.render(Context({'values': obj_list}))

        for obj in obj_list:
            if key_name == 'id':
                hidden_field_value = hidden_field_value + '||' + str(obj.id) + ':'
            elif key_name == 'title':
                hidden_field_value = hidden_field_value + '||' + str(obj.title) + ':'
            else:
                hidden_field_value = hidden_field_value + '||' + str(obj.code) + ':'

            if value_name == 'title':
                hidden_field_value = hidden_field_value + obj.title
            elif value_name == 'name_define':
                hidden_field_value += str(obj)

        if not obj_list:
            tempo[0]['null_option_message'] = 'Not available please select another options'

        tempo[0]['option_data'] = html
        tempo[0]['hidden_field_value'] = hidden_field_value
        if html_add_on_id:
            tempo[0]['html_add_on_id'] = html_add_on_id

    except Exception as e:
        print(e.args)

    return tempo


def filter_field(request):
    print(request.POST)
    if request.method == 'POST':
        filter_on = request.POST['field_name']
        model_name = request.POST['model_name']
        model_obj = PARENT_KEY_CHILD_VALUE.get(filter_on)
        data = []

        data_list = model_obj.objects.all()

        if filter_on == 'country':
            data = get_ajax_response(data_list, 'form_filter/_state_filter_options.html', 'id')
            return JsonResponse(data, safe=False)

        if filter_on == 'state':
            data_list = data_list.filter(state__id=request.POST['state'])
            data = get_ajax_response(data_list, 'form_filter/_options.html', 'code')
            return JsonResponse(data, safe=False)

        # SUBJECT FORM CALLS
        if model_name == 'subject':
            if filter_on == 'board':
                data_list = PARENT_KEY_CHILD_VALUE.get('grade').objects.\
                    filter(grade__board__pk=request.POST['board']).order_by('title', '-created').distinct('title')
                data = get_ajax_response(data_list, 'form_filter/_stream_title_select.html', 'title',
                                         html_add_on_id='select_stream')

            if filter_on == 'grade':
                print('under if grade ...')
                pass

            if filter_on == 'stream':
                stream_title = request.POST['stream']
                data_list = PARENT_KEY_CHILD_VALUE.get('board').objects.filter(board__pk=request.POST['board'],
                                                                               course__title=stream_title)
                print('----', data_list)
                data = get_ajax_response(data_list, 'form_filter/_grade_options.html', 'code',
                                         html_add_on_id='select_grade')

            return JsonResponse(data, safe=False)

        # CHAPTER FORM CALLS
        if model_name == 'chapter':
            if filter_on == 'board':
                data_list = PARENT_KEY_CHILD_VALUE.get('grade').objects.\
                    filter(grade__board__pk=request.POST['board']).order_by('title', '-created').distinct('title')
                data = get_ajax_response(data_list, 'form_filter/_stream_title_select.html', 'title',
                                         html_add_on_id='select_stream')

            if filter_on == 'grade':
                grades_list = request.POST.get('select_grade')
                stream_title = request.POST.get('stream')
                board_pk = request.POST.get('board')
                data_list = PARENT_KEY_CHILD_VALUE.get('stream').objects.\
                    filter(course__grade__pk=grades_list, course__title=stream_title, course__grade__board__pk=board_pk)
                data = get_ajax_response(data_list,
                                         'form_filter/_options.html',
                                         'code', value_name='name_define',
                                         html_add_on_id='select_subject')

            if filter_on == 'stream':
                stream_title = request.POST['stream']
                data_list = PARENT_KEY_CHILD_VALUE.get('board').objects.filter(board__pk=request.POST['board'],
                                                                               course__title=stream_title)
                data = get_ajax_response(data_list, 'form_filter/_options.html', 'code',
                                         html_add_on_id='select_grade')

            return JsonResponse(data, safe=False)

        # TOPIC FORM CALLS
        if model_name == 'topic':
            if filter_on == 'board':
                data_list = PARENT_KEY_CHILD_VALUE.get('grade').objects.\
                    filter(grade__board__pk=request.POST['board']).order_by('title', '-created').distinct('title')
                data = get_ajax_response(data_list, 'form_filter/_stream_title_select.html', 'title',
                                         html_add_on_id='select_stream')

            if filter_on == 'stream':
                stream_title = request.POST['stream']
                data_list = PARENT_KEY_CHILD_VALUE.get('board').objects.filter(board__pk=request.POST['board'],
                                                                               course__title=stream_title)
                data = get_ajax_response(data_list, 'form_filter/_options.html', 'code',
                                         html_add_on_id='select_grade')

            if filter_on == 'grade':
                grades_list = request.POST.get('select_grade')
                stream_title = request.POST.get('stream')
                board_pk = request.POST.get('board')
                data_list = PARENT_KEY_CHILD_VALUE.get('stream').objects.\
                    filter(course__grade__pk=grades_list, course__title=stream_title,
                           course__grade__board__pk=board_pk)
                data = get_ajax_response(data_list,
                                         'form_filter/_options.html',
                                         'code', value_name='name_define',
                                         html_add_on_id='select_subject')

            if filter_on == 'subject':
                selected_subject_pk = request.POST.get('subject')
                data_list = PARENT_KEY_CHILD_VALUE.get('subject').objects.filter(subject__pk=selected_subject_pk)
                data = get_ajax_response(data_list,
                                         'form_filter/_options.html',
                                         'code')

            return JsonResponse(data, safe=False)

        if model_name == 'course':
            if filter_on == 'board':
                data_list = data_list.filter(board__pk=request.POST['board'])
                # data_list = data_list.exclude(title__in=_used_titles).distinct('title')
                data = get_ajax_response(data_list, 'form_filter/_grade_options.html', 'code')
                return JsonResponse(data, safe=False)

        if filter_on == 'stream':
            data_list = data_list.filter(course__code=request.POST['stream'])
            data = get_ajax_response(data_list, 'form_filter/_options.html', 'code')

        if filter_on == 'subject':
            data_list = data_list.filter(subject__code=request.POST['subject'])
            data = get_ajax_response(data_list, 'form_filter/_options.html', 'code')

        if filter_on == 'board':
            _used_titles = data_list.values_list('title').filter(board=request.POST['board'])

            data_list = data_list.exclude(title__in=_used_titles).distinct('title')
            data = get_ajax_response(data_list, 'form_filter/_grade_options.html', 'code')

        return JsonResponse(data, safe=False)

# Create your views here.
