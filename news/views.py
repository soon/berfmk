# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.shortcuts               import render_to_response
from django.views.generic           import ListView, CreateView
from django.views.generic.detail    import DetailView
from django.views.generic.edit      import UpdateView
from django.http                    import Http404, HttpResponseRedirect
#-------------------------------------------------------------------------------
from news.models                    import News
from news.forms                     import NewsForm
#-------------------------------------------------------------------------------
class NewsList(ListView):
    model               = News
    context_object_name = 'news'
    paginate_by         = 10
    template_name       = 'news/news.hdt'
    #---------------------------------------------------------------------------
    def get_queryset(self):
        direction = self.kwargs['direction']
        news = News.objects.filter(hidden = False)
        if direction == 'site/':
            news = news.filter(siteNews = True)
        elif direction == 'school/':
            news = news.filter(schoolNews = True)
        elif direction != '':
            raise Http404()
        return news
    #---------------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        context = super(NewsList, self).get_context_data(**kwargs)
        user = self.request.user

        direction = self.kwargs['direction']
        context['can_add'] = user.has_perm('news.add_%snews' % direction[:-1]) \
            or user.has_perm('news.add_hidden') \
            or user.has_perm('news.add_only_hidden')

        can_view_hidden = user.has_perm('news.view_hidden')
        hidden_news = News.objects.filter(hidden = True) if can_view_hidden \
            else []
        if direction == 'site/':
            context['direction'] = ' сайта'
            if hidden_news:
                hidden_news = hidden_news.filter(siteNews = True)
        elif direction == 'school/':
            context['direction'] = ' школы'
            if hidden_news:
                hidden_news = hidden_news.filter(schoolNews = True)
        context['hidden_news'] = hidden_news


        return context
#-------------------------------------------------------------------------------
class NewsView(DetailView):
    model               = News
    context_object_name = 'news'
    template_name       = 'news/news_view.hdt'
    #---------------------------------------------------------------------------
    def get_object(self):
        object = super(NewsView, self).get_object()
        if object.hidden and not self.request.user.has_perm('news.view_hidden'):
            # TODO soon
            # Сделать нормальную страницу, оповещающую об отсутствии прав
            raise Http404()
        return object
#-------------------------------------------------------------------------------
class NewsUpdate(UpdateView):
    form_class      = NewsForm
    model           = News
    template_name   = 'news/news_update.hdt'
    #---------------------------------------------------------------------------
    def dispatch(self, request, *args, **kwargs):
        # soon
        # FIXME
        # Сделать нормальную страницу, оповещающую об отсутствии прав
        response = super(NewsUpdate, self).dispatch(request, *args, **kwargs)
        news = self.object
        has_perm = request.user.has_perm
        if news.hidden:
            if not (
                has_perm('news.change_hidden') or \
                has_perm('news.change_only_hidden')
            ):
                raise Http404()
        elif has_perm('news.change_only_hidden'):
            raise Http404()
        if news.siteNews and not has_perm('news.change_sitenews'):
            raise Http404()
        if news.schoolNews and not has_perm('news.change_schoolnews'):
            raise Http404()
        return response
    #---------------------------------------------------------------------------
    def form_valid(self, form):
        if 'preview' in self.request.POST:
            return self.render_to_response(self.get_context_data(form = form))
        else:
            self.object = form.save()
            self.object.last_editor = self.request.user
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
    #---------------------------------------------------------------------------
    def get_context_data(self, **kwargs):
        context = super(NewsUpdate, self).get_context_data(**kwargs)
        fields_to_exclude = []
        request = self.request
        if not request.user.has_perm('news.change_sitenews'):
            fields_to_exclude.append('siteNews')
        if not request.user.has_perm('news.change_schoolnews'):
            fields_to_exclude.append('schoolNews')
        if not request.user.has_perm('news.change_hidden'):
            fields_to_exclude.append('hidden')
        if request.user.has_perm('news.change_only_hidden'):
            fields_to_exclude.extend(['schoolNews', 'siteNews', 'hidden'])
        context['form'].exclude_fields(fields_to_exclude)
        return context
#-------------------------------------------------------------------------------
