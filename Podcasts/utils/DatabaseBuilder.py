import csv
from Podcasts.models import *


def build_database():
    with open('Podcasts/podcasts.txt', 'rt', encoding='ISO-8859-1') as csvfile:
        readcsv = csv.reader(csvfile, delimiter='\t')
        for row in readcsv:
            # if not header row, save entry as podcast
            if row[1] != 'name':
                name = row[1]
                author = row[2]
                description = row[3]
                date_published = row[4]
                keywords = row[5].lower().split(",")
                duration = row[6]
                image_filename = row[7]
                upvotes = row[8]
                source = row[11]
                podcast = Podcast.objects.create(name=name, description=description, author=author,
                                                 date_published=date_published, duration=duration,
                                                 image_filename=image_filename, keywords=keywords,
                                                 upvotes=upvotes, source=source)
                podcast.save()
