from django.core.management.base import BaseCommand
from apps.emotions.models import Emotion

class Command(BaseCommand):
    help = 'Deletes the last 5 emotions from the database'

    def handle(self, *args, **options):
        # Get the last 5 emotions ordered by ID
        last_emotions = Emotion.objects.order_by('-id')[:5]
        
        if not last_emotions:
            self.stdout.write(self.style.WARNING('No emotions found to delete'))
            return
            
        # Delete the emotions
        for emotion in last_emotions:
            self.stdout.write(f'Deleting emotion: {emotion.name}')
            emotion.delete()
            
        self.stdout.write(self.style.SUCCESS('Successfully deleted last 5 emotions')) 