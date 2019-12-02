import csv


def save_to_csv(first_name, last_name, all_selected_podcasts):
    filename = first_name + '_' + last_name
    with open('data_files/' + filename + '.csv', 'w', newline='', encoding='ISO-8859-1') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'author', 'description', 'date published',
                         'keywords', 'duration', 'image filename', 'upvotes'])
        for podcast in all_selected_podcasts:
            name = podcast['name']
            author = podcast['author']
            description = podcast['description']
            date_published = podcast['date_published']
            keywords = podcast['keywords']
            duration = podcast['duration']
            image_filename = podcast['image_filename']
            upvotes = podcast['upvotes']
            source = podcast['source']
            writer.writerow([name, author, description, date_published,
                             keywords, duration, image_filename, upvotes, source])
        file.close()
