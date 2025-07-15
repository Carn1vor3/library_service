from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from book.models import Book
from rest_framework.reverse import reverse
from rest_framework import status

User = get_user_model()


class BookViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.staff = User.objects.create_user(
            email='staff@example.com',
            password='staffpass123',
            is_staff=True
        )

        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            cover='HARD',
            inventory=3,
            daily_fee=5.00
        )

    # ----------- SAFE_METHODS (GET) -----------

    def test_list_books_as_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_book_as_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book:book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_books_as_staff(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse('book:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ----------- CREATE (POST) -----------

    def test_create_book_as_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book:book-list')
        data = {
            'title': 'Forbidden Book',
            'author': 'Somebody',
            'cover': 'SOFT',
            'inventory': 2,
            'daily_fee': '1.99'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_as_staff(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse('book:book-list')
        data = {
            'title': 'New Book',
            'author': 'Admin Author',
            'cover': 'SOFT',
            'inventory': 5,
            'daily_fee': '3.50'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    # ----------- UPDATE (PUT) -----------

    def test_update_book_as_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book:book-detail', args=[self.book.id])
        data = {
            'title': 'Should Fail',
            'author': 'Fail Author',
            'cover': 'SOFT',
            'inventory': 1,
            'daily_fee': '2.00'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_as_staff(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse('book:book-detail', args=[self.book.id])
        data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'cover': 'SOFT',
            'inventory': 10,
            'daily_fee': '7.99'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')

    # ----------- PARTIAL UPDATE (PATCH) -----------

    def test_partial_update_book_as_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book:book-detail', args=[self.book.id])
        data = {'title': 'Patch Fail'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_book_as_staff(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse('book:book-detail', args=[self.book.id])
        data = {'title': 'Patch OK'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Patch OK')

    # ----------- DELETE -----------

    def test_delete_book_as_user_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('book:book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_as_staff(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse('book:book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
