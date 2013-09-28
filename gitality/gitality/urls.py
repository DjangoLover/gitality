from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'gitality.views.home', name='home'),
    # url(r'^gitality/', include('gitality.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
