# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table('stream_company', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
        ))
        db.send_create_signal('stream', ['Company'])

        # Adding model 'Customer'
        db.create_table('stream_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('stream', ['Customer'])

        # Adding model 'Payment'
        db.create_table('stream_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payments_received', to=orm['stream.Customer'])),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payments_made', to=orm['stream.Customer'])),
            ('item', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('remote_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('stream', ['Payment'])


    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table('stream_company')

        # Deleting model 'Customer'
        db.delete_table('stream_customer')

        # Deleting model 'Payment'
        db.delete_table('stream_payment')


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
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments_made'", 'to': "orm['stream.Customer']"}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payments_received'", 'to': "orm['stream.Customer']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['stream']