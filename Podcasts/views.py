from django.http import HttpResponse
from django.template import loader
from django.db import models
from .models import *
from django.shortcuts import render

def index(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render({}, request))


def search_results(request):
    # podcast = Podcast.objects.create(name='samy the poopnose', description='poopy samy', author='samyukta venkat')
    # podcast.save()
    # podcast.delete()
    # podcast = Podcast.objects.raw("SELECT * FROM Podcasts_podcast WHERE name='samy the poopnose'")

    # get podcast
    podcast = Podcast.objects.get(name='samy the poopnose')

    template = loader.get_template('searchResults.html')
    context = {
        'podcast': podcast
    }
    return render(request, 'searchResults.html', context)
    # return HttpResponse(template.render({}, request))


def confirmation(request):
    template = loader.get_template('confirmation.html')
    return HttpResponse(template.render({}, request))
