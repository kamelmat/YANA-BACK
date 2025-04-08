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
