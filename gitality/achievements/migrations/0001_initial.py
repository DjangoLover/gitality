# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Achievement'
        db.create_table(u'achievements_achievement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('entity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('points', self.gf('django.db.models.fields.PositiveIntegerField')(default=10)),
            ('logic_class', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'achievements', ['Achievement'])

        # Adding M2M table for field requirements on 'Achievement'
        m2m_table_name = db.shorten_name(u'achievements_achievement_requirements')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('achievement', models.ForeignKey(orm[u'achievements.achievement'], null=False)),
            ('kvs', models.ForeignKey(orm[u'core.kvs'], null=False))
        ))
        db.create_unique(m2m_table_name, ['achievement_id', 'kvs_id'])

        # Adding model 'CommitAchievement'
        db.create_table(u'achievements_commitachievement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('achievement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievements.Achievement'])),
            ('commit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='achievements', to=orm['commits.Commit'])),
        ))
        db.send_create_signal(u'achievements', ['CommitAchievement'])

        # Adding unique constraint on 'CommitAchievement', fields ['achievement', 'commit']
        db.create_unique(u'achievements_commitachievement', ['achievement_id', 'commit_id'])

        # Adding model 'CommitAuthorAchievement'
        db.create_table(u'achievements_commitauthorachievement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('achievement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievements.Achievement'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='achievements', to=orm['commits.CommitAuthor'])),
        ))
        db.send_create_signal(u'achievements', ['CommitAuthorAchievement'])

        # Adding unique constraint on 'CommitAuthorAchievement', fields ['achievement', 'author']
        db.create_unique(u'achievements_commitauthorachievement', ['achievement_id', 'author_id'])

        # Adding model 'ProjectAchievement'
        db.create_table(u'achievements_projectachievement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('achievement', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['achievements.Achievement'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='achievements', to=orm['projects.Project'])),
        ))
        db.send_create_signal(u'achievements', ['ProjectAchievement'])

        # Adding unique constraint on 'ProjectAchievement', fields ['achievement', 'project']
        db.create_unique(u'achievements_projectachievement', ['achievement_id', 'project_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ProjectAchievement', fields ['achievement', 'project']
        db.delete_unique(u'achievements_projectachievement', ['achievement_id', 'project_id'])

        # Removing unique constraint on 'CommitAuthorAchievement', fields ['achievement', 'author']
        db.delete_unique(u'achievements_commitauthorachievement', ['achievement_id', 'author_id'])

        # Removing unique constraint on 'CommitAchievement', fields ['achievement', 'commit']
        db.delete_unique(u'achievements_commitachievement', ['achievement_id', 'commit_id'])

        # Deleting model 'Achievement'
        db.delete_table(u'achievements_achievement')

        # Removing M2M table for field requirements on 'Achievement'
        db.delete_table(db.shorten_name(u'achievements_achievement_requirements'))

        # Deleting model 'CommitAchievement'
        db.delete_table(u'achievements_commitachievement')

        # Deleting model 'CommitAuthorAchievement'
        db.delete_table(u'achievements_commitauthorachievement')

        # Deleting model 'ProjectAchievement'
        db.delete_table(u'achievements_projectachievement')


    models = {
        u'achievements.achievement': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Achievement'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'entity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'db_index': 'True'}),
            'logic_class': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'points': ('django.db.models.fields.PositiveIntegerField', [], {'default': '10'}),
            'requirements': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.KVS']", 'symmetrical': 'False'})
        },
        u'achievements.commitachievement': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('achievement', 'commit'),)", 'object_name': 'CommitAchievement'},
            'achievement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['achievements.Achievement']"}),
            'commit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'achievements'", 'to': u"orm['commits.Commit']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'achievements.commitauthorachievement': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('achievement', 'author'),)", 'object_name': 'CommitAuthorAchievement'},
            'achievement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['achievements.Achievement']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'achievements'", 'to': u"orm['commits.CommitAuthor']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'achievements.projectachievement': {
            'Meta': {'ordering': "['-created']", 'unique_together': "(('achievement', 'project'),)", 'object_name': 'ProjectAchievement'},
            'achievement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['achievements.Achievement']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'achievements'", 'to': u"orm['projects.Project']"})
        },
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'commits.commit': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Commit'},
            'additions': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commits'", 'to': u"orm['commits.CommitAuthor']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deletions': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'etag': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'html_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commits'", 'to': u"orm['projects.Project']"}),
            'sha': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'commits.commitauthor': {
            'Meta': {'ordering': "['-created']", 'object_name': 'CommitAuthor'},
            'author_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'avatar_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'followers': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'following': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'gravatar_id': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.kvs': {
            'Meta': {'object_name': 'KVS'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'value_raw': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'value_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        u'projects.project': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'repo_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '256'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['achievements']