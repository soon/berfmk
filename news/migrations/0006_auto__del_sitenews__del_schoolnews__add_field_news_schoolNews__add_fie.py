# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SiteNews'
        db.delete_table('news_sitenews')

        # Deleting model 'SchoolNews'
        db.delete_table('news_schoolnews')

        # Adding field 'News.schoolNews'
        db.add_column('news_news', 'schoolNews',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'News.siteNews'
        db.add_column('news_news', 'siteNews',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Renaming column for 'News.author' to match new field type.
        db.rename_column('news_news', 'author', 'author_id')
        # Changing field 'News.author'
        db.alter_column('news_news', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))
        # Adding index on 'News', fields ['author']
        db.create_index('news_news', ['author_id'])


    def backwards(self, orm):
        # Removing index on 'News', fields ['author']
        db.delete_index('news_news', ['author_id'])

        # Adding model 'SiteNews'
        db.create_table('news_sitenews', (
            ('news_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['news.News'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('news', ['SiteNews'])

        # Adding model 'SchoolNews'
        db.create_table('news_schoolnews', (
            ('news_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['news.News'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('news', ['SchoolNews'])

        # Deleting field 'News.schoolNews'
        db.delete_column('news_news', 'schoolNews')

        # Deleting field 'News.siteNews'
        db.delete_column('news_news', 'siteNews')


        # Renaming column for 'News.author' to match new field type.
        db.rename_column('news_news', 'author_id', 'author')
        # Changing field 'News.author'
        db.alter_column('news_news', 'author', self.gf('django.db.models.fields.CharField')(max_length=16))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'news.news': {
            'Meta': {'ordering': "['-create_date']", 'object_name': 'News'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'schoolNews': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'siteNews': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'text_block': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['news']