from django.conf.urls import patterns, url

urlpatterns=patterns('',
    url("^$",'cblog.views.cblog_index', name='reverse_cblog_index'),
    url(r'login/$', 'cblog.views.cblog_login',name='reverse_cblog_login'),

)
