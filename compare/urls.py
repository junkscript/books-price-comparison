from django.conf.urls import patterns, url
urlpatterns = patterns('compare.views',
    url(r'^home/$', 'home_page', name='home_page'),
    url(r'^search/$', 'web_search', name='web_search'),
    url(r'^detail/$', 'product_detail', name='product_detail'),
    )
