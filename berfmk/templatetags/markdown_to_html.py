# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django                         import template
from django.template.defaultfilters import stringfilter
#-------------------------------------------------------------------------------
from markdown                       import markdown
#-------------------------------------------------------------------------------
register = template.Library()
#-------------------------------------------------------------------------------
@register.filter(needs_autoescape = False)
@stringfilter
def markdown_to_html(text):
    return markdown(text)
#-------------------------------------------------------------------------------