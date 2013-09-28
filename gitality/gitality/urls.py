from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'gitality.views.home', name='home'),
    # url(r'^gitality/', include('gitality.foo.urls')),
    url(r'^$', 'core.views.home', name='home'),
    url(r'^auth/', include('social_auth.urls')),
    url(r'^projects/', include('projects.urls', namespace='projects')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
