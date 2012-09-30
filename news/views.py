# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.shortcuts               import redirect
from django.views.generic.simple    import direct_to_template
from django.views.generic           import ListView, CreateView
from django.conf                    import settings
from django.http                    import Http404
from django.core.paginator          import Paginator, EmptyPage
#-------------------------------------------------------------------------------
from news.models                    import News
from news.forms                     import NewsForm
from news.utils                     import get_news_or_404
from news.utils                     import get_number_from_param_or_404
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
def news_page(request, id):
    news = get_news_or_404(id)
    if news.hidden and not request.user.has_perm('news.view_hidden'):
        # soon(02.08.12, 14:17)
        # FIXME
        #  Сделать нормальную страницу, оповещающую об отсутствии прав
        raise Http404()

    return direct_to_template(
        request,
        'news/news_page.hdt', {
            'news': news
        }
    )
#-------------------------------------------------------------------------------
def edit_news(request, id, preview = False):
    # FIXME
    # Если послать поддельный POST, то юзер без прав(на определенный раздел)
    # сможет добавить новость
    # soon(30.08.12, 11:11)
    # См. выше
    user = request.user

    if not (
        user.has_perm('news.add_news')          or \
        user.has_perm('news.add_schoolnews')    or \
        user.has_perm('news.add_sitenews')      or \
        user.has_perm('news.add_hidden')        or \
        user.has_perm('news.add_only_hidden')
    ):
        # soon(02.09.12, 15:32)
        # FIXME
        # Сделать нормальную страницу, оповещающую об отсутствии прав
        raise Http404()

    news = get_news_or_404(id)
    if news.hidden:
        if not (
            user.has_perm('news.add_hidden') or \
            user.has_perm('news.add_only_hidden')
        ):
        # soon(02.09.12, 14:13)
        # FIXME
        # Сделать нормальную страницу, оповещающую об отсутствии прав
            raise Http404()
    # FIXME:
    # Если длинна будет нулевая
    if request.method == 'POST':
        errors = {'title': False, 'text_block': False}
        title = request.POST['input_title']
        if len(title) > 100:
            errors['title'] = True

        text_block = request.POST['input_text_block']
        if len(text_block) > 1000:
            errors['text_block'] = True

        if not True in errors.values():
            schoolNews = 'school' in request.POST.keys()
            if schoolNews and not user.has_perm('news.add_schoolnews'):
                # soon(02.09.12, 14:07)
                # FIXME
                # Сделать нормальную страницу, оповещающую об отсутствии прав
                raise Http404()

            siteNews = 'site' in request.POST.keys()
            if siteNews and not user.has_perm('news.add_sitenews'):
                # soon(02.09.12, 14:07)
                # FIXME
                # Сделать нормальную страницу, оповещающую об отсутствии прав
                raise Http404()

            hidden = 'hidden' in request.POST.keys() or \
                    user.has_perm('news.add_only_hidden')
            if hidden:
                if not (
                    user.has_perm('news.add_hidden') or \
                    user.has_perm('news.add_only_hidden')
                ):
                    # soon(02.09.12, 14:08)
                    # FIXME
                    # Сделать нормальную страницу, оповещающую об отсутствии прав
                    raise Http404()
            news.title, news.text_block, news.schoolNews, news.siteNews = \
            title,      text_block,         schoolNews,     siteNews
            news.hidden = hidden
            if not preview:
                news.last_editor = user
                news.save()
                return redirect('/news/{0}/'.format(id))
        return direct_to_template(
            request,
            'news/edit_news.hdt', {
                'news'              : news,
                'news_title'        : title,
                'news_text_block'   : text_block,
                'errors'            : errors
            }
        )
    else:
        return direct_to_template(
            request,
            'news/edit_news.hdt', {
                'news': news
            }
        )
#-------------------------------------------------------------------------------
