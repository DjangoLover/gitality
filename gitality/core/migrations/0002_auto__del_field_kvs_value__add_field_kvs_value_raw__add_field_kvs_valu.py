# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'KVS.value'
        db.delete_column(u'core_kvs', 'value')

        # Adding field 'KVS.value_raw'
        db.add_column(u'core_kvs', 'value_raw',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'KVS.value_type'
        db.add_column(u'core_kvs', 'value_type',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'KVS.value'
        db.add_column(u'core_kvs', 'value',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'KVS.value_raw'
        db.delete_column(u'core_kvs', 'value_raw')

        # Deleting field 'KVS.value_type'
        db.delete_column(u'core_kvs', 'value_type')


    models = {
        u'core.kvs': {
            'Meta': {'object_name': 'KVS'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'value_raw': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'value_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']