from django.contrib import admin
from droplet.stream.models import *

admin.site.register(Customer)
admin.site.register(Company)

class PaymentAdmin(admin.ModelAdmin):
	list_display = ('customer', 'company', 'amount', 'item')
	list_filter = ('customer', 'company')
	date_hierarchy = 'date'
	readonly_fields = ('remote_id',)

admin.site.register(Payment, PaymentAdmin)