from bambu.pages.models import Page

def basics(request):
	return {
		'root_pages': Page.objects.filter(parent__isnull = True)
	}