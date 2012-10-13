# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.forms           import TextInput, Textarea
from django.forms.models    import fields_for_model
#-------------------------------------------------------------------------------
from berfmk.forms           import MyModelForm
from news.models            import News
#-------------------------------------------------------------------------------
class NewsForm(MyModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)

        tabindex = 1
        for field in self.fields:
            self.fields[field].widget.attrs['tabindex'] = tabindex
            tabindex = tabindex + 1
    #---------------------------------------------------------------------------
    class Meta(object):
        model   = News
        fields  = ('title', 'text_block', 'schoolNews', 'siteNews', 'hidden')
        widgets = {
            'title'     : TextInput(
                attrs = {'required': '', 'class': 'full_width'}
            ),
            'text_block': Textarea(
                attrs = {
                    'required'  : '',
                    'rows'      : 20,
                    'class'     : 'full_width',
                    'maxlength' : fields_for_model(
                        News, fields = ('text_block', )
                    )['text_block'].max_length
                    # I have no idea why it not set automatically
                }
            )
        }
#-------------------------------------------------------------------------------
