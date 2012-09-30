from django.conf.urls   import patterns, include, url
#-------------------------------------------------------------------------------
from news.views         import NewsList
from news.forms         import NewsForm
from news.preview       import NewsFormPreview
from berfmk.decorators  import any_permission_required
from news.utils         import can_add_news
from django.contrib.auth.decorators import login_required
#-------------------------------------------------------------------------------
urlpatterns = patterns(
    '',
    # url(r'^(?P<direction>|site/|school/)$', 'news.views.news', {'page': '1'}),
    url(r'^(?P<direction>|site/|school/)$', NewsList.as_view(), {'page': 1}),
    url(
        r'^(?P<direction>|site/|school/)page/(?P<page>[1-9]\d{0,3})/$',
        NewsList.as_view()
    ),
    url(r'^(?P<id>[1-9]\d{0,4})/$', 'news.views.news_page'),
    url(r'^add/$', can_add_news(NewsFormPreview(NewsForm))),
    # url(r'^preview/$', 'news.views.add_news', {'preview': True}),
    url(r'^(?P<id>[1-9]\d{0,4})/edit/$', 'news.views.edit_news'),
    url(
        r'^(?P<id>[1-9]\d{0,4})/edit/preview/$',
        'news.views.edit_news',
        {'preview': True}
    ),
)
#-------------------------------------------------------------------------------
