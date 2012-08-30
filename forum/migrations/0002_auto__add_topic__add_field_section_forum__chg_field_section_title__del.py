# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Topic'
        db.create_table('forum_topic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Section'])),
        ))
        db.send_create_signal('forum', ['Topic'])

        # Adding field 'Section.forum'
        db.add_column('forum_section', 'forum',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['forum.Forum']),
                      keep_default=False)


        # Changing field 'Section.title'
        db.alter_column('forum_section', 'title', self.gf('django.db.models.fields.CharField')(max_length=64))
        # Deleting field 'Forum.section'
        db.delete_column('forum_forum', 'section_id')


        # Changing field 'Forum.title'
        db.alter_column('forum_forum', 'title', self.gf('django.db.models.fields.CharField')(max_length=64))
        # Deleting field 'Thread.forum'
        db.delete_column('forum_thread', 'forum_id')

        # Adding field 'Thread.topic'
        db.add_column('forum_thread', 'topic',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['forum.Topic']),
                      keep_default=False)


        # Changing field 'Thread.title'
        db.alter_column('forum_thread', 'title', self.gf('django.db.models.fields.CharField')(max_length=64))

    def backwards(self, orm):
        # Deleting model 'Topic'
        db.delete_table('forum_topic')

        # Deleting field 'Section.forum'
        db.delete_column('forum_section', 'forum_id')


        # Changing field 'Section.title'
        db.alter_column('forum_section', 'title', self.gf('django.db.models.fields.CharField')(max_length=60))
        # Adding field 'Forum.section'
        db.add_column('forum_forum', 'section',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['forum.Section']),
                      keep_default=False)


        # Changing field 'Forum.title'
        db.alter_column('forum_forum', 'title', self.gf('django.db.models.fields.CharField')(max_length=60))
        # Adding field 'Thread.forum'
        db.add_column('forum_thread', 'forum',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['forum.Forum']),
                      keep_default=False)

        # Deleting field 'Thread.topic'
        db.delete_column('forum_thread', 'topic_id')


        # Changing field 'Thread.title'
        db.alter_column('forum_thread', 'title', self.gf('django.db.models.fields.CharField')(max_length=60))

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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'forum.post': {
            'Meta': {'object_name': 'Post'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Thread']"})
        },
        'forum.section': {
            'Meta': {'object_name': 'Section'},
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'forum.thread': {
            'Meta': {'object_name': 'Thread'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Topic']"})
        },
        'forum.topic': {
            'Meta': {'object_name': 'Topic'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Section']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['forum']