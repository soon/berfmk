# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Thread'
        db.delete_table('forum_thread')

        # Adding model 'Sub_section'
        db.create_table('forum_sub_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Section'])),
        ))
        db.send_create_signal('forum', ['Sub_section'])

        # Deleting field 'Post.thread'
        db.delete_column('forum_post', 'thread_id')

        # Adding field 'Post.topic'
        db.add_column('forum_post', 'topic',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['forum.Topic']),
                      keep_default=False)

        # Deleting field 'Topic.address'
        db.delete_column('forum_topic', 'address')

        # Adding field 'Topic.created'
        db.add_column('forum_topic', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=None, blank=True),
                      keep_default=False)

        # Adding field 'Topic.creator'
        db.add_column('forum_topic', 'creator',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Topic.sub_section'
        db.add_column('forum_topic', 'sub_section',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Sub_section'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Thread'
        db.create_table('forum_thread', (
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Section'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Topic'], null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('forum', ['Thread'])

        # Deleting model 'Sub_section'
        db.delete_table('forum_sub_section')

        # Adding field 'Post.thread'
        db.add_column('forum_post', 'thread',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['forum.Thread']),
                      keep_default=False)

        # Deleting field 'Post.topic'
        db.delete_column('forum_post', 'topic_id')

        # Adding field 'Topic.address'
        db.add_column('forum_topic', 'address',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32),
                      keep_default=False)

        # Deleting field 'Topic.created'
        db.delete_column('forum_topic', 'created')

        # Deleting field 'Topic.creator'
        db.delete_column('forum_topic', 'creator_id')

        # Deleting field 'Topic.sub_section'
        db.delete_column('forum_topic', 'sub_section_id')


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
        'forum.forum': {
            'Meta': {'object_name': 'Forum'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'forum.post': {
            'Meta': {'ordering': "['id']", 'object_name': 'Post'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Topic']"})
        },
        'forum.section': {
            'Meta': {'object_name': 'Section'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'forum.sub_section': {
            'Meta': {'object_name': 'Sub_section'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Section']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'forum.topic': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Topic'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Section']"}),
            'sub_section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Sub_section']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['forum']