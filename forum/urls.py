from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^$', 'forum.views.forums'),
    url(r'^(?P<forum>[^/]{1,32})/$', 'forum.views.sections'),
    url(
        r'^(?P<forum>[^/]{1,32})/(?P<section>[^/]{1,32})/$',
        'forum.views.topics'
    ),
    url(
        r'^(?P<forum>[^/]{1,32})/(?P<section>[^/]{1,32})/(?P<topic>\d{1,9})/$',
        'forum.views.posts',
        {'page': 1}
    ),
    url(
        r'^(?P<forum>[^/]{1,32})/(?P<section>[^/]{1,32})/(?P<topic>\d{1,9})' + \
        r'/page/(?P<page>[1-9]\d{0,3})/',
        'forum.views.posts'
    ),
    url(
        r'^(?P<forum>[^/]{1,32})/(?P<section>[^/]{1,32})/add-topic/$',
        'forum.views.add_topic',
        {'preview': False}
    ),
    url(
        r'^(?P<forum>[^/]{1,32})/(?P<section>[^/]{1,32})/add-topic/preview/$',
        'forum.views.add_topic',
        {'preview': True}
    ),
    url(
        r'^(?P<forum>[^/]{1,32})/(?P<section>[^/]{1,32})/(?P<topic>\d{1,9})' + \
        r'/add-post/$',
        'forum.views.add_post',
        {'preview': False}
    ),
    url(
        r'^(?P<forum>[^/]{1,32})/(?P<section>[^/]{1,32})/(?P<topic>\d{1,9})' + \
        r'/add-post/preview/$',
        'forum.views.add_post',
        {'preview': True}
    ),
)