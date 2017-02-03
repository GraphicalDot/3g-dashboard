from django.conf.urls import url

from . import views

app_name = 'task_management'

urlpatterns = [
    url(r'^$', views.login_user, name='login'),
    url(r'^logout/$', views.login_user, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^(?P<task_id>[0-9]+)/$', views.edit_task, name='task')
]