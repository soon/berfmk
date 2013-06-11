# -*- coding: utf-8 -*-

import warnings

warnings.warn("This module is deprecated since 11.06.13")

from forum.models import Forum, Section, SubSection, Topic, Post

def create_and_get_forum(title, address, order=0):
    f, created = Forum.objects.get_or_create(title=title, address=address)
    if(not created):
        raise ValueError('Forum with that address and title already exists')
    f.order = order
    f.save()
    return f

def create_and_get_section(title, address, forum, order=0):
    if(not Forum.objects.get(id=forum.id) == forum):
        raise ValueError('Invalid forum')
    s, created = Section.objects.get_or_create(
        title   = title,
        address = address,
        forum   = forum
    )
    if(not created):
        raise ValueError('Section with that address and title already exists')
    s.order = order
    s.save()
    return s

def create_and_get_sub_section(title, address, section, order=0):
    if(not Section.objects.get(id=section.id) == section):
        raise ValueError('Invalid section')
    ss, created = SubSection.objects.get_or_create(
        title   = title,
        address = address,
        section = section
    )
    if(not created):
        raise ValueError(
            'SubSection with that address and title already exists'
        )
    ss.order = order
    ss.save()
    return ss

def create_and_get_topic(title, creator, section, body):
    sub_section = None

    if(type(section) == SubSection):
        if(SubSection.objects.get(id=section.id) == section):
            sub_section = section
            section = sub_section.section
    elif(type(section) == Section):
        if(not Section.objects.filter(id=section.id)[0] == section):
            raise ValueError('Invalid section or sub_section')
    else:
        ValueError('type(section) != SubSection or Section. Get The Fuck Out')

    t, created = Topic.objects.get_or_create(
        title       = title,
        creator     = creator,
        section     = section,
        sub_section = sub_section
    )
    if(not created):
        raise ValueError('Topic with that address and title already exists')

    Post.objects.create(creator=creator, topic=t, body=body)

    return t

def create_and_get_post(topic, creator, body):
    if(not Topic.objects.get(id=topic.id) == topic):
        raise ValueError('Invalid topic')

    p, created = Post.objects.get_or_create(
        topic = topic,
        creator = creator,
        body = body
    )
    if(not created):
        raise ValueError('This post already exists')

    p.save()
    return p
