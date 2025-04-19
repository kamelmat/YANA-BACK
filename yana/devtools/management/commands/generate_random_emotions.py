"""
Command to generate random emotions at random locations.

Usage:
  python manage.py generate_random_emotions [--count N] [--email EMAIL] [--radius R]

Options:
    --count N     Number of random emotions to generate (default: 10)
    --email EMAIL Email of the user whose last emotion will be used as reference point
    --radius R    Radius in degrees around the reference point (default: 0.1)

Examples:
    # Generate 10 random emotions near a specific user's last emotion
    python manage.py generate_random_emotions --email testing_frontend_1@example.com

    # Generate 50 random emotions very close to a specific user's last emotion
    python manage.py generate_random_emotions --count 50 --email testing_frontend_1@example.com --radius 0.01

    # Generate 10 random emotions in a wider area around a specific user's last emotion
    python manage.py generate_random_emotions --email testing_frontend_1@example.com --radius 0.5
"""

from django.core.management.base import BaseCommand
from apps.emotions.models import Emotion, SharedEmotion
from django.contrib.auth import get_user_model
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generates random emotions at random locations. Usage: python manage.py generate_random_emotions [--count N] [--email EMAIL] [--radius R]'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of random emotions to generate (default: 10)'
        )
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='Email of the user whose last emotion will be used as reference point'
        )
        parser.add_argument(
            '--radius',
            type=float,
            default=0.1,
            help='Radius in degrees around the reference point (default: 0.1)'
        )

    def handle(self, *args, **options):
        count = options['count']
        email = options['email']
        radius = options['radius']

        # Get all existing emotions and the reference user
        emotions = list(Emotion.objects.all())
        User = get_user_model()
        try:
            reference_user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with email {email} not found'))
            return

        # Get the reference user's last emotion
        try:
            reference_emotion = SharedEmotion.objects.filter(user=reference_user).latest('created_at')
            ref_lat = reference_emotion.latitude
            ref_lon = reference_emotion.longitude
        except SharedEmotion.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'No emotions found for user {email}'))
            return

        # Get all testing users
        testing_users = list(User.objects.filter(email__contains='testing_frontend'))
        if not testing_users:
            self.stdout.write(self.style.ERROR('No testing users found in the database'))
            return

        if not emotions:
            self.stdout.write(self.style.ERROR('No emotions found in the database'))
            return

        # Generate random emotions
        created_count = 0
        for _ in range(count):
            try:
                # Pick random emotion and user
                emotion = random.choice(emotions)
                user = random.choice(testing_users)

                # Generate random coordinates within radius degrees of the reference point
                lat = ref_lat + random.uniform(-radius, radius)
                lon = ref_lon + random.uniform(-radius, radius)

                # Ensure coordinates are within valid ranges
                lat = max(min(lat, 90), -90)
                lon = max(min(lon, 180), -180)

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
                        f'Created emotion: {emotion.name} for user {user.email} at ({lat:.6f}, {lon:.6f})'
                    )
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating emotion: {str(e)}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} random emotions within {radius} degrees of the last emotion of user {email}'
            )
        )