# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(u'stream_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=36)),
        ))
        db.send_create_signal(u'stream', ['Location'])

        # Adding unique constraint on 'Location', fields ['name', 'latitude', 'longitude']
        db.create_unique(u'stream_location', ['name', 'latitude', 'longitude'])

        # Adding field 'Payment.location'
        db.add_column(u'stream_payment', 'location',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='payments', null=True, to=orm['stream.Location']),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'Location', fields ['name', 'latitude', 'longitude']
        db.delete_unique(u'stream_location', ['name', 'latitude', 'longitude'])

        # Deleting model 'Location'
        db.delete_table(u'stream_location')

        # Deleting field 'Payment.location'
        db.delete_column(u'stream_payment', 'location_id')


    models = {
        u'stream.company': {
            'Meta': {'ordering': "('display_name',)", 'object_name': 'Company'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        },
        u'stream.customer': {
            'Meta': {'ordering': "('display_name', 'username')", 'object_name': 'Customer'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'stream.location': {
            'Meta': {'unique_together': "(('name', 'latitude', 'longitude'),)", 'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'stream.payment': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments_received'", 'to': u"orm['stream.Company']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments_made'", 'to': u"orm['stream.Customer']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'payments'", 'null': 'True', 'to': u"orm['stream.Location']"}),
            'remote_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['stream']