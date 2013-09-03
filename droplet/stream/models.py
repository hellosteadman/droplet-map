from django.db import models
from django.db.models import Sum
from django.template.loader import render_to_string
from droplet.stream.managers import CompanyManager, PaymentManager, LocationManager

class Location(models.Model):
	name = models.CharField(max_length = 100)
	latitude = models.CharField(max_length = 36)
	longitude = models.CharField(max_length = 36)
	objects = LocationManager()
	
	def __unicode__(self):
		return self.name
	
	def balloon(self):
		payments = Payment.objects.filter(company__location = self)
		
		return render_to_string('stream/location.inc.html',
			{
				'location': self,
				'payments': payments.count(),
				'total_amount': payments.aggregate(
					total_amount = Sum('amount')
				).get('total_amount', 0)
			}
		)
	
	class Meta:
		ordering = ('name',)
	
	class Meta:
		unique_together = ('name', 'latitude', 'longitude')

class Company(models.Model):
	display_name = models.CharField(max_length = 50, null = True, blank = True)
	username = models.CharField(max_length = 30, db_index = True)
	location = models.ForeignKey(Location, related_name = 'payments', null = True, blank = True)
	url = models.URLField(u'URL', max_length = 255, null = True, blank = True)
	image = models.URLField(max_length = 255, null = True, blank = True)
	description = models.CharField(max_length = 200, null = True, blank = True)
	objects = CompanyManager()
	
	def __unicode__(self):
		return self.display_name
	
	class Meta:
		ordering = ('display_name',)
		verbose_name_plural = 'companies'

class Customer(models.Model):
	username = models.CharField(max_length = 30, unique = True)
	display_name = models.CharField(max_length = 50, null = True, blank = True)
	
	def __unicode__(self):
		return self.display_name or self.username
	
	class Meta:
		ordering = ('display_name', 'username')

class Payment(models.Model):
	customer = models.ForeignKey(Customer, related_name = 'payments')
	company = models.ForeignKey(Company, related_name = 'payments')
	item = models.CharField(max_length = 100, null = True, blank = True)
	amount = models.DecimalField(decimal_places = 2, max_digits = 5)
	date = models.DateTimeField()
	remote_id = models.CharField(max_length = 30, unique = True, editable =False)
	objects = PaymentManager()
	
	def __unicode__(self):
		return u'%s to %s' % (unicode(self.amount), unicode(self.company))
	
	class Meta:
		ordering = ('-date',)
		get_latest_by = 'date'