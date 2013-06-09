from django.conf.urls   import patterns, include, url

from forum.views        import ForumList, ForumDetail, SectionDetail
from forum.views        import SubSectionDetail, TopicDetail

urlpatterns = patterns(
    '',
    url(
        r'^'
        r'$',

        ForumList.as_view()
    ),
    url(
        r'^'
            r'(?P<forum>[^/\d]{1,32})/'
        r'$',

        ForumDetail.as_view()
    ),
    url(
        r'^'
            r'(?P<forum>[^/\d]{1,32})/'
            r'(?P<section>[^/\d]{1,32})/'
        r'$',

        SectionDetail.as_view(),
    ),
    url(
        r'^'
            r'(?P<forum>[^/\d]{1,32})/'
            r'(?P<section>[^/\d]{1,32})/'
            r'(?P<sub_section>[^/\d]{1,32})/'
        r'$',

        SubSectionDetail.as_view()
    ),
    url(
        r'^'
            r'(?P<forum>[^/]{1,32})/'
            r'(?P<section>[^/]{1,32})/'
            r'(?P<topic>\d{1,9})/'
        r'$',

        TopicDetail.as_view(),
        {'page': 1}
    ),
        url(
        r'^'
            r'(?P<forum>[^/]{1,32})/'
            r'(?P<section>[^/]{1,32})/'
            r'(?P<topic>\d{1,9})/'
            r'page/(?P<page>[1-9]\d{0,3})/'
        r'$',

        TopicDetail.as_view()
    ),
)
