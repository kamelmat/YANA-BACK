from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Emotion, UserEmotion
from datetime import datetime

User = get_user_model()

class EmotionModelTest(TestCase):
    def setUp(self):
        self.emotion = Emotion.objects.create(name="Happy")

    def test_emotion_creation(self):
        self.assertEqual(str(self.emotion), "Happy")
        self.assertEqual(self.emotion.name, "Happy")

class UserEmotionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            name="Test",
            last_name="User"
        )
        self.emotion = Emotion.objects.create(name="Happy")
        self.user_emotion = UserEmotion.objects.create(
            user=self.user,
            emotion=self.emotion
        )

    def test_user_emotion_creation(self):
        self.assertEqual(self.user_emotion.user, self.user)
        self.assertEqual(self.user_emotion.emotion, self.emotion)
        self.assertIsNotNone(self.user_emotion.timestamp)

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
        data = {'emotion': self.emotion.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserEmotion.objects.count(), 1)
        user_emotion = UserEmotion.objects.first()
        self.assertEqual(user_emotion.user, self.user)
        self.assertEqual(user_emotion.emotion, self.emotion)

    def test_create_user_emotion_unauthenticated(self):
        data = {'emotion': self.emotion.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(UserEmotion.objects.count(), 0)

    def test_create_user_emotion_invalid_emotion(self):
        self.client.force_authenticate(user=self.user)
        data = {'emotion': 999}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserEmotion.objects.count(), 0)

    def test_create_user_emotion_missing_emotion(self):
        self.client.force_authenticate(user=self.user)
        data = {}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UserEmotion.objects.count(), 0)

class UserEmotionListViewTest(TestCase):
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
        
        self.user_emotion1 = UserEmotion.objects.create(
            user=self.user,
            emotion=self.emotion1
        )
        self.user_emotion2 = UserEmotion.objects.create(
            user=self.user,
            emotion=self.emotion2
        )
        
        self.other_user_emotion = UserEmotion.objects.create(
            user=self.other_user,
            emotion=self.emotion3
        )
        
        self.url = reverse('user-emotion-list')

    def test_get_user_emotions_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        emotion_names = [item['emotion_name'] for item in response.data]
        self.assertIn('Happy', emotion_names)
        self.assertIn('Sad', emotion_names)
        self.assertNotIn('Angry', emotion_names)

    def test_get_user_emotions_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_emotions_ordered_by_timestamp(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        timestamps = [item['timestamp'] for item in response.data]
        self.assertEqual(timestamps, sorted(timestamps, reverse=True))

class EmotionViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            name="Test",
            last_name="User"
        )
        self.emotion = Emotion.objects.create(name="Happy")
        self.user_emotion = UserEmotion.objects.create(
            user=self.user,
            emotion=self.emotion
        )

    def test_get_emotions_list(self):
        url = reverse('emotion-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_emotion_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('user-create-emotion')
        data = {'emotion': self.emotion.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserEmotion.objects.count(), 2)

    def test_create_emotion_unauthenticated(self):
        url = reverse('user-create-emotion')
        data = {'name': 'Sad'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_bulk_create_emotions(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('emotion-bulk-create')
        data = [
            {'name': 'Angry'},
            {'name': 'Excited'}
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Emotion.objects.count(), 3)

    def test_get_user_emotions(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('emotion-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
