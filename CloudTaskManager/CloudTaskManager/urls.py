from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('tasks.urls', namespace='tasks')),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'tasks/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)
