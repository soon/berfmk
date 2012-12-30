# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.contrib.auth.models import User
from django.contrib.auth.forms  import UserCreationForm, AuthenticationForm
#-------------------------------------------------------------------------------
from accounts.models            import UserProfile
from berfmk.forms               import MyModelForm
from captcha.forms              import ReCaptchaForm, ReCaptchaModelForm
#-------------------------------------------------------------------------------
class RegisterForm(UserCreationForm, ReCaptchaModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class']    = 'full_width'
            self.fields[field].widget.attrs['required'] = ''
    #---------------------------------------------------------------------------
    class Meta(object):
        model   = User
        fields  = ('username', 'email', )
#-------------------------------------------------------------------------------
class LoginForm(AuthenticationForm, ReCaptchaForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class']    = 'full_width'
            self.fields[field].widget.attrs['required'] = ''
#-------------------------------------------------------------------------------
