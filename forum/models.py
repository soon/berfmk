# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Structure
#
#     forum
#       |
#    section ---+
#       |       |
#  sub_section  |
#       |       |
#     topic ----+
#       |
#     post
#


class BaseForumModel(models.Model):
    """
    A base model class with title, address and order fields

    """
    title = models.CharField(max_length=64, verbose_name=u'Заголовок')
    address = models.CharField(max_length=32, verbose_name=u'Адрес')
    order = models.PositiveIntegerField(default=0,
                                        verbose_name=u'Порядковый номер')

    class Meta:
        abstract = True
        ordering = ['order']

    def __unicode__(self):
        return self.title


class Forum(BaseForumModel):
    """
    A model for forum object

    """
    def get_absolute_url(self):
        return '/forum/' + self.address + '/'


class Section(BaseForumModel):
    """
    A model for section object

    """
    forum = models.ForeignKey(Forum)

    def get_absolute_url(self):
        return self.forum.get_absolute_url() + self.address + '/'

    def get_last_post(self):
        """
        Returns last post(by time) in the section or None

        """
        topics = self.topic_set.all()
        if not topics:
            return None
        else:
            topic = max(
                topics,
                key = lambda t: t.get_last_post().created,
            )
            return topic.get_last_post()


class SubSection(BaseForumModel):
    """
    A model for sub-section object

    """
    section = models.ForeignKey(Section)

    def get_absolute_url(self):
        return self.section.get_absolute_url() + self.address + '/'

    def get_last_post(self):
        """
        Returns last post(by time) in the sub-section or None

        """
        topics = self.topic_set.all()
        if not topics:
            return None
        else:
            topic = max(
                topics,
                key = lambda t: t.get_last_post().created,
            )
            return topic.get_last_post()


class Topic(models.Model):
    """
    A model for topic object

    """
    title = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    section = models.ForeignKey(Section)
    sub_section = models.ForeignKey(SubSection, null=True)

    closed = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    locked = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s - %s at %s(%s)' % \
            (self.creator, self.title, self.created, self.sub_section)

    def get_absolute_url(self):
        if(self.sub_section == None):
            return self.section.get_absolute_url() + str(self.id) + '/'
        else:
            return self.sub_section.get_absolute_url() + str(self.id) + '/'

    def get_last_post(self):
        return self.post_set.latest()


class Post(models.Model):
    """
    A model for post object

    """
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)
    body = models.TextField(max_length=1000, verbose_name=u'Текст сообщения')
    # viewers     = models.ManyToManyField(User)
    # number      = models.PositiveIntegerField(default = 0)

    visible = models.BooleanField(default = True)

    class Meta:
        ordering = ['id']
        get_latest_by = 'id'

    def __unicode__(self):
        return u'%s - %s...(%s)' % (self.creator, self.body[:10], self.topic)

    def get_absolute_url(self):
        # p = 1 if self.number == 0 else (self.number) / 10 + 1
        # return self.topic.get_absolute_url() + 'page/' + str(p) + '/#post' + \
            # str(self.id)
        # p = 1 if self.is_first_post() \
            # else self.topic.post_set.objects.count()
        # TODO
        # soon(19.09.12)
        raise NotImplementedError()

    def is_first_post(self):
        return self.topic.post_set.objects.all()[0] is self
