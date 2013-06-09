# -*- coding: utf-8 -*-

from django.conf.urls   import patterns, include, url

from news.views         import NewsList, NewsView, NewsUpdate, NewsCreate
from news.forms         import NewsForm
from news.preview       import NewsFormPreview
from news.utils         import can_add_news

urlpatterns = patterns(
    '',
    url(r'^(?P<direction>|site/|school/)$', NewsList.as_view(), {'page': 1}),
    url(
        r'^(?P<direction>|site/|school/)page/(?P<page>[1-9]\d{0,3})/$',
        NewsList.as_view()
    ),
    url(r'^(?P<pk>[1-9]\d{0,4})/$', NewsView.as_view()),
    url(r'^add/$', can_add_news(NewsCreate.as_view())),
    url(r'^(?P<pk>[1-9]\d{0,4})/edit/$', NewsUpdate.as_view()),
)
