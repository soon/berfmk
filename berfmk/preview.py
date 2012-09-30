# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.contrib.formtools.preview   import FormPreview
#-------------------------------------------------------------------------------
class MyFormPreview(FormPreview):
    #---------------------------------------------------------------------------
    '''
        The difference between MyFormPreview and FormPreview is overloading
        post_post function, that calling function done if form is valid, but
        hash is empty. Now, we can add some content without preview
    '''
    #---------------------------------------------------------------------------
    def post_post(self, request):
        f = self.form(request.POST, auto_id=self.get_auto_id())
        if f.is_valid():
            if request.POST.get(self.unused_name('hash'), '') == '':
                return self.done(request, f.cleaned_data)
        return super(MyFormPreview, self).post_post(request)
#-------------------------------------------------------------------------------
