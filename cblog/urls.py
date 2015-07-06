from django.conf.urls import patterns, url

urlpatterns=patterns('',
    url("^$",'cblog.views.cblog_index', name='reverse_cblog_index'),
    url(r'^login/$', 'cblog.views.cblog_login',name='reverse_cblog_login'),
    url(r'^logout/$', 'cblog.views.cblog_logout',name='reverse_cblog_logout'),
    url(r'^edit/$', 'cblog.views.cblog_edit',name='reverse_cblog_edit'),
    url(r'^edit/(?P<id>\d*)/$', 'cblog.views.cblog_edit',name='reverse_cblog_edit'),
    url(r'^delete/(?P<id>\d*)/$', 'cblog.views.cblog_delete',name='reverse_cblog_delete' ),
    url(r'^comment/(?P<entry_id>\d*)/$', 'cblog.views.cblog_edit_comment', name='reverse_cblog_edit_comment'),
    url(r'^comment/(?P<entry_id>\d*)/(?P<comment_id>\d*)/$', 'cblog.views.cblog_edit_comment', name='reverse_cblog_edit_comment'),
    url(r'^delete_comment/(?P<entry_id>\d*)/(?P<comment_id>\d*)/$', 'cblog.views.cblog_delete_comment', name='reverse_cblog_delete_comment'),
    url(r'^category/$', 'cblog.views.cblog_category', name='reverse_cblog_category'),
    url(r'^category/(?P<category_id>\d*)/$', 'cblog.views.cblog_category', name='reverse_cblog_category'),
    url(r'^delete_category/(?P<category_id>\d*)/$', 'cblog.views.cblog_delete_category', name='reverse_cblog_delete_category'),
    url(r'^date_list/$', 'cblog.views.cblog_datelist_article', name='reverse_cblog_datelist_article'),
    url(r'^date_list/(?P<year>\d{4})/$', 'cblog.views.cblog_datelist_article', name='reverse_cblog_datelist_article'),
    url(r'^entry/(?P<slug>\w+)/(?P<id>\d*)/$','cblog.views.cblog_entry',name='reverse_cblog_entry'),
)
