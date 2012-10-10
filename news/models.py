# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.db                  import models
from django.contrib.auth.models import User
#-------------------------------------------------------------------------------
class News(models.Model):
    title       = models.CharField(max_length = 100)
    text_block  = models.TextField(max_length = 1000)
    created     = models.DateTimeField(auto_now_add = True)
    last_change = models.DateTimeField(auto_now = True, null = True)
    author      = models.ForeignKey(User, related_name = 'author')
    last_editor = models.ForeignKey(
        User,
        related_name = 'last_editor',
        null = True
    )
    schoolNews  = models.BooleanField(default = False)
    siteNews    = models.BooleanField(default = False)
    hidden      = models.BooleanField(default = False)
    #---------------------------------------------------------------------------
    class Meta:
        ordering = ['-last_change']
        #-----------------------------------------------------------------------
        permissions = (
            (      'add_sitenews',  'Can add sitenews'              ),
            (    'add_schoolnews',  'Can add schoolnews'            ),
            (   'change_sitenews',  'Can change sitenews'           ),
            ( 'change_schoolnews',  'Can change schoolnews'         ),
            (   'delete_sitenews',  'Can delete sitenews'           ),
            ( 'delete_schoolnews',  'Can delete schoolnews'         ),
            (   'add_only_hidden',  'Can add only hidden news'      ),
            ('change_only_hidden',  'Can change only hidden news'   ),
            ('delete_only_hidden',  'Can delete only hidden news'   ),
            (        'add_hidden',  'Can add hidden news'           ),
            (     'change_hidden',  'Can change hidden news'        ),
            (     'delete_hidden',  'Can delete hidden news'        ),
            (       'view_hidden',  'Can view hidden news'          ),
        )
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return self.title
    #---------------------------------------------------------------------------
    def get_absolute_url(self):
        return u'/news/%i/' % self.id
#-------------------------------------------------------------------------------
