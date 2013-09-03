from django.db.models import Sum
from droplet.stream.models import Company, Location, Payment
from django.conf import settings

def charts(request):
	def companies():
		return Company.objects.annotate(
			total_amount = Sum('payments__amount')
		).order_by(
			'-total_amount'
		)[:10]
	
	return {
		'charts': {
			'companies': companies
		}
	}

def locations(request):
	def tryint(val):
		try:
			return int(val)
		except:
			return None
	
	return {
		'locations': Location.objects.all,
		'map_width': '%spx' % (tryint(request.GET.get('width')) or 1024),
		'map_height': '%spx' % (tryint(request.GET.get('height')) or 576),
		'map_zoom': tryint(request.GET.get('zoom')) or settings.MAPPING_SETTINGS['zoom']
	}