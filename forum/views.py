# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.shortcuts               import redirect, get_object_or_404
from django.views.generic.simple    import direct_to_template
from django.conf                    import settings
from django.http                    import Http404
from django.db.models               import Q
from django.core.exceptions         import ObjectDoesNotExist
#-------------------------------------------------------------------------------
from forum.models                   import Forum, Section, Sub_section, Topic
from forum.models                   import Post
from forum.utils                    import create_and_get_topic
from forum.utils                    import create_and_get_post
from berfmk.utils                   import get_number_from_param_or_404
#-------------------------------------------------------------------------------
#               defs
# forums........................return all forums
# sections......................return all sections in forum
# topics.+---.(got Section).---.return all sub_sections and topics in section
#        |
#        +-.(got Sub_section).-.return all topics in sub_section
# posts.........................return all posts in topic
#-------------------------------------------------------------------------------
#               templates
# forum_main....................show all forums
# forum.........................show all sections in forum
# section.......................show all sub-sections and topics in section
# sub_section...................show all topics in sub_section
# topic.........................show all posts in topic
#-------------------------------------------------------------------------------
def forums(request):
    return direct_to_template(
        request,
        'forum/forum_main.hdt', {
            'forums': Forum.objects.all()
        }
    )
#-------------------------------------------------------------------------------
def sections(request, forum):
    f = get_object_or_404(Forum, address = forum)
    return direct_to_template(
        request,
        'forum/forum.hdt', {
            'sections'  : f.section_set.all(),
            'forum'     : f
        }
    )
#-------------------------------------------------------------------------------
def topics(request, forum, section):
    f = get_object_or_404(Forum, address = forum)
    try:
        s = f.section_set.get(address = section)
        topics = sorted(
            s.topic_set.filter(sub_section = None),
            key = lambda t: t.get_last_post().created,
            reverse = True
        )
        return direct_to_template(
            request,
            'forum/section.hdt', {
                'topics'        : topics,
                'sub_sections'  : s.sub_section_set.all(),
                'section'       : s,
                'forum'         : f
            }
        )
    except ObjectDoesNotExist:
        ss = get_object_or_404(Sub_section, address = section)
        topics = sorted(
            ss.topic_set.exclude(sub_section = None),
            key = lambda t: t.get_last_post().created,
            reverse = True
        )
        return direct_to_template(
            request,
            'forum/sub_section.hdt', {
                'topics'        : topics,
                'sub_section'   : ss,
                'forum'         : f
            }
        )
#-------------------------------------------------------------------------------
def posts(request, forum, section, topic, page):
    topic = get_number_from_param_or_404(topic)
    page = get_number_from_param_or_404(page)

    f = get_object_or_404(Forum, address = forum)
    try:
        s = f.section_set.get(address = section)
        t = get_object_or_404(
            s.topic_set.filter(sub_section = None),
            id = topic
        )
        p = t.post_set.all()

        if p.count() <= (page - 1) * 10 and p.count():
            raise Http404()

        return direct_to_template(
            request,
            'forum/topic.hdt', {
                'posts'         : p[:10] if page == 1 else \
                                    list(p[:1]) + \
                                    list(p[(page - 1) * 10:page * 10]),
                'topic'         : t,
                'section'       : s,
                'forum'         : f,
                'page'          : page
            }
        )
    except ObjectDoesNotExist:
        ss = get_object_or_404(Sub_section, address = section)
        t = get_object_or_404(ss.topic_set.all(), id = topic)
        p = t.post_set.all()

        if p.count() <= (page - 1) * 10 and p.count():
            raise Http404()

        return direct_to_template(
            request,
            'forum/topic.hdt', {
                'posts'         : p[:10] if page == 1 else \
                                    list(p[:1]) + \
                                    list(p[(page - 1) * 10:page * 10]),
                'topic'         : t,
                'sub_section'   : ss,
                'section'       : ss.section,
                'forum'         : f,
                'page'          : page
            }
        )
#-------------------------------------------------------------------------------
def add_topic(request, forum, section, preview):
    if not request.user.has_perm('forum.add_topic'):
        raise Http404()

    f = get_object_or_404(Forum, address = forum)
    s, ss = None, None
    try:
        s = f.section_set.get(address = section)
    except ObjectDoesNotExist:
        ss = get_object_or_404(Sub_section, address = section)
        s = ss.section

    if request.method == 'POST':
        errors = {'title': False, 'body': False}
        
        title = request.POST['input_title']
        if len(title) > 64:
            errors['title'] = True

        body = request.POST['input_body']
        if len(body) > 1000:
            errors['body'] = True

        if not True in errors.values():
            if not preview:
                try:
                    t = create_and_get_topic(
                        title   = title,
                        creator = request.user,
                        section = s if ss is None else ss,
                        body    = body
                    )
                except ValueError:
                    # soon(30.08.12, 12:42)
                    # FIXME
                    # Обработать нормально эту ситуацию
                    raise Http404() 
                return redirect(t.get_absolute_url())
            else:
                t = Topic(
                    title       = title,
                    creator     = request.user,
                    section     = s,
                    sub_section = ss,
                )
                p = Post(
                    creator = t.creator,
                    topic = t,
                    body = body
                )
                return direct_to_template(
                    request,
                    'forum/add_topic.hdt', {
                        'topic'     : t,
                        'post'      : p,
                        'forum'     : f,
                        'section'   : s
                    }
                )
        return direct_to_template(
            request,
            'forum/add_topic.hdt', { 
                'topic_title'   : title,
                'post_body'     : text_block,
                'errors'        : errors
            }
        )
    else:
        return direct_to_template(
            request,
            'forum/add_topic.hdt', {
                'forum'     : f,
                'section'   : s if ss is None else ss
            }
        )
#-------------------------------------------------------------------------------
def add_post(request, forum, section, topic, preview):
    if not request.user.has_perm('forum.add_post'):
        raise Http404()

    topic = get_number_from_param_or_404(topic)

    f = get_object_or_404(Forum, address = forum)
    s, ss = None, None
    try:
        s = f.section_set.get(address = section)
    except ObjectDoesNotExist:
        ss = get_object_or_404(Sub_section, address = section)
        s = ss.section

    t = get_object_or_404(s.topic_set.all(), id = topic)

    if request.method == 'POST':
        errors = {'body': False}

        body = request.POST['input_body']
        if len(body) > 1000:
            errors['body'] = True

        if not True in errors.values():
            if not preview:
                try:
                    p = create_and_get_post(
                        creator = request.user,
                        topic   = t,
                        body    = body
                    )
                except ValueError:
                    # soon(30.08.12, 12:42)
                    # FIXME
                    # Обработать нормально эту ситуацию
                    raise Http404() 
                return redirect(p.get_absolute_url())
            else:
                p = Post(
                    creator = request.user,
                    topic   = t,
                    body    = body
                )
                return direct_to_template(
                    request,
                    'forum/add_post.hdt', {
                        'post'      : p,
                        'topic'     : t,
                        'forum'     : f,
                        'section'   : s
                    }
                )
        return direct_to_template(
            request,
            'forum/add_post.hdt', { 
                'post_body'     : text_block,
                'errors'        : errors
            }
        )
    else:
        raise Http404()
#-------------------------------------------------------------------------------