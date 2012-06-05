# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'News.author'
        db.add_column('news_news', 'author',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'News.author'
        db.delete_column('news_news', 'author')


    models = {
        'news.news': {
            'Meta': {'ordering': "['create_date']", 'object_name': 'News'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
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