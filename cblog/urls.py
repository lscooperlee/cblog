from django.conf.urls import patterns, url

urlpatterns=patterns('',
    url("^$",'cblog.views.cblog_index', name='reverse_cblog_index'),
    url(r'login/$', 'cblog.views.cblog_login',name='reverse_cblog_login'),
    url(r'logout/$', 'cblog.views.cblog_logout',name='reverse_cblog_logout'),
    url(r'create/$', 'cblog.views.cblog_create',name='reverse_cblog_create'),
)
