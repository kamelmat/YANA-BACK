from django.core.management.base import BaseCommand
from apps.emotions.models import Emotion

class Command(BaseCommand):
    help = 'Deletes the last N emotions from the database. Usage: python manage.py delete_last_emotions [--count N]'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of emotions to delete (default: 5)'
        )

    def handle(self, *args, **options):
        count = options['count']
        # Get the last N emotions ordered by ID
        last_emotions = Emotion.objects.order_by('-id')[:count]
        
        if not last_emotions:
            self.stdout.write(self.style.WARNING('No emotions found to delete'))
            return
            
        # Delete the emotions
        for emotion in last_emotions:
            self.stdout.write(f'Deleting emotion: {emotion.name}')
            emotion.delete()
            
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted last {count} emotions')) 