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

    6. Create test users:
        python manage.py create_test_users --count 50 --email-pattern testing_frontend
"""

from django.core.management import call_command
from django.test import TestCase
from apps.emotions.models import Emotion, SharedEmotion
from django.contrib.auth import get_user_model
import json
import os
from io import StringIO
import re

User = get_user_model()

class ManagementCommandsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test',
            last_name='User'
        )

    def test_add_emotions(self):
        call_command('add_emotions', 'Happiness', 'Sadness')
        
        self.assertTrue(Emotion.objects.filter(name='Happiness').exists())
        self.assertTrue(Emotion.objects.filter(name='Sadness').exists())
        
        call_command('add_emotions', 'Happiness')
        self.assertEqual(Emotion.objects.filter(name='Happiness').count(), 1)

    def test_delete_last_emotions(self):
        emotions = ['Emotion1', 'Emotion2', 'Emotion3', 'Emotion4', 'Emotion5']
        for name in emotions:
            Emotion.objects.create(name=name)
        
        call_command('delete_last_emotions', '--count', '3')
        
        self.assertEqual(Emotion.objects.count(), 2)
        self.assertTrue(Emotion.objects.filter(name='Emotion1').exists())
        self.assertTrue(Emotion.objects.filter(name='Emotion2').exists())

    def test_clear_user_emotions(self):
        emotion = Emotion.objects.create(name='TestEmotion')
        SharedEmotion.objects.create(
            user=self.user,
            emotion=emotion,
            latitude=0.0,
            longitude=0.0,
            is_active=True
        )
        
        call_command('clear_user_emotions')
        self.assertEqual(SharedEmotion.objects.count(), 1)
        
        call_command('clear_user_emotions', '--confirm')
        self.assertEqual(SharedEmotion.objects.count(), 0)

    def test_generate_random_emotions(self):
        # Create test users with testing_frontend pattern
        call_command('create_test_users', '--count', '5', stdout=StringIO())
        
        # Create base emotion and a reference user's emotion
        emotion = Emotion.objects.create(name='BaseEmotion')
        reference_user = get_user_model().objects.first()
        reference_emotion = SharedEmotion.objects.create(
            user=reference_user,
            emotion=emotion,
            latitude=40.7128,  # New York coordinates
            longitude=-74.0060
        )
        
        # Generate random emotions
        call_command('generate_random_emotions', '--count', '5', '--email', reference_user.email, '--radius', '0.1')
        
        # Verify emotions were created
        self.assertEqual(SharedEmotion.objects.count(), 6)  # Reference + 5 new
        
        # Verify all emotions are within the specified radius of the reference point
        emotions = SharedEmotion.objects.exclude(id=reference_emotion.id)
        for emotion in emotions:
            # Check latitude is within 0.1 degrees
            self.assertTrue(abs(emotion.latitude - reference_emotion.latitude) <= 0.1)
            # Check longitude is within 0.1 degrees
            self.assertTrue(abs(emotion.longitude - reference_emotion.longitude) <= 0.1)
            # Verify coordinates are within valid ranges
            self.assertTrue(-90 <= emotion.latitude <= 90)
            self.assertTrue(-180 <= emotion.longitude <= 180)
            # Verify emotion was created by a testing user
            self.assertTrue('testing_frontend' in emotion.user.email)

    def test_export_db_json(self):
        emotion = Emotion.objects.create(name='TestEmotion')
        SharedEmotion.objects.create(
            user=self.user,
            emotion=emotion,
            latitude=0.0,
            longitude=0.0,
            is_active=True
        )
        
        call_command('export_db_json')
        
        json_files = [f for f in os.listdir('.') if f.startswith('db_export_') and f.endswith('.json')]
        self.assertTrue(len(json_files) > 0)
        
        with open(json_files[0], 'r') as f:
            data = json.load(f)
            self.assertTrue('emotions' in data)
            self.assertTrue('emotions_emotion' in data['emotions'])
            self.assertTrue('emotions_sharedemotion' in data['emotions'])
        
        os.remove(json_files[0])

class CreateTestUsersCommandTest(TestCase):
    def setUp(self):
        self.out = StringIO()

    def test_create_test_users_default(self):
        """Test creating users with default parameters"""
        call_command('create_test_users', stdout=self.out)
        output = self.out.getvalue()
        
        users = User.objects.filter(email__contains='testing_frontend')
        self.assertEqual(users.count(), 50)
        
        for user in users:
            self.assertTrue(user.email.startswith('testing_frontend_'))
            self.assertTrue(user.email.endswith('@example.com'))
            self.assertIn(user.name, ['John', 'Jane'])
            self.assertIn(user.last_name, ['Smith', 'Doe'])
            self.assertTrue(user.check_password('testpass123'))

    def test_create_test_users_custom_count(self):
        """Test creating users with custom count"""
        call_command('create_test_users', '--count', '10', stdout=self.out)
        output = self.out.getvalue()
        
        users = User.objects.filter(email__contains='testing_frontend')
        self.assertEqual(users.count(), 10)

    def test_create_test_users_custom_email_pattern(self):
        """Test creating users with custom email pattern"""
        call_command('create_test_users', '--email-pattern', 'testing_mobile', stdout=self.out)
        output = self.out.getvalue()
        
        users = User.objects.filter(email__contains='testing_mobile')
        self.assertEqual(users.count(), 50)
        
        for user in users:
            self.assertTrue(user.email.startswith('testing_mobile_'))
            self.assertTrue(user.email.endswith('@example.com'))

    def test_create_test_users_output_format(self):
        """Test the output format of the command"""
        call_command('create_test_users', '--count', '2', stdout=self.out)
        output = self.out.getvalue()
        
        lines = output.strip().split('\n')
        self.assertEqual(len(lines), 3)
        
        for line in lines[:-1]:
            self.assertTrue('Created test user:' in line)
            self.assertTrue('@example.com' in line)
            self.assertTrue('(' in line and ')' in line)
        
        self.assertTrue('Successfully created 2 test users' in lines[-1]) 