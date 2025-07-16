from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from borrowing.models import Borrowing
from book.models import Book
from payment.models import Payment

User = get_user_model()


class PaymentViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="pass123"
        )
        self.staff = User.objects.create_user(
            email="staff@example.com", password="pass123", is_staff=True
        )

        self.book = Book.objects.create(
            title="Book for payment",
            author="Author",
            cover="HARD",
            inventory=1,
            daily_fee=10.0,
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            borrow_date="2025-01-01",
            expected_return_date="2025-01-10",
            actual_return_date=None,
        )

        self.payment = Payment.objects.create(
            status=Payment.Status.PENDING,
            type=Payment.Type.PAYMENT,
            borrowing=self.borrowing,
            session_url="https://example.com/session",
            session_id="session123",
            money_to_pay=100,
        )

    def test_list_payments_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("payment:payment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(p["id"] == self.payment.id for p in response.data))

    def test_list_payments_unauthenticated(self):
        url = reverse("payment:payment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_payment_as_non_staff_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("payment:payment-list")
        data = {
            "status": Payment.Status.PAID,
            "type": Payment.Type.FINE,
            "borrowing": self.borrowing.id,
            "session_url": "https://example.com/session2",
            "session_id": "session124",
            "money_to_pay": "50.00",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
