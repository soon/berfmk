# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Art(models.Model):
    name        = models.CharField(max_length = 15)
    title       = models.CharField(max_length = 100)
    text_block  = models.TextField()
    author      = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['-name']
