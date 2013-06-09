# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import stringfilter

from spidermonkey import Runtime
import os

register = template.Library()

@register.filter(needs_autoescape=False)
@stringfilter
def markdown_to_html(text):
    def loadfile(fname):
     return open(fname).read()

    rt = Runtime()
    cx = rt.new_context()
    cx.add_global('loadfile', loadfile)
    cx.add_global('mytext', text)

    return cx.execute(
       u'eval(loadfile("{0}/berfmk/static/js/pagedown/Markdown.Converter.js"));'
       u'eval(loadfile("{0}/berfmk/static/js/pagedown/Markdown.Sanitizer.js"));'
       u'var converter = Markdown.getSanitizingConverter();'
       u'converter.makeHtml(mytext);'.format(os.getcwd())
    )
