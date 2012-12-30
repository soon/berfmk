# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.forms               import ModelForm, Form
#-------------------------------------------------------------------------------
class MyForm(Form):
    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)

        tabindex = 1
        for field in self.fields:
            print self.fields[field].widget, tabindex
            self.fields[field].widget.attrs['tabindex'] = tabindex
            tabindex += 1
    #---------------------------------------------------------------------------
    def exclude_fields(self, fields):
        for field in fields:
            if field in self.fields:
                del self.fields[field]
#-------------------------------------------------------------------------------
class MyModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MyModelForm, self).__init__(*args, **kwargs)

        tabindex = 1
        for field in self.fields:
            print self.fields[field].widget, tabindex
            self.fields[field].widget.attrs['tabindex'] = tabindex
            print self.fields[field].widget.attrs['tabindex'], tabindex
            tabindex += 1
    #---------------------------------------------------------------------------
    def exclude_fields(self, fields):
        for field in fields:
            if field in self.fields:
                del self.fields[field]
#-------------------------------------------------------------------------------
