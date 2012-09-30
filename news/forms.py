# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from berfmk.forms   import MyModelForm
from news.models    import News
#-------------------------------------------------------------------------------
class NewsForm(MyModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)

        self.fields['title'].label = 'Заголовок'
        self.fields['title'].widget.attrs['required'] = ''
        self.fields['title'].widget.attrs['class'] = "full_width"
        self.fields['title'].widget.attrs['class'] = "full_width"

        self.fields['text_block'].label = 'Текст новости'
        self.fields['text_block'].widget.attrs['required'] = ''
        self.fields['text_block'].widget.attrs['rows'] = 20
        self.fields['text_block'].widget.attrs['class'] = "full_width"

        self.fields['schoolNews'].label = 'Новость для школы'
        self.fields['siteNews'].label = 'Новость для сайта'
        self.fields['hidden'].label = 'Скрытая новость'

        tabindex = 1
        for field in self.fields:
            self.fields[field].widget.attrs['tabindex'] = tabindex
            tabindex = tabindex + 1
    #---------------------------------------------------------------------------
    class Meta:
        model = News
        fields = ('title', 'text_block', 'schoolNews', 'siteNews', 'hidden')
#-------------------------------------------------------------------------------
