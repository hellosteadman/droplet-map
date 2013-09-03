# coding: UTF-8

from django.db.models import Manager
from django.utils.http import urlencode
from django.utils import simplejson
from django.utils.timezone import utc
from django.conf import settings
from oauth2 import Consumer, Token, Client
from urllib import urlopen
from dateutil.parser import parse
from datetime import timedelta
import re

SEARCH_URL = 'https://api.twitter.com/1.1/search/tweets.json'
USER_URL = 'https://api.twitter.com/1.1/users/show.json'
GEOCODE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
REGEX = re.compile(ur'^I just paid ([^£]+) £(\d+(?:\.\d+)?) via @dropletpay(?: for a (?:#tworder of )?(.+))?(?: - (.+))?$',
	re.IGNORECASE
)

class CompanyManager(Manager):
	def fetch(self, username):
		from droplet.stream.models import Location
		
		try:
			return self.get(username = username)
		except self.model.DoesNotExist:
			pass
		
		client = Client(
			Consumer(
				key = settings.TWITTER_CONSUMER_KEY,
				secret = settings.TWITTER_CONSUMER_SECRET
			),
			Token(
				key = settings.TWITTER_ACCESS_KEY,
				secret = settings.TWITTER_ACCESS_SECRET
			)
		)
		
		response, content = client.request(
			USER_URL + '?' + urlencode(
				{
					'screen_name': username
				}
			)
		)
		
		if response.status != 200:
			return
		
		try:
			content = simplejson.loads(content)
		except:
			return
		
		url = content.get('url')
		if url:
			try:
				url = urlopen(url).url
			except:
				pass
		
		return self.create(
			username = content.get('screen_name'),
			display_name = content.get('name'),
			description = content.get('description'),
			image = content.get('profile_image_url'),
			location = Location.objects.fetch(
				content.get('location')
			),
			url = url
		)

class PaymentManager(Manager):
	def fetch(self):
		from droplet.stream.models import Company, Customer
		
		client = Client(
			Consumer(
				key = settings.TWITTER_CONSUMER_KEY,
				secret = settings.TWITTER_CONSUMER_SECRET
			),
			Token(
				key = settings.TWITTER_ACCESS_KEY,
				secret = settings.TWITTER_ACCESS_SECRET
			)
		)
		
		params = {
			'q': 'via @dropletpay',
			'result_type': 'recent',
			'count': 100
		}
		
		try:
			params['since_id'] = self.latest().remote_id
		except self.model.DoesNotExist:
			pass
		
		qs = urlencode(params)
		response, content = client.request(SEARCH_URL + '?' + qs)
		
		while True:
			if response.status != 200:
				break
			
			try:
				content = simplejson.loads(content)
			except:
				break
			
			for tweet in content.get('statuses', []):
				message = tweet.get('text')
				if not message:
					continue
				
				user = tweet.get('user')
				if not user:
					continue
				
				match = REGEX.search(message)
				if match is None:
					continue
				
				username, amount, item, notes = match.groups()
				if not username:
					continue
				
				try:
					amount = float(amount)
				except:
					continue
				
				company = None
				if username.startswith('@'):
					for mention in tweet.get('entities', {}).get('user_mentions', []):
						if mention.get('screen_name') == username[1:]:
							company = Company.objects.fetch(
								username[1:]
							)
							
							if company is None:
								continue
							
							break
					
					if company is None:
						company = Company.objects.fetch(
							username[1:]
						)
						
						if company is None:
							continue
				else:
					company, created = Company.objects.get_or_create(
						display_name = username
					)
				
				try:
					customer = Customer.objects.get(
						username = user.get('screen_name')
					)
				except Customer.DoesNotExist:
					customer = Customer.objects.create(
						username = user.get('screen_name'),
						display_name = user.get('name')
					)
				
				offset = user.get('utc_offset')
				if offset is None:
					offset = 0
				
				payment = self.create(
					company = company,
					customer = customer,
					item = item,
					amount = str(amount),
					remote_id = tweet.get('id'),
					date = (
						parse(
							tweet.get('created_at')
						) + timedelta(seconds = offset)
					).replace(
						tzinfo = utc
					)
				)
			
			qs = content.get('search_metadata', {}).get('next_results')
			if not qs:
				break
			
			response, content = client.request(SEARCH_URL + '?' + qs)

class LocationManager(Manager):
	def fetch(self, name):
		if not name:
			return
		
		try:
			return self.get(name__iexact = name)
		except self.model.DoesNotExist:
			pass
		
		params = {
			'address': name,
			'sensor': 'false'
		}
		
		url = GEOCODE_URL + '?' + urlencode(params)
		request = urlopen(url)
		response = simplejson.loads(request.read())
		results = response.get('results', [])
		
		if any(results):
			coords = results[0]['geometry']['location']
			
			if len(coords) >= 2:
				latitude, longitude = coords['lat'], coords['lng']
				return self.create(
					name = name,
					latitude = latitude,
					longitude = longitude
				)