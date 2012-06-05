# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'News.title'
        db.alter_column('news_news', 'title', self.gf('django.db.models.fields.CharField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'News.title'
        db.alter_column('news_news', 'title', self.gf('django.db.models.fields.CharField')(max_length=45))

    models = {
        'news.news': {
            'Meta': {'ordering': "['create_date']", 'object_name': 'News'},
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text_block': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'news.schoolnews': {
            'Meta': {'ordering': "['create_date']", 'object_name': 'SchoolNews', '_ormbases': ['news.News']},
            'news_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['news.News']", 'unique': 'True', 'primary_key': 'True'})
        },
        'news.sitenews': {
            'Meta': {'ordering': "['create_date']", 'object_name': 'SiteNews', '_ormbases': ['news.News']},
            'news_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['news.News']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['news']