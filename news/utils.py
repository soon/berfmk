# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from berfmk.decorators import any_permission_required

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

