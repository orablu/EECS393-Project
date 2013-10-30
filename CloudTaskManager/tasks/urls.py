from django.conf.urls import patterns, url
from tasks import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<list_id>\d+)/$', views.details, name='details'),
    url(r'^(?P<list_id>\d+)/edit/$', views.edit_list, name='edit_list'),
    url(r'^(?P<list_id>\d+)/save/$', views.save_list, name='save_list'),
    url(r'^(?P<list_id>\d+)/new/$', views.new_task, name='new_task'),
    url(r'^(?P<list_id>\d+)/new/save/$', views.save_new_task, name='save_new_task'),
    url(r'^task/(?P<task_id>\d+)/$', views.edit_task, name='edit_task'),
    url(r'^task/(?P<task_id>\d+)/save/$', views.save_task, name='save_task'),
)
