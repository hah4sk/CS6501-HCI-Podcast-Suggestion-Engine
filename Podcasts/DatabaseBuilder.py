import csv
from .models import *


def build_database():
    with open('Podcasts/podcasts.txt') as csvfile:
        readcsv = csv.reader(csvfile, delimiter='\t')
        for row in readcsv:
            # if not header row
            if row[0] != 'name':
                name = row[0]
                author = row[1]
                description = row[2]
                date_published = row[3]
                keywords = row[4]
                duration = row[5]
                image_filename = row[6]
                upvotes = row[7]

                podcast = Podcast.objects.create(name=name, description=description, author=author,
                                                 date_published=date_published, runtime=duration,
                                                 image_filename=image_filename, keywords=keywords)
                podcast.save()

