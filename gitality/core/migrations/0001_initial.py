# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'KVS'
        db.create_table(u'core_kvs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'core', ['KVS'])


    def backwards(self, orm):
        # Deleting model 'KVS'
        db.delete_table(u'core_kvs')


    models = {
        u'core.kvs': {
            'Meta': {'object_name': 'KVS'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['core']