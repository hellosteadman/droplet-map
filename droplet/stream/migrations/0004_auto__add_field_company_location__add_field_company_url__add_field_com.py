# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Company.location'
        db.add_column(u'stream_company', 'location',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='payments', null=True, to=orm['stream.Location']),
                      keep_default=False)

        # Adding field 'Company.url'
        db.add_column(u'stream_company', 'url',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Company.image'
        db.add_column(u'stream_company', 'image',
                      self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Company.description'
        db.add_column(u'stream_company', 'description',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Payment.location'
        db.delete_column(u'stream_payment', 'location_id')


    def backwards(self, orm):
        # Deleting field 'Company.location'
        db.delete_column(u'stream_company', 'location_id')

        # Deleting field 'Company.url'
        db.delete_column(u'stream_company', 'url')

        # Deleting field 'Company.image'
        db.delete_column(u'stream_company', 'image')

        # Deleting field 'Company.description'
        db.delete_column(u'stream_company', 'description')

        # Adding field 'Payment.location'
        db.add_column(u'stream_payment', 'location',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='payments', null=True, to=orm['stream.Location'], blank=True),
                      keep_default=False)


    models = {
        u'stream.company': {
            'Meta': {'ordering': "('display_name',)", 'object_name': 'Company'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'payments'", 'null': 'True', 'to': u"orm['stream.Location']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'remote_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['stream']