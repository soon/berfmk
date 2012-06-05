# -*- coding: utf-8 -*-

from django.views.generic.simple    import direct_to_template
from django.shortcuts               import redirect

def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        return direct_to_template(request, 'user/login.hdt')

def register(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        return direct_to_template(request, 'user/register.hdt')

