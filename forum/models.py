# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.db                  import models
from django.contrib.auth.models import User
#-------------------------------------------------------------------------------
#                                   forum
#                                     |
#                                  section ---+
#                                     |       |
#                                sub_section  |
#                                     |       |
#                                   topic ----+
#                                     |
#                                   post
#-------------------------------------------------------------------------------
# Add fields title, address and order and simple __unicode__
class Base_title_address(models.Model):
    title       = models.CharField(max_length = 64)
    address     = models.CharField(max_length = 32)
    order       = models.PositiveIntegerField(default = 0)
    #---------------------------------------------------------------------------
    class Meta:
        abstract = True
        ordering = ['order']
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return self.title
#-------------------------------------------------------------------------------
class Forum(Base_title_address):
    def get_absolute_url(self):
        return '/forum/' + self.address + '/'
#-------------------------------------------------------------------------------
class Section(Base_title_address):
    forum       = models.ForeignKey(Forum)
    #---------------------------------------------------------------------------
    def get_absolute_url(self):
        return self.forum.get_absolute_url() + self.address + '/'
    #---------------------------------------------------------------------------
    def get_last_post(self):
        topics = self.topic_set.all()
        if not topics:
            return None
        else:
            topic = max(
                topics,
                key = lambda t: t.get_last_post().created,
            )
            return topic.get_last_post()
#-------------------------------------------------------------------------------
class Sub_section(Base_title_address):
    section     = models.ForeignKey(Section)
    #---------------------------------------------------------------------------
    def get_absolute_url(self):
        return self.section.forum.get_absolute_url() + self.address + '/'
    #---------------------------------------------------------------------------
    def get_last_post(self):
        topics = self.topic_set.all()
        if not topics:
            return None
        else:
            topic = max(
                topics,
                key = lambda t: t.get_last_post().created,
            )
            return topic.get_last_post()
#-------------------------------------------------------------------------------
class Topic(models.Model):
    title       = models.CharField(max_length = 64)
    created     = models.DateTimeField(auto_now_add = True)
    creator     = models.ForeignKey(User)
    section     = models.ForeignKey(Section)
    sub_section = models.ForeignKey(Sub_section, null = True)
    #---------------------------------------------------------------------------
    closed      = models.BooleanField(default = False)
    visible     = models.BooleanField(default = True)
    locked      = models.BooleanField(default = False)
    #---------------------------------------------------------------------------
    # class Meta:
        # ordering = ['-created']
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return u'%s - %s at %s(%s)' % \
            (self.creator, self.title, self.created, self.sub_section)
    #---------------------------------------------------------------------------
    def get_absolute_url(self):
        if(self.sub_section == None):
            return self.section.get_absolute_url() + str(self.id) + '/'
        else:
            return self.sub_section.get_absolute_url() + str(self.id) + '/'
    #---------------------------------------------------------------------------
    def get_last_post(self):
        return self.post_set.reverse()[0]
#-------------------------------------------------------------------------------
class Post(models.Model):
    created     = models.DateTimeField(auto_now_add = True)
    creator     = models.ForeignKey(User)
    topic       = models.ForeignKey(Topic)
    body        = models.TextField(max_length = 1000)
    number      = models.PositiveIntegerField(default = 0)
    #---------------------------------------------------------------------------
    visible     = models.BooleanField(default = True)
    #---------------------------------------------------------------------------
    class Meta:
        ordering = ['id']
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return u'%s - %s...(%s)' % (self.creator, self.body[:10], self.topic)
    #---------------------------------------------------------------------------
    def get_absolute_url(self):
        p = 1 if self.number == 0 else (self.number) / 10 + 1
        return self.topic.get_absolute_url() + 'page/' + str(p) + '/#post' + \
            str(self.id)
#-------------------------------------------------------------------------------