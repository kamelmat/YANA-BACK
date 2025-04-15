from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="testpass123",
            name="Test",
            last_name="User"
        )

    def test_user_creation(self):
        self.assertEqual(str(self.user), "test@example.com")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_admin)
        self.assertFalse(self.user.is_staff)
        self.assertIsNotNone(self.user.user_id)
        self.assertEqual(self.user.avatar_id, 34)

    def test_superuser_creation(self):
        superuser = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123"
        )
        self.assertTrue(superuser.is_admin)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.avatar_id, 34)

class UserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            password="testpass123",
            name="Test",
            last_name="User"
        )
        self.superuser = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123"
        )

    def test_register_user(self):
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'password': 'Newpass123!',
            'name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)
        self.assertIn('avatar_id', response.data)
        self.assertEqual(response.data['avatar_id'], 34)
        self.assertEqual(CustomUser.objects.count(), 3)
        new_user = CustomUser.objects.get(email='newuser@example.com')
        self.assertEqual(new_user.avatar_id, 34)

    def test_login_user(self):
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        user_data = response.data['user']
        self.assertEqual(user_data['email'], 'test@example.com')
        self.assertEqual(user_data['user_id'], self.user.user_id)
        self.assertEqual(user_data['name'], 'Test')
        self.assertEqual(user_data['avatar_id'], 34)

    def test_get_users(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_generate_user_id_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('generate_user_id')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_id', response.data)

    def test_generate_user_id_unauthenticated(self):
        url = reverse('generate_user_id')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        self.client.force_authenticate(user=self.user)
        refresh = RefreshToken.for_user(self.user)
        url = reverse('logout')
        data = {'refresh': str(refresh)}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Logout successful"})

    def test_password_validation(self):
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'password': 'weak',
            'name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_check_email_exists(self):
        url = reverse('check-email')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['email_exists'])

    def test_check_email_not_exists(self):
        url = reverse('check-email')
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['email_exists'])

    def test_check_email_missing(self):
        url = reverse('check-email')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_delete_account(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('delete-account')
        data = {'password': 'testpass123'}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Account successfully deleted"})
        self.assertFalse(CustomUser.objects.filter(email='test@example.com').exists())

    def test_delete_account_wrong_password(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('delete-account')
        data = {'password': 'wrongpassword'}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_delete_account_unauthenticated(self):
        url = reverse('delete-account')
        data = {'password': 'testpass123'}
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

