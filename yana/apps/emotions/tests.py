from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Emotion, SharedEmotion
from datetime import datetime, timedelta
import time

User = get_user_model()

class EmotionModelTest(TestCase):
    def setUp(self):
        self.emotion = Emotion.objects.create(name="Happy")

    def test_emotion_creation(self):
        self.assertEqual(str(self.emotion), "Happy")
        self.assertEqual(self.emotion.name, "Happy")

class SharedEmotionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            name="Test",
            last_name="User"
        )
        self.emotion = Emotion.objects.create(name="Happy")
        self.shared_emotion = SharedEmotion.objects.create(
            user=self.user,
            emotion=self.emotion,
            latitude=40.7128,
            longitude=-74.0060
        )

    def test_shared_emotion_creation(self):
        self.assertEqual(self.shared_emotion.user, self.user)
        self.assertEqual(self.shared_emotion.emotion, self.emotion)
        self.assertEqual(self.shared_emotion.latitude, 40.7128)
        self.assertEqual(self.shared_emotion.longitude, -74.0060)
        self.assertTrue(self.shared_emotion.is_active)
        self.assertIsNotNone(self.shared_emotion.created_at)

class UserCreateEmotionViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            name="Test",
            last_name="User"
        )
        self.emotion = Emotion.objects.create(name="Happy")
        self.url = reverse('user-create-emotion')

    def test_create_user_emotion_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'emotion_id': self.emotion.id,
            'latitude': 40.7128,
            'longitude': -74.0060
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SharedEmotion.objects.count(), 1)
        shared_emotion = SharedEmotion.objects.first()
        self.assertEqual(shared_emotion.user, self.user)
        self.assertEqual(shared_emotion.emotion, self.emotion)
        self.assertEqual(shared_emotion.latitude, 40.7128)
        self.assertEqual(shared_emotion.longitude, -74.0060)

    def test_create_user_emotion_unauthenticated(self):
        data = {
            'emotion_id': self.emotion.id,
            'latitude': 40.7128,
            'longitude': -74.0060
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(SharedEmotion.objects.count(), 0)

    def test_create_user_emotion_invalid_emotion(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'emotion_id': 999,
            'latitude': 40.7128,
            'longitude': -74.0060
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SharedEmotion.objects.count(), 0)

    def test_create_user_emotion_missing_required_fields(self):
        self.client.force_authenticate(user=self.user)
        data = {'emotion_id': self.emotion.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SharedEmotion.objects.count(), 0)

class SharedEmotionListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            name="Test",
            last_name="User"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass123",
            name="Other",
            last_name="User"
        )
        self.emotion1 = Emotion.objects.create(name="Happy")
        self.emotion2 = Emotion.objects.create(name="Sad")
        self.emotion3 = Emotion.objects.create(name="Angry")
        
        self.shared_emotion1 = SharedEmotion.objects.create(
            user=self.user,
            emotion=self.emotion1,
            latitude=40.7128,
            longitude=-74.0060
        )
        self.shared_emotion2 = SharedEmotion.objects.create(
            user=self.user,
            emotion=self.emotion2,
            latitude=40.7128,
            longitude=-74.0060
        )
        
        self.other_shared_emotion = SharedEmotion.objects.create(
            user=self.other_user,
            emotion=self.emotion3,
            latitude=40.7128,
            longitude=-74.0060
        )
        
        self.url = reverse('user-emotion-list')

    def test_get_user_emotions_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        emotions = [item['emotion'] for item in response.data]
        self.assertIn('Happy', emotions)
        self.assertIn('Sad', emotions)
        self.assertNotIn('Angry', emotions)

    def test_get_user_emotions_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_emotions_ordered_by_created_at(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        created_at_times = [item['created_at'] for item in response.data]
        self.assertEqual(created_at_times, sorted(created_at_times, reverse=True))

class NearbyEmotionsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            name="Test",
            last_name="User"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass123",
            name="Other",
            last_name="User"
        )
        self.emotion1 = Emotion.objects.create(name="Happy")
        self.emotion2 = Emotion.objects.create(name="Sad")
        self.emotion3 = Emotion.objects.create(name="Angry")
        
        # Create emotions with explicit timestamps
        now = datetime.now()
        self.other_user_emotion1 = SharedEmotion.objects.create(
            user=self.other_user,
            emotion=self.emotion1,  # Happy
            latitude=40.7128,
            longitude=-74.0060,
            created_at=now - timedelta(days=2)
        )
        time.sleep(0.1)  # Small delay to ensure different timestamps
        self.other_user_emotion2 = SharedEmotion.objects.create(
            user=self.other_user,
            emotion=self.emotion2,  # Sad
            latitude=40.7128,
            longitude=-74.0060,
            created_at=now - timedelta(hours=1)
        )
        
        # Create an emotion for a third user
        self.third_user = User.objects.create_user(
            email="third@example.com",
            password="testpass123",
            name="Third",
            last_name="User"
        )
        time.sleep(0.1)
        self.third_user_emotion = SharedEmotion.objects.create(
            user=self.third_user,
            emotion=self.emotion3,  # Angry
            latitude=40.7128,
            longitude=-74.0060,
            created_at=now
        )
        
        self.url = reverse('nearby_emotions')

    def test_get_nearby_emotions_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_nearby_emotions_no_user_emotion(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_nearby_emotions_matching_emotion(self):
        # Create a Sad emotion for the authenticated user
        self.user_emotion = SharedEmotion.objects.create(
            user=self.user,
            emotion=self.emotion2,  # Sad
            latitude=40.7128,
            longitude=-74.0060,
            created_at=datetime.now()
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should see other_user's Sad emotion
        
        emotions = [item['emotion'] for item in response.data]
        self.assertIn('Sad', emotions)
        self.assertNotIn('Happy', emotions)
        self.assertNotIn('Angry', emotions)

    def test_get_nearby_emotions_no_matching_emotions(self):
        # Create a Happy emotion for the authenticated user
        self.user_emotion = SharedEmotion.objects.create(
            user=self.user,
            emotion=self.emotion1,  # Happy
            latitude=40.7128,
            longitude=-74.0060,
            created_at=datetime.now()
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No other users have Happy as their latest emotion

    def test_get_nearby_emotions_multiple_matches(self):
        # Create a Sad emotion for the authenticated user
        self.user_emotion = SharedEmotion.objects.create(
            user=self.user,
            emotion=self.emotion2,  # Sad
            latitude=40.7128,
            longitude=-74.0060,
            created_at=datetime.now()
        )
        
        # Create another user with Sad as their latest emotion
        self.fourth_user = User.objects.create_user(
            email="fourth@example.com",
            password="testpass123",
            name="Fourth",
            last_name="User"
        )
        time.sleep(0.1)
        self.fourth_user_emotion = SharedEmotion.objects.create(
            user=self.fourth_user,
            emotion=self.emotion2,  # Sad
            latitude=40.7128,
            longitude=-74.0060,
            created_at=datetime.now()
        )
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should see both other_user's and fourth_user's Sad emotions
        
        emotions = [item['emotion'] for item in response.data]
        self.assertEqual(emotions.count('Sad'), 2)
        self.assertNotIn('Happy', emotions)
        self.assertNotIn('Angry', emotions)

class LastUserEmotionViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            name="Test",
            last_name="User"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass123",
            name="Other",
            last_name="User"
        )
        self.emotion1 = Emotion.objects.create(name="Happy")
        self.emotion2 = Emotion.objects.create(name="Sad")
        
        now = datetime.now()
        self.shared_emotion1 = SharedEmotion.objects.create(
            user=self.user,
            emotion=self.emotion1,
            latitude=40.7128,
            longitude=-74.0060,
            created_at=now - timedelta(days=2)
        )

        time.sleep(0.1)
        self.shared_emotion2 = SharedEmotion.objects.create(
            user=self.user,
            emotion=self.emotion2,
            latitude=40.7128,
            longitude=-74.0060,
            created_at=now - timedelta(hours=1)
        )
        
        self.other_shared_emotion = SharedEmotion.objects.create(
            user=self.other_user,
            emotion=self.emotion1,
            latitude=40.7128,
            longitude=-74.0060,
            created_at=now
        )
        
        self.url = reverse('user-last-emotion')

    def test_get_last_emotion_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['emotion'], 'Sad')
        self.assertEqual(response.data['latitude'], 40.7128)
        self.assertEqual(response.data['longitude'], -74.0060)

    def test_get_last_emotion_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_last_emotion_no_emotions(self):
        SharedEmotion.objects.filter(user=self.user).delete()
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No emotions found for this user')

    def test_get_last_emotion_only_active(self):
        self.shared_emotion2.is_active = False
        self.shared_emotion2.save()
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['emotion'], 'Happy')
