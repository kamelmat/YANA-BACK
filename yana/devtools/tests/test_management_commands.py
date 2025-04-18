"""
How to run the tests:
    python manage.py test devtools.tests.test_management_commands

How to run the management commands:
    1. Add emotions:
        python manage.py add_emotions "Emotion1" "Emotion2" "Emotion3"
    
    2. Delete last N emotions:
        python manage.py delete_last_emotions --count 5
    
    3. Clear all user emotions:
        python manage.py clear_user_emotions --confirm
    
    4. Generate random emotions:
        python manage.py generate_random_emotions --count 10 --radius 5.0
    
    5. Export database to JSON:
        python manage.py export_db_json
"""

from django.core.management import call_command
from django.test import TestCase
from apps.emotions.models import Emotion, SharedEmotion
from django.contrib.auth import get_user_model
import json
import os

class ManagementCommandsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test',
            last_name='User'
        )

    def test_add_emotions(self):
        # Test adding new emotions
        call_command('add_emotions', 'Happiness', 'Sadness')
        
        # Verify emotions were created
        self.assertTrue(Emotion.objects.filter(name='Happiness').exists())
        self.assertTrue(Emotion.objects.filter(name='Sadness').exists())
        
        # Test adding existing emotions
        call_command('add_emotions', 'Happiness')
        self.assertEqual(Emotion.objects.filter(name='Happiness').count(), 1)

    def test_delete_last_emotions(self):
        # Create some emotions
        emotions = ['Emotion1', 'Emotion2', 'Emotion3', 'Emotion4', 'Emotion5']
        for name in emotions:
            Emotion.objects.create(name=name)
        
        # Delete last 3 emotions
        call_command('delete_last_emotions', '--count', '3')
        
        # Verify only first 2 emotions remain
        self.assertEqual(Emotion.objects.count(), 2)
        self.assertTrue(Emotion.objects.filter(name='Emotion1').exists())
        self.assertTrue(Emotion.objects.filter(name='Emotion2').exists())

    def test_clear_user_emotions(self):
        # Create some shared emotions
        emotion = Emotion.objects.create(name='TestEmotion')
        SharedEmotion.objects.create(
            user=self.user,
            emotion=emotion,
            latitude=0.0,
            longitude=0.0,
            is_active=True
        )
        
        # Try to clear without confirmation
        call_command('clear_user_emotions')
        self.assertEqual(SharedEmotion.objects.count(), 1)
        
        # Clear with confirmation
        call_command('clear_user_emotions', '--confirm')
        self.assertEqual(SharedEmotion.objects.count(), 0)

    def test_generate_random_emotions(self):
        # Create base emotion
        Emotion.objects.create(name='BaseEmotion')
        
        # Generate random emotions
        call_command('generate_random_emotions', '--count', '5', '--radius', '1.0')
        
        # Verify emotions were created
        self.assertEqual(SharedEmotion.objects.count(), 5)
        
        # Verify coordinates are within valid ranges
        for emotion in SharedEmotion.objects.all():
            self.assertTrue(-90 <= float(emotion.latitude) <= 90)
            self.assertTrue(-180 <= float(emotion.longitude) <= 180)

    def test_export_db_json(self):
        # Create some test data
        emotion = Emotion.objects.create(name='TestEmotion')
        SharedEmotion.objects.create(
            user=self.user,
            emotion=emotion,
            latitude=0.0,
            longitude=0.0,
            is_active=True
        )
        
        # Export database
        call_command('export_db_json')
        
        # Find the exported file
        files = [f for f in os.listdir('.') if f.startswith('db_export_') and f.endswith('.json')]
        self.assertTrue(len(files) > 0)
        
        # Read and verify the export
        with open(files[0], 'r') as f:
            data = json.load(f)
            # Check that the emotions app data exists
            self.assertTrue('emotions' in data)
            emotions_data = data['emotions']
            # Check that both tables exist in the emotions app data
            self.assertTrue('emotions_emotion' in emotions_data)
            self.assertTrue('emotions_sharedemotion' in emotions_data)
            
        # Clean up
        os.remove(files[0]) 