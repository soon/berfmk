# -*- coding: utf-8 -*-

from django.forms import Textarea

from berfmk.forms import MyModelForm
from forum.models import Forum, Post


class ForumForm(MyModelForm):
    class Meta(object):
        model = Forum


class PostForm(MyModelForm):
    class Meta(object):
        model = Post
        fields = ('body', )
        widgets = {
            'body': Textarea(
                attrs = {
                    'required'  : '',
                    'rows'      : 8,
                    'id'        : 'wmd-input',
                }
            )
        }

