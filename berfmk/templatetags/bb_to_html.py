from django                         import template
from django.template.defaultfilters import stringfilter

import re

register = template.Library()

@register.filter(needs_autoescape = False)
@stringfilter
def bb_to_html(text):
    text = text.replace('\r', '<br>')
    text = re.sub(r'\[b\](.+?)\[/b\]', r'<strong>\1</strong>', text)
    text = re.sub(r'\[i\](.+?)\[/i\]', r'<em>\1</em>', text)
    text = re.sub(
            r'\[u\](.+?)\[/u\]',
            r'<span style="text-decoration:underline;">\1</span>',
            text
        )
    text = re.sub(r'\[s\](.+?)\[/s\]', r'<del>\1</del>', text)
    text = re.sub(r'\[url\s*=\s*(.+?)\](.+?)\[/url\]', r'<a href="\1">\2</a>', text)
    text = re.sub(r'\[url\s*=\s*(.+?)\]\[/url\]', r'<a href="\1">\1</a>', text)
    text = re.sub(
            r'\[size\s*=\s*(\d+?)\](.+?)\[/size\]',
            r'<span style="font-size:\1pt;">\2</span>',
            text
        )
    text = re.sub(
            r'\[color\s*=\s*(.+?)\](.*?)\[/color\]',
            r'<span style="color:\1">\2</span>',
            text
        )
    return text
