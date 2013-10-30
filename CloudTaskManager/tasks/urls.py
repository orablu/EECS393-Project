from django.conf.urls import patterns, url
from tasks import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^addList/$', views.addList, name='addList'),
        url(r'^(?P<list_id>\d+)/$', views.details, name='details'),
        url(r'^(?P<list_id>\d+)/edit/$', views.edit, name='edit'),
        url(r'^(?P<list_id>\d+)/save/$', views.save, name='save'),
        url(r'^tasks/(?P<task_id>\d+)/delete/$', views.delete_task, name='delete_task'),
)
