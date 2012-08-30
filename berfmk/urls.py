from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^$', 'news.views.news', {'direction': '', 'page': '1'}),
    url(r'^news/', include('news.urls')),
    url(r'^forum/', include('forum.urls')),
    # url(r'^forum/$', 'forum.views.forum_main'),
    url(r'^art/(?P<name>.+)/$', 'art.views.art_page'),
    url(r'^login/$', 'accounts.views.login'),
    url(r'^logout/$', 'accounts.views.logout'),
    url(r'^register/$', 'accounts.views.register'),
    # Examples:
    # url(r'^$', 'berfmk.views.home', name='home'),
    # url(r'^berfmk/', include('berfmk.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
