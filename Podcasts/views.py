from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render({}, request))


def search_results(request):
    template = loader.get_template('searchResults.html')
    return HttpResponse(template.render({}, request))


def confirmation(request):
    template = loader.get_template('confirmation.html')
    return HttpResponse(template.render({}, request))
