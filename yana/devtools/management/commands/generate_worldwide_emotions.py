"""
Command to generate random emotions for testing users with random coordinates worldwide.

Usage:
  python manage.py generate_worldwide_emotions

This command will:
1. Find all users with email containing 'testing_frontend'
2. Generate a random emotion for each user
3. Assign random coordinates anywhere in the world
4. Set random timestamps within the last 30 days
"""

from django.core.management.base import BaseCommand
from apps.emotions.models import Emotion, SharedEmotion
from django.contrib.auth import get_user_model
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generates random emotions for testing users with worldwide coordinates'

    def handle(self, *args, **options):
        # Get all existing emotions and testing users
        emotions = list(Emotion.objects.all())
        User = get_user_model()
        testing_users = list(User.objects.filter(email__contains='testing_frontend'))
        
        if not testing_users:
            self.stdout.write(self.style.ERROR('No testing users found in the database'))
            return

        if not emotions:
            self.stdout.write(self.style.ERROR('No emotions found in the database'))
            return

        # Generate random emotions for each user
        created_count = 0
        for user in testing_users:
            try:
                emotion = random.choice(emotions)

                # Generate random coordinates and format them as strings with 4 decimal places
                lat = "{:.4f}".format(random.uniform(-90, 90))
                lon = "{:.4f}".format(random.uniform(-180, 180))

                days_ago = random.uniform(0, 30)
                created_at = datetime.now() - timedelta(days=days_ago)

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
                        f'Created emotion: {emotion.name} for user {user.email} at ({lat}, {lon})'
                    )
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating emotion for user {user.email}: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} random emotions for testing users worldwide'
            )
        ) 