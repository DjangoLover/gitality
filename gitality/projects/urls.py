from django.conf.urls import patterns, url


urlpatterns = patterns('projects.views',
    url(r'^$', 'project_list', name='project_list'),
    url(r'^create/$', 'project_create', name='project_create'),
    url(r'^(?P<slug>[-\w]+)/$', 'project_detail', name='project_detail'),
    url(r'^(?P<slug>[-\w]+)/update/$', 'project_update', name='project_update'),
)
