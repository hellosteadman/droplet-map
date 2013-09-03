from django.conf.urls import patterns, include, url
from django.contrib import admin
from bambu.bootstrap.views import DirectTemplateView
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^mapping/', include('bambu.mapping.urls')),
	url(r'^embed/$',
		DirectTemplateView.as_view(template_name = 'embed.html'),
		name = 'embedded_map'
	),
	url(r'^', include('bambu.pages.urls')),
	url(r'^$',
		DirectTemplateView.as_view(
			template_name = 'home.html',
			extra_context = {
				'menu_selection': 'home',
				'body_classes': ('home',)
			}
		),
		name = 'home'
	)
)