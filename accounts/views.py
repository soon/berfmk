# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.views.generic.simple    import direct_to_template
from django.shortcuts               import redirect
from django.contrib                 import auth
from django.contrib.auth            import logout as user_logout
from django.contrib.auth.models     import User
#-------------------------------------------------------------------------------
import re
#-------------------------------------------------------------------------------
def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['input_username']
        password = request.POST['input_password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return direct_to_template(
                    request,
                    'user/login.hdt', {
                        'error': True,
                        'username': username
                    }
                )
    else:
        return direct_to_template(request, 'user/login.hdt')
#-------------------------------------------------------------------------------
def logout(request):
    if request.user.is_authenticated():
        user_logout(request)
    return redirect('/')
#-------------------------------------------------------------------------------
def register(request):
    if request.user.is_authenticated():
        return redirect('/')
    errors = {
        'username': False,
        'username_is_already_used': False,
        'email': False,
        'email_is_already_used': False,
        'password': False,
        'password_repeat': False
    }
    if request.method == 'POST':
        username = request.POST['input_username']
        if not re.match(r'^[0-9A-Za-z_]{4,16}$', username):
            errors['username'] = True
            username = ''

        email = request.POST['input_email']
        if not re.match(
                r'^[A-Za-z0-9\.\-_]{1,64}@[a-z0-9\.\-_]{1,255}\.[a-z]{2,4}$',
                email
            ) or len(email) > 75:
            errors['email'] = True
            email = ''

        password = request.POST['input_password']
        if not 4 <= len(password) <= 128:
            errors['password'] = True

        password_repeat = request.POST['input_password_repeat']
        if password != password_repeat:
            errors['password_repeat'] = True

        if not errors['username']:
            if User.objects.filter(username = username):
                errors['username_is_already_used'] = True
            if User.objects.filter(email = unicode.lower(email)):
                errors['email_is_already_used'] = True

        if not True in errors.values():
            User.objects.create_user(username, email, password)
            user = auth.authenticate(username = username, password = password)
            auth.login(request, user)
            return redirect('/')
        else:
            return direct_to_template(
                    request,
                    'user/register.hdt', {
                        'errors': errors,
                        'username': username,
                        'email': email
                    }
                )
    else:
        return direct_to_template(request, 'user/register.hdt')
#-------------------------------------------------------------------------------
