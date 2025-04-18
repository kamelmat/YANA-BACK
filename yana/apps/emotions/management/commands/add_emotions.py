from django.core.management.base import BaseCommand
from apps.emotions.models import Emotion

class Command(BaseCommand):
    help = 'Adds 5 specific emotions to the database'

    def handle(self, *args, **options):
        emotions_to_add = [
            'Sadness',
            'Loneliness',
            'Distress',
            'Reluctance',
            'Tranquility'
        ]
        
        for emotion_name in emotions_to_add:
            # Check if emotion already exists
            if not Emotion.objects.filter(name=emotion_name).exists():
                emotion = Emotion.objects.create(name=emotion_name)
                self.stdout.write(self.style.SUCCESS(f'Created emotion: {emotion_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Emotion already exists: {emotion_name}'))
                
        self.stdout.write(self.style.SUCCESS('Finished adding emotions')) 