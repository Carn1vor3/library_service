from django.db import models
from rest_framework.exceptions import ValidationError

from book.models import Book
from library_service import settings


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def clean(self):
        if self.borrow_date > self.expected_return_date:
            raise ValidationError("Borrowing date must be before expected return date")
        if self.actual_return_date:
            if self.actual_return_date < self.borrow_date:
                raise ValidationError(
                    "Borrowing date cannot be after actual return date"
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.book.title}, {self.expected_return_date}, {self.actual_return_date}"
        )