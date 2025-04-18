from django.core.management.base import BaseCommand
from apps.emotions.models import Emotion

class Command(BaseCommand):
  help = 'Adds emotions to the database. Usage: python manage.py add_emotions "Emotion1" "Emotion2" "Emotion3"'

  def add_arguments(self, parser):
    parser.add_argument(
      'emotions',
      nargs='+',  # This allows one or more arguments
      type=str,
      help='List of emotions to add to the database'
    )

  def handle(self, *args, **options):
    emotions_to_add = options['emotions']
        
    for emotion_name in emotions_to_add:
      # Check if emotion already exists
      if not Emotion.objects.filter(name=emotion_name).exists():
        emotion = Emotion.objects.create(name=emotion_name)
        self.stdout.write(self.style.SUCCESS(f'Created emotion: {emotion_name}'))
      else:
        self.stdout.write(self.style.WARNING(f'Emotion already exists: {emotion_name}'))
                
      self.stdout.write(self.style.SUCCESS('Finished adding emotions')) 