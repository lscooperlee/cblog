from django.conf.urls import patterns, url

urlpatterns=patterns('',
    url("^$",'cblog.views.cblog_index', name='reverse_cblog_index'),
    url(r'login/$', 'cblog.views.cblog_login',name='reverse_cblog_login'),
    url(r'logout/$', 'cblog.views.cblog_logout',name='reverse_cblog_logout'),
    url(r'edit/$', 'cblog.views.cblog_edit',name='reverse_cblog_edit'),
    url(r'edit/(?P<id>\d*?)/$', 'cblog.views.cblog_edit',name='reverse_cblog_edit'),
    url(r'delete/(?P<id>\d*?)$', 'cblog.views.cblog_delete',name='reverse_cblog_delete' ),
)
