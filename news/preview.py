# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.http        import HttpResponseRedirect
#-------------------------------------------------------------------------------
from berfmk.preview     import MyFormPreview
from news.forms         import NewsForm
from news.models        import News
#-------------------------------------------------------------------------------
class NewsFormPreview(MyFormPreview):
    preview_template    = 'news/news_add_preview.hdt'
    form_template       = 'news/news_add_form.hdt'
    #---------------------------------------------------------------------------
    def done(self, request, cleaned_data):
        f = NewsForm(cleaned_data)
        n = f.save(commit = False)
        n.author = request.user
        n.save()
        f.save_m2m()
        return HttpResponseRedirect(n.get_absolute_url())
    #---------------------------------------------------------------------------
    def get_context(self, request, form):
        context = super(NewsFormPreview, self).get_context(request, form)
        fields_to_exclude = []
        if not request.user.has_perm('news.add_sitenews'):
            fields_to_exclude.append('siteNews')
        if not request.user.has_perm('news.add_schoolnews'):
            fields_to_exclude.append('schoolNews')
        if not request.user.has_perm('news.add_hidden'):
            fields_to_exclude.append('hidden')
        if request.user.has_perm('news.change_only_hidden'):
            fields_to_exclude.extend(['schoolNews', 'siteNews', 'hidden'])
        context['form'].exclude_fields(fields_to_exclude)
        return context
#-------------------------------------------------------------------------------
