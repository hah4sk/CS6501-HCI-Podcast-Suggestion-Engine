from django.http import HttpResponse
from django.template import loader
from django.db import models
from .models import *
from .utils.DatabaseBuilder import *
from .utils.save_to_csv import *
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db.models import Q
from functools import reduce


def signup(request):

    request.session['all_selected_podcasts'] = []
    request.session['first_name'] = ''
    request.session['last_name'] = ''

    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))


def select_genre(request):
    # from django import db
    # db.connections.close_all()
    # build_database()
    if request.method == "POST":
        request.session['first_name'] = str(request.POST['first_name'])
        request.session['last_name'] = str(request.POST['last_name'])

    template = loader.get_template('selectGenre.html')
    return HttpResponse(template.render({}, request))


def search_results(request):
    # podcast = Podcast.objects.create(name='samy the poopnose', description='poopy samy', author='samyukta venkat')
    # podcast.save()
    # podcast.delete()
    # podcast = Podcast.objects.raw("SELECT * FROM Podcasts_podcast WHERE name='samy the poopnose'")
    # get podcast
    # podcast = Podcast.objects.get(name='samy the poopnose')
    # podcasts = Podcast.objects.filter(name='yeet yeet')

    if request.method == "POST":
        keywords = str(request.POST['genre']).split("/")
        podcasts = Podcast.objects.filter(reduce(lambda x, y: x | y, [Q(keywords__icontains=keyword) for keyword in keywords]))
        request.session['podcast_search_results'] = []
        podcast_search_podcasts = request.session['podcast_search_results']
        for podcast in podcasts:
            podcast_search_podcasts.append(model_to_dict(podcast))
        request.session['podcast_search_results'] = podcast_search_podcasts
    else:
        keywords = []
        request.session['searched_podcasts'] = []
        podcasts = Podcast.objects.filter()


    template = loader.get_template('searchResults.html')
    context = {
        'podcasts': podcasts,
        'keywords': keywords
    }
    return render(request, 'searchResults.html', context)
    # return HttpResponse(template.render({}, request))


def confirmation(request):
    if request.method == "GET":
            keywords = request.GET['keywords']
            print('keywords are: ' + keywords)

            all_selected_podcasts = request.session.get('all_selected_podcasts')
            if not all_selected_podcasts:
                request.session['all_selected_podcasts'] = []
                all_selected_podcasts = request.session['all_selected_podcasts']

            podcast_search_results = request.session['podcast_search_results']
            print('length of search results: ' + str(len(podcast_search_results)))
            for i in range(len(podcast_search_results)):
                if str(i) in request.GET:
                    print('appending: ' + podcast_search_results[i]['name'])
                    print('-----------------')
                    all_selected_podcasts.append(podcast_search_results[i])

            request.session['all_selected_podcasts'] = all_selected_podcasts

    template = loader.get_template('confirmation.html')
    return HttpResponse(template.render({}, request))


def complete_activity(request):
    # save data to csv
    first_name = request.session['first_name']
    last_name = request.session['last_name']
    all_selected_podcasts = request.session['all_selected_podcasts']
    save_to_csv(first_name, last_name, all_selected_podcasts)

    template = loader.get_template('completeActivity.html')
    return HttpResponse(template.render({}, request))
