from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from django.contrib.auth.views import login, logout
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^tasklists/', include('tasks.urls', namespace='tasks')),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
)
