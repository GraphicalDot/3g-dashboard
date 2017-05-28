from django.conf.urls import url

from . import views

app_name = 'task_management'

urlpatterns = [
    url(r'^$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^select_uploader$', views.get_uploaders, name='select_uploader'),
    url(r'^(?P<task_id>[0-9]+)/edit$', views.edit_task, name='edit_task'),
    url(r'^(?P<uploader_id>[0-9]+)/assign_task$', views.assign_task, name='assign_task'),
    url(r'^(?P<task_id>[0-9]+)/delete/$', views.delete_task, name='delete_task'),
    url(r'^(?P<task_id>[0-9]+)/upload/$', views.upload_task_data, name='upload'),
    url(r'^(?P<task_id>[0-9]+)/complete/$', views.task_complete, name='task_complete'),

    url(r'^(?P<uploader_id>[0-9]+)/test_ajax$', views.permissions)
]
