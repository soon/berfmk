# -*- coding: utf-8 -*-

from django import template

register = template.Library()

@register.filter(is_safe = True)
def product(a, b):
    return int(a) * int(b)
