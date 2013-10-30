from django.conf.urls import patterns, url
from tasks import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'), # e.g. /tasklists/
        url(r'^(?P<list_id>\d+)/$', views.details, name='details'), # e.g. /tasklists/0/
        url(r'^(?P<list_id>\d+)/edit/$', views.edit, name='edit'), # e.g. /tasklists/0/edit/
        url(r'^(?P<list_id>\d+)/save/$', views.save, name='save'),
)

