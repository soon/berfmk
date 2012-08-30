# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
from django.db                  import models
from django.contrib.auth.models import User 
#-------------------------------------------------------------------------------
class News(models.Model):
    title       = models.CharField(max_length = 100)
    text_block  = models.TextField()
    last_change = models.DateTimeField(auto_now = True)
    author      = models.ForeignKey(User)
    schoolNews  = models.BooleanField(default = False)
    siteNews    = models.BooleanField(default = False)
    #---------------------------------------------------------------------------
    def __unicode__(self):
        return self.title
    #---------------------------------------------------------------------------
    class Meta:
        ordering = ['-last_change']
#-------------------------------------------------------------------------------
