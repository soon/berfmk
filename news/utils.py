# -*- codeing: utf-8 -*-
#-------------------------------------------------------------------------------
from django.shortcuts   import get_object_or_404
from django.http        import Http404
#-------------------------------------------------------------------------------
from news.models        import News
from berfmk.utils       import get_number_from_param_or_404
#-------------------------------------------------------------------------------
def get_news_or_404(id):
    return get_object_or_404(News, id = get_number_from_param_or_404(id))
#-------------------------------------------------------------------------------
