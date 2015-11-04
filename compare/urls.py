from django.conf.urls import patterns, url
urlpatterns = patterns('compare.views',
    url(r'^api/$', 'api', name='main_api'),
    )
