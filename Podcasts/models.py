from django.db import models
from django import forms

class Podcast(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    image = models.ImageField()
    author = models.CharField(max_length=30)
    duration = models.CharField(max_length=30)
    publication_date = models.CharField(max_length=30)
