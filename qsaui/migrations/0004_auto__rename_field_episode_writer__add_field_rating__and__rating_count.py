# -*- coding: utf-8 -*-

from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Renaming field 'Episode.writer' to 'Episode.writers'
        db.rename_column(u'qsaui_episode', 'writer', 'writers')

        # Adding field 'Episode.rating'
        db.add_column(u'qsaui_episode', 'rating',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'Episode.rating_count'
        db.add_column(u'qsaui_episode', 'rating_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Series.rating'
        db.add_column(u'qsaui_series', 'rating',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'Series.rating_count'
        db.add_column(u'qsaui_series', 'rating_count',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Renaming field 'Episode.writers' to 'Episode.writer'
        db.rename_column(u'qsaui_episode', 'writers', 'writer')

        # Deleting field 'Episode.rating'
        db.delete_column(u'qsaui_episode', 'rating')

        # Deleting field 'Episode.rating_count'
        db.delete_column(u'qsaui_episode', 'rating_count')

        # Deleting field 'Series.rating'
        db.delete_column(u'qsaui_series', 'rating')

        # Deleting field 'Series.rating_count'
        db.delete_column(u'qsaui_series', 'rating_count')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'qsaui.episode': {
            'Meta': {'unique_together': "((u'series', u'season', u'number'),)", 'object_name': 'Episode'},
            'director': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'first_aired': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'guest_stars': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'imdb_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'overview': ('django.db.models.fields.TextField', [], {}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rating_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'season': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['qsaui.Series']"}),
            'tvdb_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'writers': ('django.db.models.fields.TextField', [], {'null': 'True'})
        },
        u'qsaui.series': {
            'Meta': {'object_name': 'Series'},
            'banner': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'cast': ('django.db.models.fields.TextField', [], {}),
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_aired': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imdb_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'network': ('django.db.models.fields.TextField', [], {}),
            'overview': ('django.db.models.fields.TextField', [], {}),
            'poster': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'rating': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rating_count': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'runtime': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'tags': ('django.db.models.fields.TextField', [], {}),
            'tvdb_id': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'qsaui.watcher': {
            'Meta': {'object_name': 'Watcher'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'series': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['qsaui.Series']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['qsaui']