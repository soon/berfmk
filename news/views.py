# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.shortcuts               import redirect
from django.views.generic.simple    import direct_to_template
from django.conf                    import settings
from django.http                    import Http404
from django.core.paginator          import Paginator, EmptyPage
# from django.core.paginator          import PageNotAnInteger
#-------------------------------------------------------------------------------
from news.models                    import News
from news.utils                     import get_news_or_404
from news.utils                     import get_number_from_param_or_404
#-------------------------------------------------------------------------------
def news(request, direction, page):
    page = get_number_from_param_or_404(page)
    
    schoolNews, siteNews = False, False
    part_of_title = ''
    if direction == 'site/':
        siteNews = True
        part_of_title = ' сайта'
    elif direction == 'school/':
        schoolNews = True
        part_of_title = ' школы'
    elif direction != '':
        raise Http404()
    # NOTE
    # Может быть сделать отдельную страницу для пустых страниц
    # soon(30.08.12, 11:04)
    # Что я хотел себе этим сказать - непонятно
    news = News.objects.all()
    if(schoolNews):
        news = news.filter(schoolNews = schoolNews)
    elif(siteNews):
        news = news.filter(siteNews = siteNews)

    paginator = Paginator(news, 10)
    try:
        news = paginator.page(page)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    # if news.count() <= (page - 1) * 10 and news.count():
        # raise Http404()

    can_add = request.user.has_perm('news.add_{0}news'.format(direction[:-1])) \
        or request.user.has_perm('news.add_hidden') \
        or request.user.has_perm('news.add_only_hidden')

    return direct_to_template(
            request,
            'news/news.hdt', {
                'direction': part_of_title,
                # 'page': page,
                'news': news,
                'can_add': can_add
            }
        )
#-------------------------------------------------------------------------------
def add_news(request, preview = False):
    # FIXME
    # Если послать поддельный POST, то юзер без прав(на определенный раздел) 
    # сможет добавить новость
    # soon(30.08.12, 11:06)
    # Или не сможет.
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

        news = None

        if not True in errors.values():
            schoolNews = 'school' in request.POST.keys()
            if schoolNews and not request.user.has_perm('news.add_schoolnews'):
                # soon(02.09.12, 14:02)
                # FIXME
                # Сделать нормальную страницу, оповещающую об отсутствии прав
                raise Http404()

            siteNews = 'site' in request.POST.keys()
            if siteNews and not request.user.has_perm('news.add_sitenews'):
                # soon(02.09.12, 14:03)
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
                    # soon(02.09.12, 14:04)
                    # FIXME
                    # Сделать нормальную страницу, оповещающую об отсутствии прав
                    raise Http404()

            news = News(
                title       = title,
                text_block  = text_block,
                author      = user,
                schoolNews  = schoolNews,
                siteNews    = siteNews,
                hidden      = hidden
            )
            if not preview:
                news.save()
                return redirect('/news/{0}'.format(news.id))
        return direct_to_template(
            request,
            'news/add_news.hdt', { 
                'news_title'        : title,
                'news_text_block'   : text_block,
                'news'              : news,
                'errors'            : errors
            }
        )
    else:
        return direct_to_template(request, 'news/add_news.hdt')
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
        
