# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.shortcuts               import redirect
from django.views.generic.simple    import direct_to_template
from django.conf                    import settings
from django.http                    import Http404
#-------------------------------------------------------------------------------
from news.models                    import News
#-------------------------------------------------------------------------------
def news(request, direction, page):
    try:
        page = int(page)
    except ValueError:
        raise Http404()

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
    news = News.objects.all()
    if siteNews or schoolNews:
        news = news.filter(schoolNews = schoolNews, siteNews = siteNews)
    if len(news) <= (page - 1) * 10 and len(news):
        raise Http404()

    can_add = request.user.has_perm('news.add_{0}news'.format(direction[:-1]))

    return direct_to_template(
            request,
            'news/news.hdt', {
                'direction': part_of_title,
                'page': page,
                'news': news[(page - 1) * 10:page * 10],
                'can_add': can_add
            }
        )
#-------------------------------------------------------------------------------
def add_news(request, preview = False):
    # FIXME
    # Если послать поддельный POST, то юзер без 
    # прав(на определенный раздел) сможет 
    # добавить новость
    if not (
            request.user.has_perm('news.add_news') or \
            request.user.has_perm('news.add_schoolnews') or \
            request.user.has_perm('news.add_sitenews')
        ):
        raise Http404()
    # FIXME:
    # Если длинна будет нулевая
    errors = {'title': False, 'text_block': False}
    if request.method == 'POST':
        title = request.POST['input_title']
        if len(title) > 100:
            errors['title'] = True

        text_block = request.POST['input_text_block']
        if len(text_block) > 1000:
            errors['text_block'] = True

        news_for = request.POST['radiobutton']
        if news_for not in ['all', 'site', 'school']:
            print '/news/add/ : news_for not in ["all", "site", "school"]'
            return direct_to_template(
                    request,
                    'news/add_news.hdt', {
                        'news_title': title,
                        'news_text_block': text_block
                    }
                )
        schoolNews = news_for == 'school'
        siteNews = news_for = 'site'


        news = None

        if not True in errors.values():
            schoolNews, siteNews = False, False
            if news_for == 'site':
                siteNews = True
            elif news_for == 'school':
                schoolNews = True
            news = News(
                    title = title,
                    text_block = text_block,
                    author = request.user,
                    schoolNews = schoolNews,
                    siteNews = siteNews
                )
            if not preview:
                news.save()
                return redirect('/news/{0}'.format(news.id))
        return direct_to_template(
                request,
                'news/add_news.hdt', { 
                    'news_title': title,
                    'news_text_block': text_block,
                    'news': news
                }
            )
    else:
        return direct_to_template(request, 'news/add_news.hdt')
#-------------------------------------------------------------------------------
def news_page(request, id):
    try:
        id = int(id)
        news = News.objects.get(id = id)
        return direct_to_template(
                request,
                'news/news_page.hdt', {
                    'news': news
                }
            )
    except News.DoesNotExist, ValueError:
        raise Http404()
#-------------------------------------------------------------------------------
def edit_news(request, id, preview = False):
    # FIXME
    # Если послать поддельный POST, то юзер без 
    # прав(на определенный раздел) сможет 
    # добавить новость
    if not (
            request.user.has_perm('news.change_news') or \
            request.user.has_perm('news.change_schoolnews') or \
            request.user.has_perm('news.change_sitenews')
        ):
        raise Http404()
    news = None
    try:
        id = int(id)
        news = News.objects.get(id = id)
    except News.DoesNotExist, ValueError:
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

        news_for = request.POST['radiobutton']
        if news_for not in ['all', 'site', 'school']:
            print '/news/edit/ : news_for not in ["all", "site", "school"]'
            return direct_to_template(
                    request,
                    'news/edit_news.hdt', {
                        'news': news,
                        'news_title': title,
                        'news_text_block': text_block
                    }
                )
        schoolNews = news_for == 'school'
        siteNews = news_for = 'site'

        if not True in errors.values():
            if not preview:
                news.title, news.text_block, news.schoolNews, \
                news.siteNews = title, text_block, schoolNews, \
                siteNews
                news.save()
                return redirect('/news/{0}/'.format(id))
        return direct_to_template(
                request,
                'news/edit_news.hdt', {
                    'news': news,
                    'news_title': title,
                    'news_text_block': text_block
                }
            )
    else:
        return direct_to_template(
                request,
                'news/edit_news.hdt', {
                    'news': news
                }
            )
        
