from django.core.management import BaseCommand

from tasks.models import TodoItem

class Command(BaseCommand):
    help = 'Read tasks from file (one line = one task)and save them to db'

    def add_arguments(self, parser):
        parser.add_argument('--file', dest='filename', type=str)
    
    def handle(self, *args, **options):
        with open(options['filename']) as file:
            for line in file:
                t = TodoItem(description=line)
                t.save()
