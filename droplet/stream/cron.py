from bambu import cron
from droplet.stream.models import Payment

class PaymentJob(cron.CronJob):
	frequency = cron.MINUTE
	
	def run(self, logger):
		Payment.objects.fetch()

cron.site.register(PaymentJob)