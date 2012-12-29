# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.conf.urls   import patterns, include, url
#-------------------------------------------------------------------------------
from news.views         import NewsList
from accounts.views     import RegisterView, LoginView
#-------------------------------------------------------------------------------
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
urlpatterns = patterns(
    '',
    # url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^$', NewsList.as_view(), {'direction': '', 'page': '1'}),
    url(r'^news/', include('news.urls')),
    url(r'^forum/', include('forum.urls')),
    url(r'^art/(?P<name>.+)/$', 'art.views.art_page'),
    # url(r'^login/$', 'accounts.views.login'),
    url(r'^logout/$', 'accounts.views.logout'),
    # url(r'^register/$', 'accounts.views.register'),
    url(r'^login/$', LoginView.as_view()),
    url(r'^register/$', RegisterView.as_view()),
    # Examples:
    # url(r'^$', 'berfmk.views.home', name='home'),
    # url(r'^berfmk/', include('berfmk.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
#-------------------------------------------------------------------------------
