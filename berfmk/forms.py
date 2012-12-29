# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.forms               import ModelForm
from django.contrib.auth.forms  import AuthenticationForm
#-------------------------------------------------------------------------------
class MyModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyModelForm, self).__init__(*args, **kwargs)

        tabindex = 1
        for field in self.fields:
            self.fields[field].widget.attrs['tabindex'] = tabindex
            tabindex += 1
    #---------------------------------------------------------------------------
    def exclude_fields(self, fields):
        for field in fields:
            if field in self.fields:
                del self.fields[field]
#-------------------------------------------------------------------------------
class MyAuthenticationForm(AuthenticationForm):
    class Meta(object):
        pass
#-------------------------------------------------------------------------------
