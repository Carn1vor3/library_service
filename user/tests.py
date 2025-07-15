from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class UserRegistrationTests(APITestCase):
    def test_register_user_success(self):
        url = reverse('user:register')
        data = {
            "email": "newuser@example.com",
            "password": "strongpassword123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["email"], data["email"])
        self.assertNotIn("password", response.data)


class UserAuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('user:register')
        self.token_url = reverse('user:token_obtain_pair')
        self.me_url = reverse('user:manage')
        self.user_data = {
            "email": "testuser@example.com",
            "password": "strongpassword123"
        }
        self.client.post(self.register_url, self.user_data)

    def test_login_and_access_protected(self):
        response = self.client.post(self.token_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_access_protected_without_token(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)