# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django         import template
#-------------------------------------------------------------------------------
from forum.models   import Forum
#-------------------------------------------------------------------------------
register = template.Library()
#-------------------------------------------------------------------------------
@register.filter(needs_autoescape = False)
def get_all_forums():
    return Forum.objects.all().values('title', 'address')
#-------------------------------------------------------------------------------