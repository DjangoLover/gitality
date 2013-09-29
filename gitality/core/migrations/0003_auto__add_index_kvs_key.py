# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'KVS', fields ['key']
        db.create_index(u'core_kvs', ['key'])


    def backwards(self, orm):
        # Removing index on 'KVS', fields ['key']
        db.delete_index(u'core_kvs', ['key'])


    models = {
        u'core.kvs': {
            'Meta': {'object_name': 'KVS'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'value_raw': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'value_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']