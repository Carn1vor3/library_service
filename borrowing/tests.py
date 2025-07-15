from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from book.models import Book
from borrowing.models import Borrowing
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class BorrowingViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="testpass")
        self.staff = User.objects.create_user(email="staff@example.com", password="staffpass", is_staff=True)

        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            cover="HARD",
            inventory=2,
            daily_fee=5.00,
        )

        # Існуюча позика
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timedelta(days=7),
            actual_return_date=None
        )

    def test_list_borrowings_user_sees_only_their(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("borrowing:borrowing-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Має бачити лише свої borrowings
        self.assertEqual(len(response.data), 1)

    def test_list_borrowings_staff_sees_all(self):
        other_user = User.objects.create_user(email="other@example.com", password="testpass")
        Borrowing.objects.create(
            user=other_user,
            book=self.book,
            borrow_date=timezone.now().date(),
            expected_return_date=timezone.now().date() + timedelta(days=5),
        )
        self.client.force_authenticate(user=self.staff)
        url = reverse("borrowing:borrowing-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Має бачити 2 позики
        self.assertEqual(len(response.data), 2)

    def test_create_borrowing_decreases_book_inventory(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("borrowing:borrowing-list")
        data = {
            "book": self.book.id,
            "borrow_date": timezone.now().date(),
            "expected_return_date": (timezone.now() + timedelta(days=10)).date(),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 1)  # 2 - 1 = 1

    def test_cannot_create_borrowing_if_no_inventory(self):
        self.book.inventory = 0
        self.book.save()
        self.client.force_authenticate(user=self.user)
        url = reverse("borrowing:borrowing-list")
        data = {
            "book": self.book.id,
            "borrow_date": timezone.now().date(),
            "expected_return_date": (timezone.now() + timedelta(days=10)).date(),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No books left in inventory.", str(response.data))

    def test_return_borrowing_updates_actual_return_date_and_inventory(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("borrowing:borrowing-return", args=[self.borrowing.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.borrowing.refresh_from_db()
        self.book.refresh_from_db()

        self.assertIsNotNone(self.borrowing.actual_return_date)
        self.assertEqual(self.book.inventory, 3)  # 2 - 1 + 1

    def test_cannot_return_twice(self):
        self.borrowing.actual_return_date = timezone.now().date()
        self.borrowing.save()

        self.client.force_authenticate(user=self.user)
        url = reverse("borrowing:borrowing-return", args=[self.borrowing.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already been returned", str(response.data))
