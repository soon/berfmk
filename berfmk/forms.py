# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.forms import ModelForm
#-------------------------------------------------------------------------------
class MyModelForm(ModelForm):
    def exclude_fields(self, fields):
        for field in fields:
            if field in self.fields:
                del self.fields[field]
#-------------------------------------------------------------------------------
