from django.db import models
from django import forms

class Podcast(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=1000, default='')
    image_filename = models.CharField(max_length=20, default='')
    author = models.CharField(max_length=30, default='')
    runtime = models.CharField(max_length=30, default='')
    date_published = models.CharField(max_length=30, default='')
    keywords = models.CharField(max_length=200, default='')
