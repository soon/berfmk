# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'News'
        db.create_table('news_news', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('text_block', self.gf('django.db.models.fields.TextField')()),
            ('create_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('news', ['News'])

        # Adding model 'SchoolNews'
        db.create_table('news_schoolnews', (
            ('news_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['news.News'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('news', ['SchoolNews'])

        # Adding model 'SiteNews'
        db.create_table('news_sitenews', (
            ('news_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['news.News'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('news', ['SiteNews'])


    def backwards(self, orm):
        # Deleting model 'News'
        db.delete_table('news_news')

        # Deleting model 'SchoolNews'
        db.delete_table('news_schoolnews')

        # Deleting model 'SiteNews'
        db.delete_table('news_sitenews')


    models = {
        'news.news': {
            'Meta': {'object_name': 'News'},
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text_block': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        'news.schoolnews': {
            'Meta': {'object_name': 'SchoolNews', '_ormbases': ['news.News']},
            'news_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['news.News']", 'unique': 'True', 'primary_key': 'True'})
        },
        'news.sitenews': {
            'Meta': {'object_name': 'SiteNews', '_ormbases': ['news.News']},
            'news_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['news.News']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['news']