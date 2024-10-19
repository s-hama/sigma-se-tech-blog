from django.urls import path, re_path, include
from django.http import HttpResponse
from . import views
# import logging 

# logging.getLogger('command').debug(' >>> ' + __name__)

urlpatterns = [ 
    path('', views.PostIndexView.as_view(), name='index'), 

    re_path(r'^detail/(?P<pk>[0-9]+)/$',
        views.PostDetailView.as_view(), name='detail'),
 
    re_path(r'^category/(?P<big>\w+)/(?P<small>\w+)/$',
        views.CategoryView.as_view(), name='category'),
 
    re_path(r'^category/(?P<big>\w+)/$',
        views.CategoryView.as_view(), name='category'),
 
    re_path(r'^tag/(?P<tag>\w+)/$', 
        views.TagView.as_view(), name='tag'),

    re_path(r'^profile/$',
        views.ProfileView.as_view(), name='profile'),

    re_path(r'^contact/$',
        views.ContactView.as_view(), name='contact'),

    re_path(r'^ppolicy/$',
        views.PpolicyView.as_view(), name='ppolicy'),

    # re_path(r'^ads.txt', lambda x: HttpResponse('google.com, pub-4029756773390765, DIRECT, f08c47fec0942fa0', content_type='text/plain'), name='adsfile'),
]
