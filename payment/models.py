from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "PENDING"
        PAID = "PAID", "PAID"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT", "PAYMENT"
        FINE = "FINE", "FINE"

    status = models.CharField(max_length=20, choices=Status.choices)
    type = models.CharField(max_length=20, choices=Type.choices)
    borrowing = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.CharField(max_length=100, unique=True)
    money_to_pay = models.DecimalField(decimal_places=2, max_digits=20)
