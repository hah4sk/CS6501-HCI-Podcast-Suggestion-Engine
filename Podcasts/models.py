from django.db import models
from django import forms
from django_mysql.models import ListCharField

class Podcast(models.Model):
    name = models.CharField(max_length=100, default='')
    author = models.CharField(max_length=30, default='')
    description = models.CharField(max_length=1000, default='')
    date_published = models.CharField(max_length=30, default='')
    keywords = models.CharField(max_length=200, default='')
    duration = models.CharField(max_length=30, default='')
    image_filename = models.CharField(max_length=20, default='')
    upvotes = models.CharField(max_length=10, default='0')
    source = models.CharField(max_length=500, default='')



