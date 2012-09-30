# -*- codeing: utf-8 -*-
#-------------------------------------------------------------------------------
from django.shortcuts               import get_object_or_404
from django.http                    import Http404
from django.contrib.auth.decorators import login_required
#-------------------------------------------------------------------------------
from news.models                    import News
from berfmk.utils                   import get_number_from_param_or_404
from berfmk.decorators              import any_permission_required
#-------------------------------------------------------------------------------
def get_news_or_404(id):
    return get_object_or_404(News, id = get_number_from_param_or_404(id))
#-------------------------------------------------------------------------------
@any_permission_required(
    perms = (
        'news.add_sitenews',
        'news.add_schoolnews',
        'news.add_only_hidden',
        'news.add_hidden',
    )
)
@login_required
def can_add_news(function):
    pass
#-------------------------------------------------------------------------------
