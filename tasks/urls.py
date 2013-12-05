from django.conf.urls import patterns, url
from tasks import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^add/$', views.add_list, name='add_list'),
    url(r'^(?P<list_id>\d+)/$', views.details, name='details'),
    url(r'^(?P<list_id>\d+)/edit/$', views.edit_list, name='edit_list'),
    url(r'^(?P<list_id>\d+)/delete/$', views.delete_list, name='delete_list'),
    url(r'^(?P<list_id>\d+)/share/$', views.share_list, name='share_list'),
    url(r'^(?P<list_id>\d+)/add/$', views.add_task, name='add_task'),
    url(r'^tasks/(?P<task_id>\d+)/$', views.edit_task, name='edit_task'),
    url(r'^tasks/(?P<task_id>\d+)/delete/$', views.delete_task, name='delete_task'),
    url(r'^tasks/(?P<task_id>\d+)/check/$', views.check_task, name='check_task'),
)
