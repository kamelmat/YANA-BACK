from django.core.management.base import BaseCommand
from apps.emotions.models import Emotion, SharedEmotion
from django.contrib.auth import get_user_model
import random
from datetime import datetime, timedelta
import math

class Command(BaseCommand):
  help = 'Generates random emotions at random locations near existing emotions. Usage: python manage.py generate_random_emotions [--count N] [--radius R]'

  def add_arguments(self, parser):
    parser.add_argument(
      '--count',
      type=int,
      default=10,
      help='Number of random emotions to generate (default: 10)'
    )
    parser.add_argument(
      '--radius',
      type=float,
      default=5.0,
      help='Radius in kilometers around existing emotions (default: 5.0)'
    )

  def handle(self, *args, **options):
    count = options['count']
    radius_km = options['radius']
    
    # Get all existing emotions and users
    emotions = list(Emotion.objects.all())
    users = list(get_user_model().objects.all())
    existing_shared_emotions = list(SharedEmotion.objects.all())
    
    if not emotions or not users:
      self.stdout.write(self.style.ERROR('No emotions or users found in the database'))
      return
    
    # Function to generate random point within radius of a given point
    def random_point_near(lat, lon, radius_km):
      # Convert radius from kilometers to degrees (approximate)
      radius_deg = radius_km / 111.32
      
      # Generate random angle and distance
      angle = random.uniform(0, 2 * math.pi)
      distance = random.uniform(0, radius_deg)
      
      # Calculate new point
      new_lat = lat + (distance * math.sin(angle))
      new_lon = lon + (distance * math.cos(angle))
      
      # Ensure coordinates are within valid ranges
      new_lat = max(-90, min(90, new_lat))
      new_lon = max(-180, min(180, new_lon))
      
      return new_lat, new_lon
    
    # Generate random emotions
    created_count = 0
    for _ in range(count):
      try:
        # Pick random emotion and user
        emotion = random.choice(emotions)
        user = random.choice(users)
        
        # If there are existing shared emotions, pick one as reference
        if existing_shared_emotions:
          reference = random.choice(existing_shared_emotions)
          lat, lon = random_point_near(
            float(reference.latitude),
            float(reference.longitude),
            radius_km
          )
        else:
          # If no existing emotions, generate random coordinates within valid ranges
          lat = random.uniform(-90, 90)
          lon = random.uniform(-180, 180)
        
        # Generate random timestamp within last 30 days
        days_ago = random.uniform(0, 30)
        created_at = datetime.now() - timedelta(days=days_ago)
        
        # Create shared emotion
        SharedEmotion.objects.create(
          user=user,
          emotion=emotion,
          latitude=lat,
          longitude=lon,
          created_at=created_at,
          is_active=True
        )
        
        created_count += 1
        self.stdout.write(
          self.style.SUCCESS(
            f'Created emotion: {emotion.name} at ({lat:.6f}, {lon:.6f})'
          )
        )
        
      except Exception as e:
        self.stdout.write(
          self.style.ERROR(f'Error creating emotion: {str(e)}')
        )
    
    self.stdout.write(
      self.style.SUCCESS(
        f'Successfully created {created_count} random emotions'
      )
    ) 