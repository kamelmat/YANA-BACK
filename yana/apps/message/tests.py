from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import SupportMessageTemplate, SupportMessage
from apps.emotions.models import SharedEmotion, Emotion

User = get_user_model()

class MessageTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            email='testuser1@example.com',
            password='testpass123',
            name='Test',
            last_name='User1'
        )
        self.user2 = User.objects.create_user(
            email='testuser2@example.com',
            password='testpass123',
            name='Test',
            last_name='User2'
        )
        self.template = SupportMessageTemplate.objects.create(text='Test template')
        self.emotion = Emotion.objects.create(name='happy')
        self.shared_emotion = SharedEmotion.objects.create(
            user=self.user2,
            emotion=self.emotion,
            latitude=40.7128,
            longitude=-74.0060
        )

    def test_send_support_message(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('send-support')
        data = {
            'shared_emotion': self.shared_emotion.id,
            'template_id': self.template.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(SupportMessage.objects.filter(
            sender=self.user1,
            receiver=self.user2,
            message=self.template.text
        ).exists())

    def test_send_support_message_to_self(self):
        # Create a shared emotion for user1
        self_shared_emotion = SharedEmotion.objects.create(
            user=self.user1,
            emotion=self.emotion,
            latitude=40.7128,
            longitude=-74.0060
        )
        
        self.client.force_authenticate(user=self.user1)
        url = reverse('send-support')
        data = {
            'shared_emotion': self_shared_emotion.id,
            'template_id': self.template.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(SupportMessage.objects.filter(
            sender=self.user1,
            receiver=self.user1
        ).exists())

    def test_send_support_message_invalid_emotion(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('send-support')
        data = {
            'shared_emotion': 999,  # Non-existent emotion ID
            'template_id': self.template.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_support_message_invalid_template(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('send-support')
        data = {
            'shared_emotion': self.shared_emotion.id,
            'template_id': 999  # Non-existent template ID
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_support_message_unauthenticated(self):
        url = reverse('send-support')
        data = {
            'shared_emotion': self.shared_emotion.id,
            'template_id': self.template.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_support_templates(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('support-templates')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['text'], 'Test template')

    def test_get_support_templates_unauthenticated(self):
        url = reverse('support-templates')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # This endpoint is public

    def test_get_received_messages(self):
        SupportMessage.objects.create(
            sender=self.user1,
            receiver=self.user2,
            message=self.template.text
        )
        self.client.force_authenticate(user=self.user2)
        url = reverse('received-messages')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_received_messages_unauthenticated(self):
        url = reverse('received-messages')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_received_messages_empty(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('received-messages')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_notifications(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('notifications')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, bool)

    def test_mark_messages_as_read(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('message-as-read')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user2.refresh_from_db()
        self.assertFalse(self.user2.unread_messages)
