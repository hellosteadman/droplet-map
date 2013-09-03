# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Payment.client'
        db.delete_column('stream_payment', 'client_id')

        # Adding field 'Payment.company'
        db.add_column('stream_payment', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='payments_received', to=orm['stream.Company']),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Payment.client'
        raise RuntimeError("Cannot reverse this migration. 'Payment.client' and its values cannot be restored.")
        # Deleting field 'Payment.company'
        db.delete_column('stream_payment', 'company_id')


    models = {
        'stream.company': {
            'Meta': {'ordering': "('display_name',)", 'object_name': 'Company'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        },
        'stream.customer': {
            'Meta': {'ordering': "('display_name', 'username')", 'object_name': 'Customer'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'stream.payment': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments_received'", 'to': "orm['stream.Company']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments_made'", 'to': "orm['stream.Customer']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['stream']